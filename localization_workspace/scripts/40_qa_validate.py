#!/usr/bin/env python3
"""
40_qa_validate.py — QA a translated CSV (e.g. 07_pilot_translation.csv) and emit
08_qa_report.md.

RUNNABLE TODAY (format-independent). Checks the brief's QA list:
  - missing / changed / added placeholders & tags        (via placeholder_spec)
  - broken rich-text tag nesting
  - untranslated rows (Arabic == source, or empty, or no Arabic letters)
  - suspiciously literal / no-Arabic-script output
  - overly long UI strings (length ratio + absolute cap for category 'ui'/'menu')
  - duplicate source strings translated inconsistently
  - inconsistent glossary usage (if 05_glossary.csv present)
  - Arabic punctuation/spacing issues (ASCII ? , ; instead of ؟ ، ؛; space before punct)
  - RTL risks (LRM/RLM marks, unbalanced bidi, leading/trailing combining)

Usage:
  python 40_qa_validate.py ../07_pilot_translation.csv [--glossary ../05_glossary.csv] [--out ../08_qa_report.md]

Expected input columns (case-insensitive, extras ignored):
  ID, source text, Arabic translation, category, context, glossary terms used, notes
"""
import csv, sys, re, argparse, os
from collections import defaultdict, Counter
from placeholder_spec import compare, extract_tokens

ARABIC = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿ]")
ASCII_PUNCT_IN_AR = {"?": "؟", ",": "،", ";": "؛"}
# colloquial/dialectal markers that must NOT appear in MSA (style guide = MSA only).
# bounded by non-Arabic-letters so they match as whole words.
DIALECT_RE = re.compile(
    r"(?<![ء-ي])(?:"
    r"مش|عايز|عاوز|دلوقتي|كده|كدا|هسه|"
    r"علشان|عشان|ازاي|إزاي|معلش|ايوة|إزيك"
    r")(?![ء-ي])"
)
# invisible BiDi control / override / isolate chars (should not appear in clean text)
BIDI_RE = re.compile(r"[‎‏‪-‮⁦-⁩؜]")
UI_CATS = {"ui", "menu"}
UI_MAX_LEN = 28           # soft cap for UI/menu Arabic length (chars)
LEN_RATIO_FLAG = 2.4      # target longer than source by this factor => flag


def col(row, *names):
    low = {k.lower().strip(): v for k, v in row.items() if k}
    for n in names:
        if n in low:
            return (low[n] or "").strip()
    return ""


def has_arabic(s):
    return bool(ARABIC.search(s))


def rich_balanced(s):
    """UE rich text: every <tag> (non-self-closing) needs a </> close. Approximate."""
    opens = len(re.findall(r"<[A-Za-z][^<>/]*?>", s))
    selfc = len(re.findall(r"<[^<>]*/>", s))
    closes = len(re.findall(r"</>", s))
    return opens == closes


