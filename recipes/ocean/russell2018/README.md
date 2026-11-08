# Russell et al. Southern Ocean diagnostics

These numbered notebooks cover the Southern Ocean winds, fronts, transport, sea ice, carbon flux, and uptake diagnostics assembled for Russell et al. (2018). Use the [gallery](../../../web/) to inspect each recipe's model and tool metadata.

## Completed ACCESS/CMIP comparison

The [joint comparison results](../../../web/results/russell-1986-2005/index.html)
show the updated ESMValTool diagnostics applied to ACCESS-OM3, ACCESS-CM3 and
selected CMIP6/CMIP7 models over 1986–2005. There are 35 plots across 16 diagnostic
groups, with OM3 in 14 groups and CM3 in eight. All 85 CMIP baseline numerical
comparisons passed. CM3 is a present-day control, so its dates are model years.

This result set was produced from pinned ESMValTool scripts and audited MOPPy
CMORisation/preprocessing caches. It was not produced by rerunning the numbered
notebooks in this folder. See [run scope and integration notes](comparison-results.md)
for provenance, coverage and the remaining workflow packaging work.
