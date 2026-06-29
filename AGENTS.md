# AGENTS.md — rand-gallup-ai-trajectory

Conventions and guardrails for contributors and AI agents working in this repository.

## Purpose

Public-facing **secondary-data companion** for Micah Miner's NLU EdD dissertation on
pedagogical friction and generative AI. It presents a weighted 2023–2026 trajectory of U.S.
teacher AI indicators as national structural context. Part of the `minerclass` dissertation
GitHub ecosystem (sibling sites: `dissertation-overview`, `genAI-ML-pedagogy-of-friction-site`,
`quantitative-measures-studio`).

## Public / private boundaries

This repo is **public-facing**. Classify every file before committing:

- **Safe to publish:** `index.html`, analysis scripts, derived aggregate estimates in
  `results/`, references, this file.
- **Never commit:** raw RAND/Gallup public-use microdata (`*.csv`/`*.dta` respondent records),
  any RAND portal credentials, student/staff/participant data, interview transcripts, tokens,
  or private Google Drive links. The raw microdata are under a RAND data-use agreement — see
  `DATA_ACCESS.md`. The `.gitignore` blocks `raw/` and data extensions as a backstop.

## Canonical terminology

Keep aligned with the dissertation hubs. Key terms: **pedagogical friction** (noetic,
rhetorical, existential, infrastructural dimensions); **unproductive success**; **structural
context** (not "findings"). Secondary data is always *context*, never bounded-case evidence.
Do not imply causal effects or learning outcomes from these descriptive estimates.

## Data and analysis rules

- All estimates weighted with the public `PORTAL_WEIGHT`; label as public-portal analysis.
- Cross-wave numbers are **convergent directional evidence**, not a longitudinal panel — state
  this wherever waves are compared.
- Round every displayed number. Standard errors are approximate (Kish effective N).
- Do not fabricate citations, figures, or page numbers. Every dashboard number traces to
  `results/key_indicators_2023_2026.csv` with a source column.

## Deployment

GitHub Pages from `main`, root. `index.html` is self-contained (Chart.js via cdnjs CDN; no
build step). After publishing, verify the live URL renders in both light and dark mode.

## Change format

When reporting changes, use: **Summary / Files changed / Validation / Notes or risks.**
Keep changes small and focused. Verify the live Pages site, not just local files.

## Manual validation checklist

- [ ] Dashboard renders; chart + both custom panels populate.
- [ ] Light and dark mode both legible.
- [ ] No raw microdata staged (`git status` clean of `raw/`, `.dta`, large `.csv`).
- [ ] Every changed number still matches `results/`.
- [ ] Source/method footnotes intact.
