"""GAL0425T (RAND Gallup, Apr 2025 - Satisfaction and Resources)
Weighted descriptive analysis for the dissertation secondary-data strand.

AI content is limited to resource adequacy: the QUALITY and QUANTITY of AI tools
available to teachers at their school (infrastructural friction). Unlike the other
two Gallup waves, the public file retains SCHOOL_LEVEL, URBANICITY, and
SCHOOLETHNICCOMPOSITION (a majority-students-of-color indicator), enabling a
limited equity-adjacent disaggregation.

All estimates use PORTAL_WEIGHT. Approximate SEs use the Kish effective N
(n_eff = (sum w)^2 / sum w^2); they understate complex-design variance and are
not used to assert significance.
"""
import csv
import math
from pathlib import Path

ANALYSIS_DIR = Path(__file__).resolve().parent
DATA = ANALYSIS_DIR.parent / "raw" / "GAL0425T_ATP_Portal.csv"
OUT = ANALYSIS_DIR / "GAL0425T_weighted_descriptive_results.csv"
WEIGHT = "PORTAL_WEIGHT"
NA = "Not applicable to my role/classroom"


def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            try:
                row[WEIGHT] = float(row[WEIGHT])
            except (TypeError, ValueError):
                row[WEIGHT] = None
            rows.append(row)
    return rows


def wpct(rows, col, hit_values, denom_values):
    sw = swh = sw2 = 0.0
    n = 0
    for r in rows:
        w = r[WEIGHT]
        v = r.get(col)
        if w is None or v not in denom_values:
            continue
        n += 1
        sw += w
        sw2 += w * w
        if v in hit_values:
            swh += w
    if sw == 0:
        return n, None, None
    p = swh / sw
    n_eff = (sw * sw) / sw2 if sw2 else 0.0
    se = math.sqrt(p * (1 - p) / n_eff) if n_eff > 0 else None
    return n, round(100 * p, 1), (round(100 * se, 1) if se is not None else None)


def main():
    rows = load(DATA)
    results = []

    def add(section, measure, n, pct, se, denom):
        results.append({"section": section, "measure": measure,
                        "unweighted_n": n, "weighted_percent": pct,
                        "approx_se_pp": se, "denominator": denom})

    qual_denom = {"Very high quality", "Somewhat high quality",
                  "Somewhat low quality", "Very low quality"}
    qual_hi = {"Very high quality", "Somewhat high quality"}
    qual_lo = {"Somewhat low quality", "Very low quality"}
    quant_denom = {"Not enough", "The right amount", "More than enough"}

    # --- A. AI-tool QUALITY (among those for whom AI tools apply) ---
    for hit, name in [(qual_hi, "High quality (very/somewhat)"),
                      (qual_lo, "Low quality (somewhat/very)"),
                      ({"Very high quality"}, "Very high quality"),
                      ({"Very low quality"}, "Very low quality")]:
        n, p, se = wpct(rows, "QUAL_AI_TOOLS", hit, qual_denom)
        add("A. Quality of available AI tools", name, n, p, se,
            "teachers for whom AI tools apply (excl. N/A)")

    # --- B. AI-tool QUANTITY ---
    for hit, name in [({"Not enough"}, "Not enough"),
                      ({"The right amount"}, "The right amount"),
                      ({"More than enough"}, "More than enough")]:
        n, p, se = wpct(rows, "QUANT_AI_TOOLS", hit, quant_denom)
        add("B. Quantity of available AI tools", name, n, p, se,
            "teachers for whom AI tools apply (excl. N/A)")

    # --- C. "Not applicable" share (AI tools not relevant to role) ---
    na_denom_qual = qual_denom | {NA}
    na_denom_quant = quant_denom | {NA}
    n, p, se = wpct(rows, "QUAL_AI_TOOLS", {NA}, na_denom_qual)
    add("C. AI tools not applicable to role", "Quality item | N/A", n, p, se,
        "all valid responses incl. N/A")
    n, p, se = wpct(rows, "QUANT_AI_TOOLS", {NA}, na_denom_quant)
    add("C. AI tools not applicable to role", "Quantity item | N/A", n, p, se,
        "all valid responses incl. N/A")

    # --- D. Subgroup disaggregation (this wave's added value) ---
    def subgroup(section, col, hit, denom, name, gcol, gvals):
        for gv in gvals:
            sub = [r for r in rows if r.get(gcol) == gv]
            n, p, se = wpct(sub, col, hit, denom)
            add(section, f"{name} | {gv}", n, p, se, f"valid within {gcol}")

    levels = ["Elementary", "Middle", "High"]
    urban = ["Urban", "Suburban", "Town/Rural"]
    ethnic = ["Majority Students of Color", "Majority White Students"]

    subgroup("D1. 'Not enough' AI tools, by school level", "QUANT_AI_TOOLS",
             {"Not enough"}, quant_denom, "Not enough", "SCHOOL_LEVEL", levels)
    subgroup("D2. 'Not enough' AI tools, by urbanicity", "QUANT_AI_TOOLS",
             {"Not enough"}, quant_denom, "Not enough", "URBANICITY", urban)
    subgroup("D3. 'Not enough' AI tools, by school ethnic composition",
             "QUANT_AI_TOOLS", {"Not enough"}, quant_denom, "Not enough",
             "SCHOOLETHNICCOMPOSITION", ethnic)
    subgroup("D4. High-quality AI tools, by school ethnic composition",
             "QUAL_AI_TOOLS", qual_hi, qual_denom, "High quality",
             "SCHOOLETHNICCOMPOSITION", ethnic)

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["section", "measure", "unweighted_n",
                                          "weighted_percent", "approx_se_pp",
                                          "denominator"])
        w.writeheader()
        w.writerows(results)

    print(f"Wrote {OUT}  ({len(results)} rows, N={len(rows)} respondents)")
    cur = None
    for r in results:
        if r["section"] != cur:
            cur = r["section"]
            print(f"\n## {cur}")
        se = f" +/-{r['approx_se_pp']}" if r["approx_se_pp"] is not None else ""
        print(f"  {r['measure']}: {r['weighted_percent']}%{se}  (n={r['unweighted_n']})")


if __name__ == "__main__":
    main()
