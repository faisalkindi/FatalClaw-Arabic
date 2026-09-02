# Fatal Claw — Batch Translation Brief

You are translating a slice of the Korean source corpus for **Fatal Claw** (2D Metroidvania, dev NDEV GAMES/Com2uS, Korean) into Modern Standard Arabic. Full project context lives in this same directory (`00_file_audit.md`, `04_game_context.md`, `05_glossary.csv`, `06_arabic_style_guide.md`) — read `04_game_context.md`, `05_glossary.csv`, and `06_arabic_style_guide.md` in full before starting; they are short. This brief pulls out what you need to act, but those files are the source of truth if anything conflicts.

## Source language
**Korean is the source** (`source_ko` field). `ref_ja`/`ref_en` are cross-reference only — use `ref_en` to resolve gender/referents Korean drops (Rule 0 Case-B), never translate from it directly. Korean speech-levels (formal/informal) are grammatical, not honorific suffixes like Japanese — carry the register through Arabic word choice, not transliterated address terms.

## Register (LOCKED — do not deviate)
Elevated-but-readable Modern Standard Arabic (فصحى راقية مقروءة), calibrated per context:
- **Dialogue** — voice varies by speaker; consult `04_game_context.md`'s NPC gender/bio table for who's who. Cain (already translated, see `07_pilot_translation.csv` for the locked voice) is grave/clipped/soldierly; other NPCs may be warmer per their bios — don't force Cain's clipped tone onto every character.
- **Cinematic/divine content** — more archaic/liturgical (see the opening cinematic in `07_pilot_translation.csv` for the calibration).
- **UI** — plain, concise, imperative/interrogative (هل تريد...؟ for confirmations).
- **Item/Skill/Journal descriptions** — descriptive, lore-book tone, 3rd person.

## Hard rules (never violate)
1. **Preserve every placeholder/tag byte-for-byte, same count and order:** `\n` (real newline), `<c0>`/`<c1>`/`<c2>`/`<c3>` + `</>` (color tags), `<img id="PC.Num_N"/>` (icon), `{0}`-`{4}` (format args). Never translate, reorder, or drop these.
2. **Never translate the `id`/key.**
3. Western digits (0-9) only, never Eastern Arabic-Indic (٠-٩).
4. Arabic punctuation: `،` `؛` `؟` — never ASCII `,` `;` `?`. Single `…` for ellipsis (collapse any longer run). `؟` only for genuine questions.
5. **MSA only — no dialect.** No Gulf/Egyptian/Levantine colloquialisms.
6. **Hard "G" sound in transliterated names → ق, never غ.** (غ only for genuine Arabic غ words or true "gh" sounds.) Foreign "V" → ڤ.
7. Light harakat only: shadda where meaning-bearing; skip most short vowels unless a word would be misread. Not full vocalization.
8. **Names/terms already in `05_glossary.csv` with `resolved_pilot` status are FROZEN — use them exactly, do not re-decide.** If you need a name/term NOT in the glossary, transliterate/translate using the same conventions (rule 6, hard-G etc.), and flag it in your notes column as a new term for glossary review — don't invent silently.
9. If a line's meaning is genuinely unclear without more scene context, translate your best version and add a note — never leave it blank, never guess wildly.

## Gender
Consult `04_game_context.md`'s NPC gender table. Kisha = masculine. Speaker gender is usually derivable from the `id` (e.g. `Npc_<Name>/...`). For unresolved NPCs (Cabo/Carbo, Ratio, Kuro, Ordo, Deserter, Arcadia, EXODUS) default to masculine grammatical agreement and flag in notes — don't block on it.

## Task
1. Read your assigned batch file: `batches/<BATCH>.jsonl` (one JSON object per line: `id`, `ftext_key`, `category`, `source_ko`, `ref_ja`, `ref_en`).
2. Translate every row's `source_ko` into Arabic per the rules above.
3. Write output to `batches/<BATCH>_translated.csv` with columns: `id,source text,arabic translation,category,ref_en,notes` (notes = new-term flags or uncertainty flags, empty otherwise). Use Python's `csv` module with `encoding='utf-8'` — do not hand-format CSV (quoting/escaping will break).
4. Run the QA validator: `python scripts/40_qa_validate.py batches/<BATCH>_translated.csv --out batches/<BATCH>_qa.md` (run from the `localization_workspace` directory). Read the report. Fix every issue it flags (placeholder mismatches, empty rows, dialectal markers, ASCII punctuation, etc.) and re-run until it reports 0 issues, or until remaining issues are false positives you can justify in your final report (e.g. a deliberately short UI label flagged by the length heuristic).
5. Report back: row count translated, final QA issue count (should be 0), any new glossary terms you flagged, any rows you couldn't confidently translate and why.

Work directory: `C:\Users\Faisal\Ai\Mods Dev\FatalClaw\localization_workspace`
