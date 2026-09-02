# Arabic Style Guide — Fatal Claw

Inherits every cross-project frozen default from `LOCALIZATION_METHODOLOGY.md`. This file only records what's specific to this game or still open.

## Source language (Rule 0)
**Korean is the source.** Translate KO→AR directly. JA and EN are QA cross-references only (both are themselves translations of the Korean — do not treat either as authoritative for meaning; do use EN for explicit-pronoun/gender cross-checks the way the methodology's Rule 0 Case-B describes, since Korean itself drops pronouns/gender constantly, same problem class as Japanese).

## Register — LOCKED in pilot (152 lines: full Cain bucket, UI, Item, Skill, opening Cinematic)
Confirmed **elevated-but-readable MSA**, calibrated per-context:
- **Cain (dialogue)** — grave, clipped, soldier's voice. Short sentences, heavy ellipsis for hesitation/rage, formal address collapsing into contempt ("أيّتها الدُّمية" - "you puppet"). Honorific 님 on Sorron's name → المولى (respectful "Master/Lord") while Cain still believes in him; kept even after disillusionment since Cain's own words don't drop it explicitly in this batch — revisit per-line if a scene shows him explicitly renouncing the title.
- **Cinematic (opening/divine council)** — more archaic/liturgical register than Cain's soldier voice: كلّ الآلهة addressing "the divine Examu" (المولى إكسامو), royal "We" register for the King/Examu's own lines ("أرغب"/"أراهن" rather than casual speech), Grande's closing line kept simple and tender by contrast (a blessing, not a decree) — deliberate register *contrast within the same scene*, confirms register must be tracked per-speaker/per-line, not just per-project.
- **UI (CommonInterface)** — plain, concise, imperative/interrogative as appropriate (هل تريد...؟ for confirmations, single-word imperatives for buttons: دخول/خروج/تبديل).
- **Item/Skill descriptions** — descriptive, slightly elevated (matches source's own lore-book tone), consistent 3rd-person explanatory voice.
This is now the frozen calibration — do not re-litigate per batch, only refine per-character voice notes as more NPCs are translated (e.g. lighter NPCs like Lara/Nia may warrant a warmer register within the same overall MSA elevation, same way Cain's soldier clip differs from the council's liturgical tone).

## Gender
- **Kisha = masculine** [SRC: store copy "his ancestors"]. Default 2nd-person address to player follows Kisha's gender per methodology default.
- All ~29 named NPC genders are **unresolved** — must be researched (character art/trailers) before the conversation-aware speaker/addressee pass, per the methodology's mandatory pre-translation gender resolution. Do not infer from name phonetics alone.

## Names / transliteration
- Standard house rule applies: **hard G → ق, never غ**; foreign V → ڤ if the target font supports it (SST Arabic Medium does).
- Character/place names: transliterate by default (Kisha→كيشا, Sorron→سورون, Enma→إنما or إنما depending on final vetted reading, Cain→كين — to be frozen in the pilot, not decided here).
- Descriptive compound place names (X Kingdom / X Tundra / X Quarry / X Dungeon) split per the methodology's existing pattern precedent (Trails' tower-naming logic): transliterate the proper element, translate the generic element (كingdom/tundra/quarry/dungeon word) — e.g. "Higasha Tundra" → توندرا هيغاشا or تندرا هيغاشا (freeze exact form in glossary).

## Everything else (frozen, inherited, do not re-decide)
Punctuation (، ؛ ؟ single …), Western digits, light harakat (shadda always, rare disambiguating vowel only), UI-verb glossary, forbidden-pattern list, placeholder/tag preservation, honorific-suffix convention IF Korean honorifics appear in source (Korean uses 님/씨/오빠-type address terms, not Japanese さん/様 — **flag this as a real difference from prior projects**: Korean honorific/address-term handling has no precedent in this house's prior JA-sourced projects and needs its own small research pass before the pilot, not a blind reuse of the -san/-sama suffix convention).

## Korean honorific / speech-level policy [RESEARCHED, verified via Exa — Locpick, INLINGO, SandVox, Ulatus Korean-localization guides]
Korean is a genuinely different problem class from Japanese here — not honorific *suffixes* attached to names (さん/様/くん), but **speech levels baked into verb endings and sentence-final particles** (존댓말/formal-polite vs 반말/informal-plain, ~4 active levels out of a theoretical 7), chosen per-scene from **age, social rank, job position, and relationship** between speaker and addressee — "preordained," per INLINGO's guide, not a stylistic free choice. Getting this wrong (e.g., a younger character addressing an elder informally without an established close-friend relationship) reads as a real error to Korean players, not a stylistic quibble.

**Rule for this project — map speech-level shifts to Arabic REGISTER shifts, not honorific suffixes:**
- Do **not** invent or transliterate Korean address terms as if they were Japanese honorific suffixes (there is no -سان/-ساما equivalent convention for Korean — that convention is JA-specific and does not transfer).
- Instead, **encode each character's formal/informal register as part of their character-card** (age, rank, relationship to each addressee) and let the *translation itself* — word choice, sentence structure, degree of formality/elevation in the MSA — carry the distinction Korean marks grammatically. This is the same mechanism the methodology doc already prescribes for register generally; Korean speech-levels are simply a stronger, more explicit signal for it than Japanese provides.
- **Two known signal words already found in this corpus:** 오빠 (used by a younger female addressing/referring to an older male — confirms Nia↔Ain sibling relationship) and 형 (used by a younger male addressing/referring to an older male peer/senior — the "해커형" nickname for Mark). These kinship-style address terms should translate to natural Arabic address (أخي/يا أخي or role-appropriate address), not be transliterated or dropped — same principle as the existing methodology's "contextual address words that are not suffixes still translate by meaning" rule for Japanese 兄/お嬢/坊主.
- **Cain's soldier register** (clipped, intense, ellipsis-heavy per the sample) is a per-character voice choice, not a speech-level in the Korean formal/informal sense — keep it as a voice/register note on his character card, separate from politeness-level.
- Punctuation note from the Korean-localization sources: Korean source text itself uses commas/colons more sparingly than English — this is a KO-source-styling fact, not an AR-target rule; standard Arabic punctuation policy (، ؛ ؟) still applies to the *output* regardless of KO source punctuation density.

## Fatal-Claw-specific open items
1. ~~Korean honorific/address-term inventory~~ — **researched above.** Character-card-level formal/informal + relationship data still needs populating per-NPC once dialogue batching starts (age/rank data, not found in bios above beyond sibling/mentor relationships already surfaced).
2. "Fatal Claw" (title + weapon) — see recommendation in `09_localization_plan.md`.
3. Imprint School / Engraved Skills exact KO source strings not yet cross-checked against corpus (lore-post EN may not match in-game key/string exactly) — verify against `01_extracted_strings.jsonl` before freezing glossary entries.
