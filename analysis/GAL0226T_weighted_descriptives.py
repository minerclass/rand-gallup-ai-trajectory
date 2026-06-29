"""GAL0226T (RAND Gallup, Feb 2026 - Expectations & Responsibilities AI)
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
DATA = ANALYSIS_DIR.parent / "raw" / "GAL0226T_ATP_Portal.csv"
OUT = ANALYSIS_DIR / "GAL0226T_weighted_descriptive_results.csv"
WEIGHT = "PORTAL_WEIGHT"

BLANK = "Blank (no answer)"

# 10 instructional-task labels shared by AI_GUIDANCE* and AI_ENCOURAGE*
TASKS = {
    1: "Preparing to teach (planning lessons)",
    2: "Making worksheets/assignments/projects",
    3: "Making assessments/quizzes/exit tickets",
    4: "Modifying materials to meet student needs",
    5: "Grading / providing feedback",
    6: "Supplementing instruction (students use AI)",
    7: "One-on-one instruction / tutoring",
    8: "Analyzing student learning/achievement data",
    9: "Administrative work (paperwork, emails)",
    10: "Getting feedback/coaching on teaching",
}


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
    """Weighted % of hit_values among rows whose col is in denom_values."""
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
        results.append({
            "section": section, "measure": measure,
            "unweighted_n": n, "weighted_percent": pct,
            "approx_se_pp": se, "denominator": denom,
        })

    # --- A. Policy PRESENCE (infrastructural) ---
    presence_denom = {"Yes", "No", "I don't know"}
    for col, lab in [("AI_POLICY_TEACH", "Teacher AI use"),
                     ("AI_POLICY_STUDENT", "Student AI use"),
                     ("AI_POLICY_MISUSE", "Student AI misuse")]:
        for hit, name in [({"Yes"}, "Has policy (Yes)"),
                          ({"No"}, "No policy (No)"),
                          ({"I don't know"}, "Don't know if policy exists")]:
            n, p, se = wpct(rows, col, hit, presence_denom)
            add("A. Policy presence", f"{lab} | {name}", n, p, se,
                "valid responses (Yes/No/Don't know)")

    # --- B. Policy CLARITY (infrastructural; net-new construct) ---
    clear_denom = {"Not too clear or not clear at all", "Somewhat clear",
                   "Very clear", "Extremely clear"}
    clear_hi = {"Very clear", "Extremely clear"}
    for col, lab in [("AI_POLICY_CLEAR_TEACH", "Teacher AI use"),
                     ("AI_POLICY_CLEAR_STUDENT", "Student AI use"),
                     ("AI_POLICY_CLEAR_MISUSE", "Student AI misuse")]:
        n, p, se = wpct(rows, col, clear_hi, clear_denom)
        add("B. Policy clarity (among those with a policy)",
            f"{lab} | Clear (very/extremely)", n, p, se,
            "respondents whose school HAS a policy")

    # B2. Clear-policy COVERAGE: of all valid respondents, share with a policy
    #     that is also very/extremely clear (presence AND clarity together).
    pres_map = {"AI_POLICY_CLEAR_TEACH": "AI_POLICY_TEACH",
                "AI_POLICY_CLEAR_STUDENT": "AI_POLICY_STUDENT",
                "AI_POLICY_CLEAR_MISUSE": "AI_POLICY_MISUSE"}
    for clear_col, pres_col in pres_map.items():
        lab = {"AI_POLICY_TEACH": "Teacher AI use",
               "AI_POLICY_STUDENT": "Student AI use",
               "AI_POLICY_MISUSE": "Student AI misuse"}[pres_col]
        sw = swh = sw2 = 0.0
        n = 0
        for r in rows:
            w = r[WEIGHT]
            if w is None or r.get(pres_col) not in presence_denom:
                continue
            n += 1
            sw += w
            sw2 += w * w
            if r.get(clear_col) in clear_hi:
                swh += w
        p = 100 * swh / sw if sw else None
        n_eff = (sw * sw) / sw2 if sw2 else 0
        se = (100 * math.sqrt((swh / sw) * (1 - swh / sw) / n_eff)
              if sw and n_eff else None)
        add("B2. Clear-policy coverage (all valid respondents)",
            f"{lab} | Has a clear policy", n,
            round(p, 1) if p is not None else None,
            round(se, 1) if se is not None else None,
            "all valid policy-presence respondents")

    # --- C. GUIDANCE received by task (infrastructural) ---
    g_denom = {"Formal, written policy or official guidance",
               "Informal guidance (e.g., verbal guidance, shared norms, or expectations)",
               "No guidance"}
    g_any = {"Formal, written policy or official guidance",
             "Informal guidance (e.g., verbal guidance, shared norms, or expectations)"}
    g_formal = {"Formal, written policy or official guidance"}
    for i, task in TASKS.items():
        col = f"AI_GUIDANCE{i}"
        n, p, se = wpct(rows, col, g_any, g_denom)
        add("C. Any guidance received (by task)", task, n, p, se,
            "valid responses (excl. Not applicable/Blank)")
    for i, task in TASKS.items():
        col = f"AI_GUIDANCE{i}"
        n, p, se = wpct(rows, col, g_formal, g_denom)
        add("C2. Formal/written guidance (by task)", task, n, p, se,
            "valid responses (excl. Not applicable/Blank)")

    # --- D. School STANCE / encouragement by task (existential) ---
    e_denom = {"Encouraged", "Discouraged", "Neither encouraged nor discouraged"}
    for i, task in TASKS.items():
        col = f"AI_ENCOURAGE{i}"
        for hit, name in [({"Encouraged"}, "Encouraged"),
                          ({"Discouraged"}, "Discouraged"),
                          ({"Neither encouraged nor discouraged"}, "Neither")]:
            n, p, se = wpct(rows, col, hit, e_denom)
            add("D. School stance (among those who received guidance)",
                f"{task} | {name}", n, p, se,
                "respondents who received guidance for this use")

    # --- E. Subgroup disaggregation of headline indicators ---
    grade_vals = ["Elementary (PK - 5th)", "Middle School (6th - 8th)",
                  "High School (9th - 12th)"]
    subj_vals = ["Elementary, Special Education",
                 "Language Arts, ESL, non-English languages",
                 "Math and Computer Science", "Sciences, Health, CTE",
                 "Social Sciences, Arts and Music"]

    def subgroup(section, col, hit, denom, hit_name, group_col, group_vals):
        for gv in group_vals:
            sub = [r for r in rows if r.get(group_col) == gv]
            n, p, se = wpct(sub, col, hit, denom)
            add(section, f"{hit_name} | {gv}", n, p, se,
                f"valid responses within {group_col}")

    subgroup("E1. Student AI policy exists, by grade band", "AI_POLICY_STUDENT",
             {"Yes"}, presence_denom, "Has student AI policy",
             "GRADES_TAUGHT", grade_vals)
    subgroup("E2. Student AI policy exists, by subject", "AI_POLICY_STUDENT",
             {"Yes"}, presence_denom, "Has student AI policy",
             "MAIN_SUBJECT", subj_vals)
    subgroup("E3. Clear student AI policy (among policy-holders), by grade band",
             "AI_POLICY_CLEAR_STUDENT", clear_hi, clear_denom,
             "Clear student AI policy", "GRADES_TAUGHT", grade_vals)
    subgroup("E4. Any guidance on supplementing instruction (task 6), by grade band",
             "AI_GUIDANCE6", g_any, g_denom, "Any guidance (task 6)",
             "GRADES_TAUGHT", grade_vals)

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
        se = f" ±{r['approx_se_pp']}" if r["approx_se_pp"] is not None else ""
        print(f"  {r['measure']}: {r['weighted_percent']}%{se}  (n={r['unweighted_n']})")


if __name__ == "__main__":
    main()
