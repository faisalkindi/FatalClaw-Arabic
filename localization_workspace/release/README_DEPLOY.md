# Fatal Claw — Arabic Localization, Release Build

## What's in `FatalClawArabic_P.pak` (2,149,323 bytes, 8 files)
1. **`FatalClaw/Content/Localization/Game/ar/Game.locres`** — full Arabic translation, all 3,559 strings (100% of the game's text corpus), built by cloning the Korean-source locres (guaranteed full key coverage, unlike the English export which is missing ~20 keys) and importing the complete Arabic CSV over it.
2. **6 `.ufont` files** at `FatalClaw/Content/FatalClaw/UI/Faces/` — every game font face (DNFForgedBlade Bold/Light, NotoSansSC Bold/Light, Togalite Bold/Light) replaced with **SST Arabic Medium** (`_shared/fonts/SST-Arabic-Medium_sanitized.ttf`), the same font used for Elliot and every other project in this house's localization history. This game's `.ufont` format is simpler than Elliot's — raw TTF bytes, no `[size][data][0]` wrapper — confirmed by parsing the sfnt table directory (computed end == file size on 2 of 3 sampled fonts, 2-byte alignment pad on the third).
3. **`FatalClaw/Config/DefaultEngine.ini`** — full original file + one appended section:
   ```
   [ConsoleVariables]
   Slate.DefaultTextFlowDirection=2
   ```
   Sets global RTL paragraph flow, same mechanism used on Elliot, confirmed as a real UE cvar (verified live in a FF7 Remake cvar dump via Exa, not assumed).

## Why "add as an addition," not a hijack
No unused locale slot matched Elliot's "nobody plays in Italian" trick (Fatal Claw ships de/en/es/fr/ja/ko/pt-BR/ru/zh-CN/zh-TW — no natural throwaway for an Arabic-speaking audience). Instead: added a **new `ar` locale folder** under `Content/Localization/Game/`. The game's own `DefaultEngine.ini` (`+LocalizationPaths=%GAMEDIR%Content/Localization/Game`, no hardcoded culture whitelist found) points exactly at that directory with no restricted culture list visible — supports (does not 100% prove without an in-engine test) that UE's standard `FInternationalization::GetLocalizedCultureNames` auto-discovery will pick up `ar` without needing a hijack.

## What I verified myself (no game launch required)
- **Corpus coverage:** 3,559/3,559 rows, zero gaps, zero orphans (`scripts/merge_and_build.py`).
- **QA validator, full corpus:** 3,559 rows, **1 flag** — `CommonInterface/LANGUAGE_KOREAN`, a deliberate, justified non-translation (language-picker entries stay in their own native script; confirmed against `LANGUAGE_RUSSIAN`'s own EN reference showing "Русский" not "Russian").
- **Cross-batch consistency sweep:** found 22 real cases where the same Korean source string got two different Arabic renderings from different parallel translation agents (e.g. "بوّابة ڤانريون" vs "بوابة ڤانريون" — a dropped shadda; "المتجر" vs "متجر"; several full-sentence paraphrase pairs on shop/quest text). Every one individually reviewed and canonicalized to one form; re-ran QA clean after.
- **Placeholder/tag integrity:** 0 issues across all 6 tag families (`\n`, `<c0-3>`/`</>`, `<img id="..."/>`, `{0}-{4}`) on the full corpus.
- **Round-trip byte verification:** exported the packed `ar/Game.locres` back out and confirmed real Arabic text reads back correctly (not just "import succeeded" log output).
- **Register spot-check across all 11 batches:** confirmed distinct, consistent per-character voicing (Cain grave/soldierly, Iedart cold/clinical, Lara warm, divine-council liturgical, epitaph verses elegiac) rather than one flat tone applied everywhere.

## What still needs YOUR hands (I don't launch the game myself — standing rule across every project in this house)
1. Close the game if running.
2. Copy `FatalClawArabic_P.pak` into `F:\SteamLibrary\steamapps\common\Fatal Claw\FatalClaw\Content\Paks\`.
3. Launch. Check whether a language option for Arabic appears, or try Steam launch option `-culture=ar`.
4. Report back: does an Arabic option appear at all; does the RTL flag visibly right-align menus/dialogue; does SST Arabic render connected/shaped correctly (this is a modern UE title so native HarfBuzz shaping should apply automatically, same as Elliot — no pre-reshaping was done, logical-order Unicode only); any garbling, missing glyphs, or crashes.
5. If Arabic doesn't appear as a selectable option even after `-culture=ar`, the fallback is hijacking an existing slot (`ru` or `pt-BR`) instead of adding a new one — same build process, five-minute change.

## Known open items (not blocking, but real)
- ~40 character/place names surfaced during bulk translation that aren't yet in `05_glossary.csv` as `resolved_pilot` — flagged in each batch's `notes` column, listed in each batch agent's report. Worth a consolidated glossary-freeze pass, but none block release: everything shipped is a confident, consistent translation.
- 7 NPCs (Cabo/Carbo, Ratio, Kuro, Ordo, Deserter, Arcadia, EXODUS) never had a resolvable gender in the corpus — defaulted to masculine grammatical agreement throughout, flagged everywhere they appear. Revisit if you find external confirmation (character art, future patch text).
- One naming-consistency question flagged by a translation agent: "올빼미 채석장" (Owl Quarry, appears once in Ortrinde's dialogue) may be the same location as the already-glossaried "Strigine Quarry" (스트리진 채석장) under a different Korean phrasing — not merged, worth a look.

---
## 2026-08-30 13:53 — Root cause of "no Arabic in game" + fix (v2 pak, 14 files, 2,237,772 bytes)
**Two causes, both confirmed by evidence, both fixed:**
1. **The pak had never been copied into the game's `Paks\` folder** — `ls` showed only the 3.6GB original. Nothing was ever loaded. Now deployed (copied while game was confirmed not running via `tasklist`).
2. **Language picker is a hardcoded list, not auto-discovered.** Extracted + JSON-dumped the widgets (UAssetGUI, `VER_UE4_27` — engine is **UE 4.27** per exe PE version resource, not UE5 as first assumed):
   - `WBP_OptionNew` export 26 (`GameSettingWidget` instance): `SupportedLanguages` StrProperty array = `ko en ja zh-TW zh-CN de es fr ru pt-BR` (10). **Appended `ar`.**
   - `WBP_GameSetting` export 59 (`WBP_HorizontalOptionBox_Language`): `StringOptions` TextProperty array of 10 `ST_CommonInterface` StringTable keys, index-aligned with the codes. **Appended `LANGUAGE_ARABIC`.**
   - `ST_CommonInterface` StringTable asset (351 rows): **appended `["LANGUAGE_ARABIC","العربية"]`** — StringTable native value is the fallback in every culture, so the menu shows "العربية" regardless of current language without per-locale locres edits.
   - `GetLocalizedCultures`/`SetCurrentCulture` in `WBP_GameSetting`'s ubergraph do the actual switch; index N → `SupportedLanguages[N]`. No bytecode edit needed — arrays are data properties.
   - All three assets passed a **null-transform test first** (tojson→fromjson unmodified == byte-identical originals) before any edit; patched builds show SerialSize deltas exactly matching uexp growth.
**Not touched:** `Default__WBP_GameSetting_C` CDO has a stale 4-entry `SupportedLanguages` (`ko en-US ja zh-Hans`) — the instance override in OptionNew wins; left alone (one change at a time).

**Test now:** launch normally, Options → Game → Language — an 11th entry "العربية" should exist. Select it. If the entry appears but text stays non-Arabic, next suspect is the `ar` locres not being resolved (culture-name mismatch) — then try `-culture=ar` launch option to separate the two.

### 13:54 — 4th gate found and patched: `Game.locmeta` (v3 pak, 15 files, 2,238,003 bytes)
`Game.locmeta` is LocMeta **version 1** (`AddedCompiledCultures`): magic GUID + native culture `ko` + `ko/Game.locres` + a `CompiledCultures` TArray<FString> of exactly the 10 shipped cultures — no `ar`. Newer UE builds consult this list when enumerating localized cultures (`GetLocalizedCultures`), which the language widget calls. Could not find a doc line that pins 4.27's exact behavior (the 4.27 Localization Overview page still describes locmeta as "currently only the native culture" — stale relative to the v1 binary the game actually ships), so rather than guess: **patched it to 11 entries** (count 10→11, appended `ar`) — strict superset, harmless if unused, required if used. Parsed the original to byte-exact end-of-file before editing, re-parsed the patched file to byte-exact end-of-file after. Deployed; read back from the deployed pak shows all 11.

**All four gates now covered:** locres data (`ar/Game.locres`) · locmeta culture list · widget code list (`SupportedLanguages`) · widget display list (`StringOptions` + `LANGUAGE_ARABIC` StringTable row). Plus fonts + RTL cvar. Pak confirmed present in `Paks\`.

### 14:06 — Fix for "other languages missing from menu" (v4 pak, 14 files, 997,139 bytes)
**Root cause (verified with fontTools, not assumed):** v1–v3 REPLACED all 6 game faces with SST Arabic Medium. SST has only **521 glyphs** — zero Hangul, CJK, or Cyrillic. So 한국어 / 日本語 / 繁體中文 / 简体中文 / русский rendered as empty labels → 5 menu entries looked "missing." The list itself was fine (11 entries); the labels were invisible. Original coverage: DNFForgedBlade = Hangul+Cyrillic, NotoSansSC = CJK+Cyrillic+Latin, Togalite = Japanese+Cyrillic+Latin — none Arabic. Replacing was the wrong design.

**Correct design (what ships now): ADD SST as a new face, route only Arabic to it.**
- Removed all 6 `.ufont` overrides — originals load again, every language label renders.
- New package `UI/Faces/SSTArabic-Medium` (`.uasset` + `.uexp` cloned from NotoSansSC-Bold's FontFace asset with names/SourceFilename rewritten; `.ufont` = SST Arabic Medium bytes, raw TTF like the game's own faces).
- `UI/DNFForgedBlade_Font` (the game's single composite font, null-transform verified byte-identical before editing): added 2 imports (`SSTArabic-Medium` FontFace + its Package) and a **3rd `SubTypeface`** — `CharacterRanges` = U+0600–06FF, U+0750–077F, U+08A0–08FF, U+FB50–FDFF, U+FE70–FEFF; `Cultures` = "" (applies in every culture); `Typeface` Light+Bold both → the new face. Mirrors exactly how the game already routes `ja`→Togalite and `zh`→NotoSansSC. Arabic blocks don't overlap either existing range set.
- Re-read the built composite from disk: 3 sub-typefaces, new face resolves to import -16, ranges correct. Deployed; deployed pak read back: SST `.ufont` starts `00 01 00 00` (TTF), composite references `SSTArabic-Medium`.

**Test:** menu should now list all 11 languages with readable labels; Arabic text still in SST; Latin/CJK/Cyrillic text back to the game's own fonts.

### 17:05 — Fix for Arabic-Indic digits + "? ? ?" numbers (v5 pak, culture code now `ar-MA`)
**Root cause (evidence, not guess):** translations contain **0** Arabic-Indic digits (grepped all 3,559 rows). The digits come from ICU: under culture `ar`, CLDR's default numbering system is `arab`, so every *runtime-formatted* number (42 rows use `{N}` args, plus HP/counters/timers) is emitted as ٠-٩. Composite-font UI renders them as Indic digits (SST has those glyphs); engine/FX fonts without U+0660–0669 render `?`. One cause, both symptoms.
**Ruled out:** patching ICU data — the game's `ar.res` is formatVersion 3 with a shared `pool.res` (the `arab`/`latn` strings aren't even in `ar.res`), ICU 64 vs Windows ICU 72 means no way to verify a rebuilt bundle. `ar-EH` (modern CLDR: latn + `.`/`,`) — its shipped `ar_EH.res` is a 92-byte empty stub in ICU 64 → would inherit `arab`. 
**Fix:** culture code `ar` → **`ar-MA`** everywhere (locres folder, `Game.locmeta` entry, `WBP_OptionNew.SupportedLanguages`). `ar_MA.res` in the shipped ICU 64 data is a real 572-byte override; ICU's own locale data lists Zero digit `0` for `ar_MA`. Display name in the menu is unchanged («العربية»). All three copies (deployed pak, installer payload, manual zip) hash-identical: `090208f5…`.
**Known tradeoff:** `ar-MA` uses French-style separators — decimal `,` and thousands `.` (e.g. `1.234`). Integers/counters unaffected. No shipped Arabic locale in ICU 64 combines Latin digits with `.`/`,` separators.