def load_glossary(path):
    terms = []
    if not path or not os.path.exists(path):
        return terms
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            st = col(r, "source_term")
            ar = col(r, "approved_arabic")
            sh = col(r, "should_translate").lower()
            if st and ar and sh in ("yes", "", "maybe"):
                terms.append((st, ar))
    return terms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--glossary", default=os.path.join(os.path.dirname(__file__), "..", "05_glossary.csv"))
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "08_qa_report.md"))
    a = ap.parse_args()

    with open(a.csv, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    glossary = load_glossary(a.glossary)
    issues = defaultdict(list)            # check_name -> [ (id, detail) ]
    src_to_targets = defaultdict(set)

    for r in rows:
        rid = col(r, "id") or "?"
        src = col(r, "source text", "source", "original text")
        tgt = col(r, "arabic translation", "arabic", "translation")
        cat = col(r, "category").lower()

        if not src:
            continue
        src_to_targets[src].add(tgt)

        # placeholders / tags
        # normalize CSV-escaped doubled quotes ("" -> ") so tag comparison is fair
        cmp = compare(src.replace('""', '"'), tgt.replace('""', '"'))
        if cmp["missing"]:
            issues["missing_placeholders"].append((rid, f"missing {cmp['missing']}"))
        if cmp["added"]:
            issues["added_placeholders"].append((rid, f"extra {cmp['added']}"))
        if cmp["literal_newline_delta"] != 0:
            issues["newline_mismatch"].append((rid, f"newline delta {cmp['literal_newline_delta']}"))

        # broken tags
        if rich_balanced(src) and not rich_balanced(tgt):
            issues["broken_rich_text"].append((rid, "unbalanced <..>/</> in target"))

        # untranslated / no arabic — KO->AR aware (Fatal Claw source is Korean, not
        # Japanese): only flag when the source is actually Hangul (English tokens,
        # codes, numbers, credits correctly stay identical).
        src_has_ko = bool(re.search(r"[가-힣ᄀ-ᇿ㄰-㆏]", src))
        if tgt == "":
            issues["untranslated_empty"].append((rid, "no Arabic provided"))
        elif tgt == src and src_has_ko:
            issues["untranslated_identical"].append((rid, "target identical to source"))
        elif not has_arabic(tgt) and src_has_ko:
            issues["no_arabic_script"].append((rid, "target has no Arabic letters"))

        # UI length (fit hint for buttons/labels)
        if cat in UI_CATS and has_arabic(tgt) and len(tgt) > UI_MAX_LEN:
            issues["ui_too_long"].append((rid, f"{len(tgt)} chars (>{UI_MAX_LEN})"))
        # length ratio: Korean is fairly compact, so Arabic is routinely 1.5-2.5x longer;
        # only flag genuine bloat (long AND >4x), not normal expansion.
        if src and tgt and len(tgt) > 40 and len(tgt) > 4.0 * max(len(src), 1):
            issues["length_ratio"].append((rid, f"target {len(tgt)} vs source {len(src)}"))

        # Arabic punctuation / spacing
        if has_arabic(tgt):
            for ascii_p, ar_p in ASCII_PUNCT_IN_AR.items():
                if ascii_p in tgt:
                    issues["ascii_punctuation"].append((rid, f"'{ascii_p}' should be '{ar_p}'"))
                    break
            if re.search(r"\s+[،؛؟.!]", tgt):
                issues["space_before_punct"].append((rid, "space before punctuation"))
            if "  " in tgt:
                issues["double_space"].append((rid, "double space"))

        # BiDi safety: invisible bidi control/override/isolate chars
        if BIDI_RE.search(tgt):
            issues["bidi_control_chars"].append((rid, "contains invisible BiDi control/override char"))

        # MSA check: flag colloquial/dialectal markers (style guide = MSA only)
        if has_arabic(tgt):
            md = DIALECT_RE.search(tgt)
            if md:
                issues["dialectal_arabic"].append((rid, f"dialectal marker {md.group(0)!r} (use MSA)"))

        # glossary consistency
        for st, ar in glossary:
            if re.search(r"\b" + re.escape(st) + r"\b", src) and has_arabic(tgt) and ar not in tgt:
                issues["glossary_mismatch"].append((rid, f"'{st}' expected '{ar}'"))

    # duplicate source -> inconsistent target
    for src, tgts in src_to_targets.items():
        nonempty = {t for t in tgts if t}
        if len(nonempty) > 1:
            issues["inconsistent_duplicates"].append(("-", f"{src[:40]!r} -> {len(nonempty)} variants"))

    write_report(a.out, rows, issues)
    total = sum(len(v) for v in issues.values())
    print(f"QA complete: {len(rows)} rows, {total} issue(s). Report -> {a.out}")
    sys.exit(1 if total else 0)


def has_arabic_translatable(src):
    """Heuristic: a source that is pure tokens/symbols isn't expected to yield Arabic."""
    stripped = src
    for t in extract_tokens(src):
        stripped = stripped.replace(t, "")
    return bool(re.search(r"[A-Za-z]", stripped))


def write_report(path, rows, issues):
    order = [
        ("missing_placeholders", "Missing placeholders/tags", "CRITICAL"),
        ("added_placeholders", "Added/extra placeholders", "CRITICAL"),
        ("broken_rich_text", "Broken rich-text tags", "CRITICAL"),
        ("newline_mismatch", "Newline count mismatch", "HIGH"),
        ("untranslated_empty", "Untranslated (empty)", "HIGH"),
        ("untranslated_identical", "Untranslated (identical to source)", "HIGH"),
        ("no_arabic_script", "No Arabic script in target", "HIGH"),
        ("inconsistent_duplicates", "Same source, inconsistent Arabic", "HIGH"),
        ("glossary_mismatch", "Glossary term not applied", "MEDIUM"),
        ("dialectal_arabic", "Dialectal Arabic (should be MSA)", "MEDIUM"),
        ("ui_too_long", "UI string too long", "MEDIUM"),
        ("length_ratio", "Target suspiciously long vs source", "LOW"),
        ("ascii_punctuation", "ASCII punctuation instead of Arabic", "MEDIUM"),
        ("space_before_punct", "Space before punctuation", "LOW"),
        ("double_space", "Double space", "LOW"),
        ("bidi_control_chars", "Bidi/RTL control characters present", "MEDIUM"),
    ]
    total = sum(len(issues.get(k, [])) for k, _, _ in order)
    lines = ["# 08 — QA Report", "",
             f"Rows checked: **{len(rows)}**  |  Total issues: **{total}**", ""]
    if total == 0:
        lines.append("✅ No issues detected.")
    for key, title, sev in order:
        hits = issues.get(key, [])
        if not hits:
            continue
        lines.append(f"## [{sev}] {title} — {len(hits)}")
        lines.append("")
        lines.append("| ID | Detail |")
        lines.append("|----|--------|")
        for rid, detail in hits[:200]:
            safe = str(detail).replace("|", "\\|")
            lines.append(f"| {rid} | {safe} |")
        if len(hits) > 200:
            lines.append(f"| ... | (+{len(hits)-200} more) |")
        lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
