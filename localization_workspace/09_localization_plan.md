# Localization Plan — Fatal Claw

## Route decision (per master doc's "choose production route" table)
**Small full game** (3,559 rows total, ~1,150 of which are per-NPC dialogue with speaker already known from the key). This is well under the corpus size that justifies standing up local-vLLM bulk infra. Recommended route: **direct context-rich primary translation** (Gemini or Claude subagents, scene/NPC-batched) — same shape as Elliot/Octopath's pilot-then-batch approach, not the FFX/Octopath vLLM-bulk pipeline. Keep every downstream gate (editorial pass, verify pass, human approval, in-game QA) regardless of route, per the master doc's invariant.

## Status vs the 7 foundation artifacts
1. File audit — **done** (`00_file_audit.md`)
2. Source corpus — **done**, `01_extracted_strings.jsonl`, 3,559 rows, KO/JA/EN merged by key, 100% KO coverage
3. Game-context file — **done, provisional** (`04_game_context.md`) — NPC genders and honorific inventory still open
4. Glossary — **skeleton done** (`05_glossary.csv`), 27 terms, all Arabic columns empty pending pilot arbitration
5. Style guide — **done, provisional** (`06_arabic_style_guide.md`) — register unlocked, Korean-honorific research pending
6. QA validator — **not built yet** — port Elliot's `40_qa_validate.py` + `placeholder_spec.py`, adapt to this corpus's placeholder syntax (needs checking — not yet surveyed)
7. Enforcement package — **not built yet** — depends on 3/4/5 being locked first

## Before the pilot (blocking) — STATUS
1. **DONE.** NPC gender resolved for 27/29 named roster via EN-locres pronoun cross-reference (Rule 0 Case-B) — no wiki exists for this game yet, so mined directly from `Journal_DESC_System/NPC_*` bios + dialogue/achievement text. See `04_game_context.md`. Still unresolved (flagged, not guessed): Cabo/Carbo, Ratio, Kuro, Ordo, Deserter, Arcadia, EXODUS — no self-referential pronoun found anywhere in the corpus for these; will need a deeper dialogue-tree grep or store/trailer art check when their scenes come up.
2. **DONE.** Korean honorific/speech-level research completed (Exa: Locpick, INLINGO, SandVox, Ulatus guides) — see `06_arabic_style_guide.md`. Key finding: Korean speech-levels are grammatical (verb endings/particles), not honorific suffixes like Japanese — mapped to Arabic register-per-character-card instead of a suffix convention. Two kinship address terms already found in-corpus (오빠/형) confirmed to translate by meaning, not transliterate.
3. **DONE (default set, owner-overridable).** "Fatal Claw" → translate, candidate المخلب القاتل, logged in `05_glossary.csv` with reasoning (matches FFT's "Ivalice Chronicles"→سجلات إيفاليس precedent: generic word translates, only true proper nouns transliterate). Owner can override in the pilot.
4. **DONE.** Placeholder/tag inventory surveyed — small familiar set (`\n`, `<c0-3>`/`</>`, `<img id="PC.Num_N"/>`, `{0}-{4}`), no printf tokens. Documented in `00_file_audit.md`.
5. **ARTIFACT READY, awaiting owner in-game test.** Built `culture_test/FatalClawArabicTest_P.pak` — a loose unencrypted pak adding a new `ar` locale with 8 marker rows (opening-cinematic lines), byte-verified round-trip via repak+UnrealLocres. See `culture_test/README_TEST.md` for the drop-in test steps. I don't launch/control the game myself (standing convention across every prior project) — this is the one blocker whose final resolution needs your hands on the machine.

## QA validator — DONE
Ported Elliot's `40_qa_validate.py` + `placeholder_spec.py` to `scripts/`, adapted the source-language detection from Japanese-script to Hangul (KO→AR aware, not JA→AR). Smoke-tested against 20 real corpus rows — runs clean, correctly flags empty/untranslated rows. `placeholder_spec.py`'s token grammar needed no changes — Fatal Claw's tag set (`<c0-3>`, `</>`, `<img id="..."/>`, `{0}-{4}`) is already covered by the existing UE rich-text/ICU-arg patterns.

## Pilot — DONE, awaiting owner review (mandatory gate before scaling)
152 lines translated: full Cain bucket (65), CommonInterface (30), Item (25), Skill (20), opening Cinematic (12). Output: `07_pilot_translation.csv`. QA validator run clean (0 issues after 2 fixes — a newline-count mismatch and a double-space, both in `GUIDE_DEMO_CHINAJOY_ENDING`, now fixed). Register locked (see `06_arabic_style_guide.md`). Glossary updated with 20 new resolved terms + 2 corrected Korean readings (Jayma: 제이마 not 자이마; Examu: 엑사무 not 에그자무) discovered during translation — the earlier lore-post-derived readings in the original glossary draft were wrong, corpus is now the source of truth.

**This is a gate, not a formality — per the methodology, pilot output may not establish tone/terminology until it passes human review.** I have not self-approved this; it needs your read before any batch scales. Flag anything that reads wrong and I'll fix it and re-run QA before continuing.

## Batch order (once pilot is locked)
0. Pilot (~300 mixed)
1. CommonInterface + InputRebind (391) — UI verbs, freeze early
2. Journal_DESC_System/Kisha/Quote (325) + LogBook (97) — fixed phrasings, feeds glossary
3. Item (187) + Skill/SkillTree (155) + MonsterNames (102) + RegionName (101) + ObjectName (31) + DocumentedStone (45) — terminology-heavy
4. NpcNames (62) — should already be resolved by glossary at this point
5. Dialogue — Cinematic (132) + NarrativeScene (80) + Prologue (15) + ST_NPC_Event (354) + ST_Npc_Kuro (19), sub-batched by scene; then the 29 named-NPC buckets (~1,150 rows), each NPC batched together (speaker known from key, register locked per-character from lore/sample)
6. Shop_Ainjaff (10) + any leftover/uncertain rows

## Not yet done — explicitly deferred
- QA validator script
- Enforcement package (machine-readable glossary/character-cards/scenes/style-rules + batch compiler)
- Font swap build (SST Arabic Medium → `.ufont`)
- RTL flag / culture-slot delivery test in-engine
- Any DataTable/widget work (needs engine-version confirmation + usmap first)
