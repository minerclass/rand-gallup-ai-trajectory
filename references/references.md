# References

Full citations for every data source behind the dashboard. APA 7th edition.

## RAND American Educator Panel reports (trend points)

Diliberti, M. K., Schwartz, H. L., Doan, S., Shapiro, A., Rainey, L. R., & Lake, R. J. (2024).
*Using artificial intelligence tools in K–12 classrooms.* RAND Corporation.
https://www.rand.org/pubs/research_reports/RRA956-21.html  *(Fall 2023 teacher AI use ≈ 18%)*

Kaufman, J. H., Woo, A., Eagan, J., Lee, S., & Kassan, E. B. (2025). *Uneven adoption of
artificial intelligence tools among U.S. teachers and principals in the 2023–2024 school year.*
RAND Corporation. https://www.rand.org/pubs/research_reports/RRA134-25.html
*(Spring 2024 AIRS teacher AI use ≈ 25%)*

Doss, C. J., Bozick, R., Schwartz, H. L., Chu, L., Rainey, L. R., Woo, A., Reich, J., &
Dukes, J. (2025). *AI use in schools is quickly increasing but guidance lags behind: Findings
from the RAND Survey Panels.* RAND Corporation.
https://www.rand.org/pubs/research_reports/RRA4180-1.html  *(Spring 2025 teacher AI use ≈ 53%)*

## RAND/Gallup American Teacher Panel public-use files (author analysis)

RAND American Educator Panels. (2025). *Spring 2025 American Teacher Panel Survey on Teacher
Satisfaction and Resources* [Public-use data file; GAL0425T]. RAND Corporation / Gallup.

RAND American Educator Panels. (2025). *Fall 2025 American Teacher Panel Survey on Teacher
Careers and AI* [Public-use data file; GAL1025T]. RAND Corporation / Gallup.

RAND American Educator Panels. (2026). *Winter 2026 American Teacher Panel Survey on Teacher
Expectations and Responsibilities* [Public-use data file; GAL0226T]. RAND Corporation / Gallup.

> Public-use files accessed via the RAND Survey Panels Data Portal
> (https://www.rand.org/education-employment-infrastructure/survey-panels/aep/access-data.html).
> Estimates computed by the author using the public `PORTAL_WEIGHT`; they may differ from RAND's
> published figures, which use non-public weights.

## NCES School Pulse Panel

U.S. Department of Education, Institute of Education Sciences, National Center for Education
Statistics. (2024). *School Pulse Panel 2024–25, December 2024 technology and digital literacy
data release.* https://nces.ed.gov/surveys/spp/  *(Written student AI policy; AI instruction by
school neighborhood poverty)*

## Codebook / variable notes

Per-wave variable inventories and the friction-dimension mapping live in the dissertation's
secondary-data folder (`Secondary_Data_for_Dissertation/`), not in this public repo. Key
constructs used here:

- **Adoption** — `AI_USER` (GAL1025T); RAND report headline rates for 2023–2025.
- **Policy presence** — `AI_POLICY` (GAL1025T); `AI_POLICY_STUDENT` (GAL0226T); SPP written policy.
- **Policy clarity / clear-policy coverage** — `AI_POLICY_CLEAR*` combined with presence.
- **Perceived effect** — `AI_EASY_DIFF_TEACHER`, `AI_EASY_DIFF_STUDENT` (GAL1025T).
- **Resource equity** — `QUAL_AI_TOOLS` × `SCHOOLETHNICCOMPOSITION` (GAL0425T).
