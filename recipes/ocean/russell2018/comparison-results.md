# ACCESS-OM3 / ACCESS-CM3 comparison with CMIP6 and CMIP7

The [results page](../../../web/results/russell-1986-2005/index.html) records a
completed Gadi analysis3-26.10 demonstration for 1986–2005. It contains 35 original
plots across 16 groups and an exported validation summary. The existing repository
Pages workflow copies this page and its images into the deployed site.

## Execution and validation

- ESMValTool PR 4612 was pinned to `862c67571361ab6d094fbc3662c4c327053dcab9`.
- Native ACCESS fields were genuinely CMORised with MOPPy. This diagnostic run
  reused the audited full-period CMORised and ESMValCore preprocessed inputs.
- Local diagnostic adaptations handled native grid polygons, hemisphere masks,
  display labels and exclusion of ACCESS comparison points from regression fits.
- All 16 groups completed, producing 107 numerical outputs. The 85 CMIP6/CMIP7
  outputs passed comparison against their existing numerical baselines. Generated
  provenance attributes were checked separately. Figure 9 line coordinates may
  span the wider overlay range; the fitted coefficients still match the four
  CMIP6 points and were checked independently.
- The 182 retained inputs passed identity, period and size/mtime checks. Original
  output images are imported only after checking their collection-manifest hashes.

The public JSON summary records the upstream commit, software versions, model
coverage, original image checksums and hashes of the full source reports. It is
a summary of archived validation, not a replacement for the full numerical audit.
NetCDF products and the complete numerical audit are retained in the run archive;
they are not distributed with this initial gallery integration.

## Interpretation

CMIP6 selections include ACCESS-ESM1-5, CanESM5, GFDL-ESM4 and IPSL-CM6A-LR.
CMIP7 selections include ACCESS-ESM1-6, CanESM6-0-MR and UKESM1-3-LL. The exact
selection varies by variable and follows the pinned recipes.

OM3 is a forced-ocean experiment. CM3 is a present-day control whose labels refer
to model years. Their forcing is not identical to the CMIP historical experiments.
OM3 contributes to 14 groups and CM3 to eight. CM3 sea ice awaits verified matching
CICE grid/area/mask files; its carbon flux and exact monthly pH are unavailable.
OM3 lacks atmospheric wind stress and exact monthly pH. Figure 9 fits use CMIP6
only, with the ACCESS experiments added as comparison points.

Inherited climatological transport and staggered-grid approximations, native front
thresholds of 4.15/2.15 degrees C, and the March sea-ice season are retained.
Implementation parity does not independently validate these scientific methods.

## Refresh the presentation

Given the collected run archive on a local filesystem:

```bash
python scripts/import_russell_results.py /path/to/collected/russell-updated-pr
python scripts/build_site.py
python scripts/build_site.py --check
```

The importer uses Python's standard library. It verifies the successful run report
and image checksums before copying the original plots and generating the page and
summary. It does not rerun MOPPy or ESMValTool. Existing notebook metadata, model
counts and scientific code are unchanged.

## Next integration step: a reusable workflow

The completed demonstration still uses retained preprocessing caches. A portable
workflow needs the following separately reviewable work:

1. Add CMIP6, CMIP7 and joint ACCESS recipe/configuration examples in an
   `esmvaltool/` subdirectory, with model coverage explicit per diagnostic.
2. Document MOPPy CMORisation and grid requirements, with configurable input and
   output roots, experiment identities and an explicit software version pin.
3. Generalise `scripts/prepare_esmvaltool_recipes.py`, which currently targets
   ENSO, while preserving its existing defaults. Keep scientific diagnostics in
   ESMValTool; record any temporary local adapters and their source hashes.
4. Extend the catalogue builder's YAML discovery beyond the existing ENSO folder.
   Add records for actual new recipe files, and tag only the models they use.
5. Repeat the complete raw-input-to-diagnostic workflow on Gadi and record its
   validation. Package the selected numerical outputs and provenance as a
   versioned download with checksums, then link it from the results page.

GitHub catalogue validation checks presentation and file references. It must not
be presented as a scientific execution test. Credit Russell et al. (2018), the
recipe contributors, MOPPy developers, ACCESS model teams and CMIP data providers.
