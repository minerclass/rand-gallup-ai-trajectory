"""GAL1025T (RAND Gallup, Oct 2025 - Teacher Careers and AI)
Weighted descriptive analysis for the dissertation secondary-data strand.

Pure-Python (csv module): the public portal CSV stores value LABELS directly,
and MAIN_SUBJECT contains embedded commas, so csv.DictReader is required.

All estimates use PORTAL_WEIGHT. Approximate standard errors use the Kish
effective sample size n_eff = (sum w)^2 / sum(w^2); SE = sqrt(p(1-p)/n_eff).
These are approximate: the single public portal weight does not carry the full
complex-design / replicate-weight information, so SEs understate true variance
and significance tests are not asserted.
"""
import csv
import math
from pathlib import Path

ANALYSIS_DIR = Path(__file__).resolve().parent
DATA = ANALYSIS_DIR.parent / "raw" / "GAL1025T_ATP_Portal.csv"
OUT = ANALYSIS_DIR / "GAL1025T_weighted_descriptive_results.csv"
WEIGHT = "PORTAL_WEIGHT"


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

    # --- A. AI adoption (noetic/behavioral proxy) ---
    user_denom = {"Yes", "No"}
    n, p, se = wpct(rows, "AI_USER", {"Yes"}, user_denom)
    add("A. AI adoption", "Used AI tools in 2025-26", n, p, se,
        "valid Yes/No responses")
    freq_denom = {"Daily", "Weekly", "Monthly", "Never to once every few months"}
    for hit, name in [({"Daily"}, "Daily"), ({"Weekly"}, "Weekly"),
                      ({"Monthly"}, "Monthly"),
                      ({"Never to once every few months"}, "Less than monthly"),
                      ({"Daily", "Weekly"}, "Weekly or more often")]:
        n, p, se = wpct(rows, "AI_USER_FREQ", hit, freq_denom)
        add("A2. AI use frequency (among users)", name, n, p, se,
            "respondents who used AI this year")

    # --- B. Policy presence + clarity (infrastructural) ---
    pres_denom = {"Yes", "No", "I don't know"}
    for hit, name in [({"Yes"}, "Has AI policy (Yes)"), ({"No"}, "No AI policy"),
                      ({"I don't know"}, "Don't know if policy exists")]:
        n, p, se = wpct(rows, "AI_POLICY", hit, pres_denom)
        add("B. AI policy presence", name, n, p, se,
            "valid responses (Yes/No/Don't know)")
    clear_denom = {"Not clear at all", "Not too clear", "Somewhat clear",
                   "Very clear", "Extremely clear"}
    clear_hi = {"Very clear", "Extremely clear"}
    n, p, se = wpct(rows, "AI_POLICY_CLEAR", clear_hi, clear_denom)
    add("B2. Policy clarity", "Clear (very/extremely), among policy-holders",
        n, p, se, "respondents whose school HAS an AI policy")
    # clear-policy coverage among all valid presence respondents
    sw = swh = sw2 = 0.0
    n = 0
    for r in rows:
        w = r[WEIGHT]
        if w is None or r.get("AI_POLICY") not in pres_denom:
            continue
        n += 1
        sw += w
        sw2 += w * w
        if r.get("AI_POLICY_CLEAR") in clear_hi:
            swh += w
    p = 100 * swh / sw if sw else None
    n_eff = (sw * sw) / sw2 if sw2 else 0
    se = 100 * math.sqrt((swh / sw) * (1 - swh / sw) / n_eff) if sw and n_eff else None
    add("B2. Policy clarity", "Clear-policy coverage (all valid respondents)",
        n, round(p, 1) if p else None, round(se, 1) if se else None,
        "all valid policy-presence respondents")

    # --- C. Perceived effect on ease/difficulty: teacher vs student ---
    ed_denom = {"AI will make the job much easier", "AI will make the job somewhat easier",
                "AI will have no effect on ease/difficulty of the job",
                "AI will make the job somewhat harder", "AI will make the job much harder"}
    ed_easier = {"AI will make the job much easier", "AI will make the job somewhat easier"}
    ed_harder = {"AI will make the job somewhat harder", "AI will make the job much harder"}
    ed_none = {"AI will have no effect on ease/difficulty of the job"}
    for col, who in [("AI_EASY_DIFF_TEACHER", "Teachers' job"),
                     ("AI_EASY_DIFF_STUDENT", "Students' learning")]:
        for hit, name in [(ed_easier, "Easier"), (ed_none, "No effect"),
                          (ed_harder, "Harder")]:
            n, p, se = wpct(rows, col, hit, ed_denom)
            add("C. Perceived effect of AI (easier vs harder)",
                f"{who} | {name}", n, p, se, "valid responses")

    # --- D. Support: personal vs school ---
    sup1_denom = {"Strongly support", "Somewhat support", "Neither support nor oppose",
                  "Somewhat oppose", "Strongly oppose"}
    sup2_denom = sup1_denom | {"Don't know"}
    sup_yes = {"Strongly support", "Somewhat support"}
    sup_no = {"Somewhat oppose", "Strongly oppose"}
    for col, who, denom in [("AI_SUPPORT1", "Personal support", sup1_denom),
                            ("AI_SUPPORT2", "School support", sup2_denom)]:
        for hit, name in [(sup_yes, "Support"), ({"Neither support nor oppose"}, "Neither"),
                          (sup_no, "Oppose")]:
            n, p, se = wpct(rows, col, hit, denom)
            add("D. Support for teachers using AI", f"{who} | {name}", n, p, se,
                "valid responses")
    n, p, se = wpct(rows, "AI_SUPPORT2", {"Don't know"}, sup2_denom)
    add("D. Support for teachers using AI", "School support | Don't know", n, p, se,
        "valid responses")

    # --- E. Pace of adoption ---
    pace_denom = {"Too fast", "The right pace", "Too slow", "I don't know"}
    for hit, name in [({"Too fast"}, "Too fast"), ({"The right pace"}, "Right pace"),
                      ({"Too slow"}, "Too slow"), ({"I don't know"}, "Don't know")]:
        n, p, se = wpct(rows, "AI_PACE_SCHOOL", hit, pace_denom)
        add("E. Opinion on pace of AI adoption", name, n, p, se, "valid responses")

    # --- F. Subgroup disaggregation ---
    grade_vals = ["Elementary (PK - 5th)", "Middle School (6th - 8th)",
                  "High School (9th - 12th)"]
    subj_vals = ["Elementary, Special Education",
                 "Language Arts, ESL, non-English languages",
                 "Math and Computer Science", "Sciences, Health, CTE",
                 "Social Sciences, Arts and Music"]

    def subgroup(section, col, hit, denom, name, gcol, gvals):
        for gv in gvals:
            sub = [r for r in rows if r.get(gcol) == gv]
            n, p, se = wpct(sub, col, hit, denom)
            add(section, f"{name} | {gv}", n, p, se, f"valid within {gcol}")

    subgroup("F1. AI use, by grade band", "AI_USER", {"Yes"}, user_denom,
             "Used AI", "GRADES_TAUGHT", grade_vals)
    subgroup("F2. AI use, by subject", "AI_USER", {"Yes"}, user_denom,
             "Used AI", "MAIN_SUBJECT", subj_vals)
    subgroup("F3. Believes AI makes students' learning HARDER, by grade band",
             "AI_EASY_DIFF_STUDENT", ed_harder, ed_denom, "AI makes learning harder",
             "GRADES_TAUGHT", grade_vals)
    subgroup("F4. School has AI policy, by grade band", "AI_POLICY", {"Yes"},
             pres_denom, "Has AI policy", "GRADES_TAUGHT", grade_vals)

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
