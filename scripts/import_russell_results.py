"""Import a validated Russell run as a static results page (standard library only).

This imports completed results; it does not execute the scientific workflow.
NetCDF files, runtime logs and machine-specific input paths remain in the run archive.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "web/results/russell-1986-2005"
TITLES = {
    "Figure_1": "Atmospheric wind stress",
    "Figure_2": "Ocean surface wind stress",
    "Figure_3b": "Subantarctic Front",
    "Figure_3b-2": "Polar Front",
    "Figure_4": "Drake Passage section velocity",
    "Figure_5": "Sea-ice extent",
    "Figure_5g": "Southern Hemisphere sea-ice area",
    "Figure_6a": "Density-layer volume transport",
    "Figure_6b": "Density-layer heat transport",
    "Figure_7": "Surface carbon flux",
    "Figure_7h": "Zonal carbon flux",
    "Figure_7i": "Cumulative carbon flux",
    "Figure_8": "Surface pH",
    "Figure_9a": "Heat flux and wind-band width",
    "Figure_9b": "Carbon flux and wind-band width",
    "Figure_9c": "Heat and carbon flux",
}


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def collect(source: Path) -> tuple[dict, list[tuple[Path, str]]]:
    """Check the archived report and image hashes before writing public assets."""
    validation = read(source / "validation.json")
    plan = read(source / "plan.json")
    manifest = {item["path"]: item for item in read(source / "collection-manifest.json")["files"]}
    if (validation["status"] != "valid" or validation["failures"]
            or validation["input_errors"] or validation["baseline_errors"]):
        raise ValueError("The run has not passed validation")
    if plan["period"] != [1986, 2005] or plan["upstream_commit"] != validation["upstream_commit"]:
        raise ValueError("Run period or source does not match the validation report")
    checks = {group["group"]: group for group in validation["groups"]}
    if set(checks) != set(TITLES) or set(plan["groups"]) != set(TITLES):
        raise ValueError("Expected the complete set of 16 Russell diagnostic groups")
    groups, copies = [], []
    for name, title in TITLES.items():
        check = checks[name]
        if not check["valid"] or check["returncode"] != 0 or check["errors"]:
            raise ValueError(f"{name}: unsuccessful diagnostic")
        if any(item["differences"] for item in check["baseline_comparisons"]):
            raise ValueError(f"{name}: numerical baseline differences")
        plots = []
        for path in sorted((source / name / "plots").glob("*.png")):
            relative = path.relative_to(source).as_posix()
            checksum = digest(path)
            if checksum != manifest[relative]["sha256"]:
                raise ValueError(f"Image differs from collected manifest: {relative}")
            target = f"plots/{name}/{path.name}"
            plots.append({"path": target, "sha256": checksum})
            copies.append((path, target))
        if not plots or len(plots) != check["plot_count"]:
            raise ValueError(f"{name}: plot count does not match validation")
        groups.append({
            "id": name, "title": title, "models": check["expected_models"],
            "native_models": plan["groups"][name]["native_models"],
            "product_count": check["product_count"],
            "baseline_count": len(check["baseline_comparisons"]),
            "valid": True, "plots": plots,
        })
    summary = {
        "scope": "Published summary of an archived diagnostic rerun; not an independent scientific validation",
        "period": plan["period"], "upstream_commit": plan["upstream_commit"],
        "execution_mode": plan["mode"], "runtime": "Gadi analysis3-26.10",
        "runtime_versions": read(source / "provenance-finalization.json")["runtime_versions"],
        "group_count": len(groups), "plot_count": len(copies),
        "product_count": sum(group["product_count"] for group in groups),
        "baseline_count": sum(group["baseline_count"] for group in groups),
        "input_count": validation["planned_input_count"],
        "native_group_counts": {model: sum(model in g["native_models"] for g in groups)
                                for model in ("ACCESS-OM3", "ACCESS-CM3")},
        "source_report_sha256": {name: digest(source / name) for name in
                                  ("validation.json", "plan.json", "collection-manifest.json", "bundle/manifest.json")},
        "limitations": plan["limitations"], "groups": groups,
    }
    if summary["baseline_count"] != validation["baseline_product_count"]:
        raise ValueError("Baseline count does not match validation")
    return summary, copies


def render(summary: dict) -> str:
    cards, coverage = [], []
    for group in summary["groups"]:
        name, title = group["id"], escape(group["title"])
        models = ", ".join(escape(model) for model in group["models"])
        plots = "\n".join(
            f'<figure><a href="{escape(plot["path"])}"><img src="{escape(plot["path"])}" '
            f'loading="lazy" alt="{title}, plot {i}"></a><figcaption>{title} · plot {i}</figcaption></figure>'
            for i, plot in enumerate(group["plots"], 1)
        )
        cards.append(f'<article id="{name}"><p class="section-kicker">{name.replace("_", " ")}</p>'
                     f'<h2>{title}</h2><p>{models}</p><p>{group["baseline_count"]} baseline comparisons passed; '
                     f'{group["product_count"]} numerical products.</p><div class="plot-grid">{plots}</div></article>')
        cells = "".join(f'<td>{"Included" if model in group["native_models"] else "Unavailable"}</td>'
                        for model in ("ACCESS-OM3", "ACCESS-CM3"))
        coverage.append(f'<tr><th scope="row"><a href="#{name}">{title}</a></th>{cells}</tr>')
    commit = summary["upstream_commit"]
    versions = ", ".join(f'{escape(k)} {escape(v)}' for k, v in summary["runtime_versions"].items())
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Completed Southern Ocean comparison of ACCESS-OM3 and ACCESS-CM3 with selected CMIP6 and CMIP7 models using MOPPy and ESMValTool.">
<title>Russell Southern Ocean comparison | ACCESS Evaluation Recipes</title>
<link rel="stylesheet" href="../../styles.css"><link rel="stylesheet" href="results.css"></head><body>
<a class="skip-link" href="#diagnostics">Skip to results</a>
<header class="site-header"><div class="header-inner"><a class="brand" href="../../index.html">
<span class="brand-logo-panel"><img class="brand-logo" src="../../assets/access-nri-logo.svg" alt="ACCESS-NRI"></span>
<span class="brand-name"><strong>Evaluation Recipes</strong></span></a>
<nav aria-label="Primary navigation"><a href="../../index.html">Recipe gallery</a><a href="#methods">Methods and scope</a></nav></div></header>
<main class="case-study"><section class="intro"><p class="section-kicker">Completed Gadi demonstration · 1986–2005</p>
<h1>Southern Ocean evaluation across ACCESS and CMIP models</h1>
<p class="lead">ACCESS-OM3 and ACCESS-CM3 alongside selected CMIP6 and CMIP7 models, using MOPPy-CMORised ACCESS output and the updated Russell et al. diagnostics.</p>
<div class="result-stats"><div><strong>{summary['group_count']}</strong> diagnostic groups</div>
<div><strong>{summary['plot_count']}</strong> plots</div><div><strong>{summary['baseline_count']}/{summary['baseline_count']}</strong> CMIP baseline comparisons passed</div></div>
<p><strong>OM3: {summary['native_group_counts']['ACCESS-OM3']} groups. CM3: {summary['native_group_counts']['ACCESS-CM3']} groups.</strong>
The run produced {summary['product_count']} numerical products. Availability varies by diagnostic.</p>
<p class="scope-note">CM3 is a present-day control: 1986–2005 denotes model years. OM3 is a forced-ocean experiment.
These experiments have different forcing from the CMIP historical runs.</p>
<p><a href="#coverage">Check model coverage</a> · <a href="#methods">Read the validation scope</a> · <a href="summary.json">Download the validation summary and image checksums</a></p></section>
<section id="coverage"><h2>What is included?</h2><div class="table-scroll"><table><caption>ACCESS model coverage; select a diagnostic to view all its comparison models.</caption>
<thead><tr><th scope="col">Diagnostic</th><th scope="col">ACCESS-OM3</th><th scope="col">ACCESS-CM3</th></tr></thead><tbody>{''.join(coverage)}</tbody></table></div>
<p>OM3 lacks atmospheric wind stress and exact monthly pH. CM3 sea ice awaits a verified CICE grid, area and mask; validated carbon flux and exact monthly pH are also unavailable.</p></section>
<section id="methods"><h2>How these results were produced</h2>
<p><strong>ACCESS output → MOPPy CMORisation → ESMValCore preprocessing → Russell diagnostics → joint model comparison.</strong></p>
<p>This run reused audited full-period CMORised outputs and preprocessing caches. The updated diagnostic scripts were rerun on Gadi analysis3-26.10.
Local adaptations handled native cell polygons, hemisphere masks, display labels and exclusion of the ACCESS experiments from regression fits.
MOPPy CMORisation was not repeated for this diagnostic run.</p>
<p>All {summary['baseline_count']} CMIP6/CMIP7 baseline comparisons passed for scientific values, dtypes, masks, coordinates and units, subject to the Figure 9 plotting-range exception below.
Generated provenance attributes were checked separately. The {summary['input_count']} input files passed identity, time-coverage and size/mtime checks.</p>
<p>Figure 9 fits use the four selected CMIP6 models only, with OM3/CM3 added as comparison points. The updated CMIP7 recipe omits these fits.
Saved regression lines may extend over the wider plotting range; their coefficients were independently checked against the CMIP6 points.</p>
<p>The inherited climatological transport and staggered-grid approximations, native front thresholds of 4.15/2.15°C and March sea-ice season were retained.
Numerical parity establishes implementation consistency; it does not independently establish the accuracy of these scientific methods.</p>
<details><summary>Software and source provenance</summary><p>{versions}.</p>
<p>ESMValTool <a href="https://github.com/ESMValGroup/ESMValTool/pull/4612">PR 4612</a>, pinned to
<a href="https://github.com/ESMValGroup/ESMValTool/commit/{commit}">{commit}</a>.
Source-report hashes and original image checksums are in <a href="summary.json">summary.json</a>.</p>
<p>The numerical archive and reusable joint-run configuration are not distributed by this page yet.
The existing <a href="https://github.com/ACCESS-NRI/ACCESS-Evaluation-recipes/tree/main/recipes/ocean/russell2018">Russell notebooks</a>
provide related methods; they are not the execution source for this comparison.</p></details></section>
<section id="diagnostics" aria-label="Diagnostic results">{''.join(cards)}</section>
<section><h2>Credits</h2><p>Russell et al. (2018), the ESMValTool recipe contributors, ACCESS-MOPPy developers,
ACCESS model teams and CMIP data providers. This page presents a scoped evaluation demonstration.</p></section></main>
<footer><span>ACCESS Evaluation Recipes</span><span>Click a plot to inspect the original full-size image.</span></footer></body></html>
'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Collected run containing plan.json and validation.json")
    args = parser.parse_args()
    summary, copies = collect(args.source.resolve())
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for source, relative in copies:
        target = DESTINATION / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    (DESTINATION / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (DESTINATION / "index.html").write_text(render(summary), encoding="utf-8")
    print(f"Imported {len(copies)} verified plots into {DESTINATION.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
