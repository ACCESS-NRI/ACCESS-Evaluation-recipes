![ACCESS-NRI logo](web/assets/access-nri-logo.svg)

# ACCESS Evaluation Recipes

A community collection of notebooks and ESMValTool workflows for evaluating ACCESS and other climate models. The collection began with the [CLIVAR ENSO metrics](https://doi.org/10.1175/BAMS-D-19-0337.1) and now includes the Indian Ocean Dipole, MJO/BSISO, ocean diagnostics, examples, and training material. Most notebooks use [ESMValCore](https://docs.esmvaltool.org/projects/ESMValCore/en/stable/) to discover, load, and preprocess climate data.

**[Browse the recipe gallery](https://access-nri.github.io/ACCESS-Evaluation-recipes/)** to search the collection and filter by ACCESS model, scientific subject, realm, tool, or recipe type. Click the screenshot to open the live gallery.

The [Russell Southern Ocean comparison](web/results/russell-1986-2005/index.html)
presents a completed Gadi demonstration combining ACCESS-OM3 and ACCESS-CM3 with
selected CMIP6/CMIP7 models: 35 plots across 16 diagnostic groups, with coverage
and validation scope documented alongside the results.

[![Screenshot of the ACCESS Evaluation Recipes gallery showing the model diagram and recipe counts](docs/gallery-screenshot.jpg)](https://access-nri.github.io/ACCESS-Evaluation-recipes/)

The model spotlight features ACCESS-ESM1.5, ACCESS-ESM1.6, ACCESS-OM2, ACCESS-OM3, ACCESS-ESM3, and ACCESS-CM3. Counts reflect recipes with an explicit model input or comparison, so a model without tagged recipes may still be usable with a general method. Previews illustrate a notebook; they do not establish that its data or environment is current. To build the static gallery in [`web/`](web/) locally, run `python -m pip install -r requirements-site.txt` followed by `python scripts/build_site.py`.

## Find a recipe

The repository is organised first by purpose, then by science subject. The gallery's subject, realm, tool, and model filters come from catalogue metadata rather than folder names.

```text
recipes/              Evaluation notebooks and ESMValTool workflows
  enso/               ENSO notebooks; esmvaltool/ holds YAML workflows and scripts
  iod/                Indian Ocean Dipole notebooks
  mjo-bsiso/          Intraseasonal variability notebooks
  ocean/
    cosima/           Native ACCESS-OM/CICE analyses using the COSIMA approach
    cmip6/            CMORised ocean and sea-ice analyses using ESMValCore
    russell2018/      Russell et al. Southern Ocean diagnostics
examples/             Small ESMValCore technique demonstrations
training/             Workshop material, grouped by year
catalog/              Recipe and model metadata used by the gallery
web/                  Static gallery source and preview images
scripts/              Catalogue, preview, and workflow preparation tools
docs/                 Setup, review, and migration guidance
```

| Area | Contents |
| --- | --- |
| [ENSO metrics](recipes/enso/) | CLIVAR metrics notebooks and [ESMValTool YAML workflows](recipes/enso/esmvaltool/) |
| [Indian Ocean Dipole](recipes/iod/) | IOD characteristics and Indian Ocean climatology |
| [MJO and BSISO](recipes/mjo-bsiso/) | Intraseasonal patterns, life cycles, and precipitation biases |
| [Ocean](recipes/ocean/) | Native-model COSIMA examples, [CMIP6 counterparts](recipes/ocean/cmip6/), and Russell et al. diagnostics |
| [ESMValCore examples](examples/esmvalcore/) | Regridding, ensembles, means, and data handling |
| [Training](training/2025/) | 2025 workshop examples and exercises |

The [catalogue metadata](catalog/recipes.yml) describes all 91 notebooks and eight ESMValTool YAML recipes. It is the source for the gallery. The `catalog/legacy-paths.json` file maps files from the former `ACCESS-ENSO-recipes` layout to their new locations.

## Run a notebook

Clone this repository on NCI Gadi, open an ARE JupyterLab session, and choose a notebook from the catalogue. The data collections and compute resources needed vary by recipe. See [running recipes](docs/running.md) for setup guidance, and read the first cells of each notebook before running it.

```bash
module use /g/data/xp65/public/modules
module load conda/analysis3
git clone https://github.com/ACCESS-NRI/ACCESS-Evaluation-recipes.git
cd ACCESS-Evaluation-recipes
```

For ESMValTool YAML workflows with local diagnostic scripts, first generate machine-specific copies as described in the [ENSO ESMValTool guide](recipes/enso/esmvaltool/README.md).

## Contribute

New notebooks and YAML workflows belong in the relevant subject folder. Add a record to [the catalogue](catalog/README.md), then run `python scripts/build_site.py --check`. Use a pull request so the scientific method, data requirements, preview, and metadata can be reviewed together. [Notebook review guidance](docs/github_notebooks.md) is available for contributors.

## Provenance and citation

This project grows from ACCESS-ENSO-recipes, whose releases have a [Zenodo record](https://doi.org/10.5281/zenodo.14168217). Refer to that record when citing an earlier release. The existing GitHub repository was renamed to preserve its history and community. Check the Zenodo connection before the first release under the broader name. The original authorship remains in the notebook history and `.zenodo.json`.

Licensed under [Apache-2.0](LICENSE). Developed by the ACCESS-NRI Model Evaluation and Diagnostics team and contributors.
