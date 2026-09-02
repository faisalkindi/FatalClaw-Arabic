# -*- coding: utf-8 -*-
"""
merge_and_build.py — merge all translated batch CSVs + the pilot into one
master 10_arabic_translation.jsonl, cross-check coverage against
01_extracted_strings.jsonl, then build the final ar-locale Game.locres
and pack it into a deployable loose pak.

Run from localization_workspace/scripts/.
"""
import json, csv, glob, os, sys, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_master_corpus():
    path = os.path.join(ROOT, "01_extracted_strings.jsonl")
    return {json.loads(l)["id"]: json.loads(l) for l in open(path, encoding="utf-8")}


def load_translations():
    ar = {}
    notes = {}
    # pilot
    pilot = os.path.join(ROOT, "07_pilot_translation.csv")
    with open(pilot, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            ar[r["id"]] = r.get("arabic translation", "")
    # all batch outputs
    for path in glob.glob(os.path.join(ROOT, "batches", "*_translated.csv")):
        with open(path, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                rid = r.get("id")
                if not rid:
                    continue
                ar[rid] = r.get("arabic translation", "")
                n = r.get("notes", "")
                if n:
                    notes[rid] = n
    return ar, notes


def main():
    corpus = load_master_corpus()
    ar, notes = load_translations()

    missing = [k for k in corpus if k not in ar or not ar[k]]
    extra = [k for k in ar if k not in corpus]

    print(f"corpus rows: {len(corpus)}")
    print(f"translated rows: {len(ar)}")
    print(f"missing (in corpus, no translation): {len(missing)}")
    print(f"extra (translated but not in corpus - stale?): {len(extra)}")
    if missing:
        print("First 20 missing:")
        for m in missing[:20]:
            print(" ", m)
    if extra:
        print("First 20 extra:")
        for e in extra[:20]:
            print(" ", e)

    # write master translation jsonl
    out_path = os.path.join(ROOT, "10_arabic_translation.jsonl")
    with open(out_path, "w", encoding="utf-8") as f:
        for rid, row in corpus.items():
            f.write(json.dumps({
                "id": rid,
                "source_ko": row["source_ko"],
                "arabic": ar.get(rid, ""),
                "category": row["category"],
                "notes": notes.get(rid, ""),
            }, ensure_ascii=False) + "\n")
    print(f"wrote {out_path}")

    # write flat CSV for the QA validator + for UnrealLocres import
    csv_path = os.path.join(ROOT, "10_arabic_translation.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "source", "target"])
        for rid, row in corpus.items():
            w.writerow([rid, row["source_ko"], ar.get(rid, "")])
    print(f"wrote {csv_path}")

    return len(missing) == 0


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
