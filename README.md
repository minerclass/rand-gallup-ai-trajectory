# RAND/Gallup teacher AI trajectory, 2023–2026

A weighted secondary-data trajectory of U.S. K–12 teacher artificial-intelligence
adoption, policy presence and clarity, perceived effects on learning, and equity gaps —
assembled as national structural context for a mixed-methods dissertation on **pedagogical
friction** and generative AI.

**Live dashboard:** `index.html` (publish via GitHub Pages → Settings ▸ Pages ▸ deploy from `main`, root).

## What this is — and is not

This is the **secondary-data / structural-context strand** of the dissertation. It situates the
study's bounded case within national patterns. It is **not** evidence from inside the bounded
case, and it does **not** measure pedagogical friction directly. The surveys were not designed
to capture noetic, rhetorical, existential, or infrastructural friction; their indicators are
read as proxies that frame the qualitative work.

Chapter placement: **Chapters 1 and 3** (problem urgency + documented quantitative baseline),
with reuse in the **Chapter 5** discussion. It is deliberately kept out of Chapter 4, which is
reserved for bounded-case findings.

## Headline findings

- **Adoption raced ahead of guardrails.** Teacher AI use rose ~18% (Fall 2023) → 25% (Spring
  2024) → 53% (Spring 2025) → **69% (2025–26)**.
- **Functional policy stalled near ~13%.** Across two independent waves, only ~12.5–12.8% of
  teachers report an AI policy that is also *clear* — far below the ~25–35% who report any
  policy *exists*. Policy presence overstates functional governance.
- **Easier for teachers, harder for students.** Teachers say AI makes their own job easier
  (72.5%) but makes students' learning **harder (61.9%)** — and the "harder" belief rises with
  grade band. This is the empirical face of the "unproductive success" argument.
- **The equity gap repeats.** Schools serving majority students of color report lower-quality
  AI tools (71.3% vs. 80.8%); the NCES School Pulse Panel shows a parallel poverty gap in AI
  instruction (39% vs. 49%). Two independent datasets, same direction.

## Data sources

| Source | Wave | Role |
|---|---|---|
| RAND American Teacher Panel | Fall 2023 (RRA956-21) | Adoption trend point |
| RAND AIRS | Spring 2024 (RRA134-25) | Adoption trend point |
| RAND American Teacher Panel | Spring 2025 (RRA4180-1) | Adoption trend point |
| RAND/Gallup ATP `GAL0425T` | Apr 2025 | AI-tool resource adequacy + equity (author analysis) |
| RAND/Gallup ATP `GAL1025T` | Oct 2025 | Adoption, policy clarity, perceived effects (author analysis) |
| RAND/Gallup ATP `GAL0226T` | Feb 2026 | Policy presence/clarity, guidance, stance (author analysis) |
| NCES School Pulse Panel | Dec 2024 | School-level policy + poverty equity context |

See [references/references.md](references/references.md) for full APA citations.

## Repository layout

```
index.html                         interactive dashboard (GitHub Pages)
analysis/                          reproducible weighted-descriptive scripts (pure Python)
results/                           derived aggregate estimates (safe to publish)
  key_indicators_2023_2026.csv     the figures behind the dashboard, with per-point sources
  GAL0226T/GAL1025T/GAL0425T_*.csv full weighted indicator tables
references/references.md           APA citations + codebook notes
DATA_ACCESS.md                     how to obtain the raw microdata and reproduce
AGENTS.md                          conventions + data/privacy boundaries for contributors/agents
```

## Reproducing the estimates

The raw RAND/Gallup public-use microdata are **not** included (see DATA_ACCESS.md for why).
After you register with RAND and download the public files, place each wave's CSV where the
script expects it and run:

```bash
python analysis/GAL1025T_weighted_descriptives.py
```

Scripts are dependency-free (Python standard library only) and use the public `PORTAL_WEIGHT`.

## License & attribution

Code and derived results in this repository: released for scholarly reuse with attribution.
The underlying survey data remain the property of RAND, Gallup, and NCES under their respective
terms of use. Cite both this repository and the original data sources.
