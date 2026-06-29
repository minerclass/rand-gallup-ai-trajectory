# Data access and reproduction

## Why the raw microdata are not in this repository

The teacher-level files analyzed here (`GAL0226T`, `GAL1025T`, `GAL0425T`) are **RAND public-use
files** distributed through the RAND Survey Panels Data Portal. They are free, but access is
**gated by individual registration and a data-use agreement**. Redistributing the raw
respondent-level files in a public repository would violate those terms. This repository
therefore publishes only **derived aggregate estimates** (weighted percentages), the analysis
code, and documentation — never the raw `.csv`/`.dta` microdata.

Aggregate, non-identifiable estimates of the kind in `results/` are standard scholarly output
and are safe to publish.

## How to obtain the files

1. Register for the RAND American Educator Panels Data Portal with an institutional email:
   <https://www.rand.org/education-employment-infrastructure/survey-panels/aep/access-data.html>
2. Download the public-use file for each wave you want to reproduce:
   - `GAL0226T` — Winter 2026 ATP Survey on Teacher Expectations and Responsibilities
   - `GAL1025T` — Fall 2025 ATP Survey on Teacher Careers and AI
   - `GAL0425T` — Spring 2025 ATP Survey on Teacher Satisfaction and Resources
3. The NCES School Pulse Panel December 2024 estimates are openly downloadable (no registration):
   <https://nces.ed.gov/surveys/spp/results.asp>

## Reproducing

Each script in `analysis/` expects the wave's public CSV at a relative `../raw/` path (matching
the dissertation's local data tree). Adjust the `DATA` path near the top of the script to point
at your downloaded copy, then:

```bash
python analysis/GAL1025T_weighted_descriptives.py
```

Output is written next to the script as `*_weighted_descriptive_results.csv`. Estimates use the
public `PORTAL_WEIGHT`; standard errors are approximate (Kish effective N) and understate the
full complex-survey design variance. The public portal weight differs from RAND's non-public
weight, so estimates may differ slightly from RAND's published figures and should be labeled a
public-portal analysis.

## A note on comparability

The waves use different instruments, question wordings, and (in some years) different teacher
subpopulations. Cross-wave comparisons are **convergent directional evidence**, not a single
longitudinal panel. Do not present them as equivalent measurements.
