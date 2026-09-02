# Pipeline notes (for contributors)

Working files, not needed to play. Everything player-facing is in the README and the Releases page.

## Layout

| Path | What |
|---|---|
| `localization_workspace/00_file_audit.md` | Recon: pak layout, AES key location, engine version, text formats |
| `localization_workspace/04_game_context.md` | World, cast, factions, speaker/gender evidence |
| `localization_workspace/05_glossary.csv` | Frozen terminology for characters, factions, places, items |
| `localization_workspace/06_arabic_style_guide.md` | Register, gender, punctuation, locked decisions |
| `localization_workspace/07_pilot_translation.csv` | Pilot batch that locked the register |
| `localization_workspace/09_localization_plan.md` | Batch plan and stage order |
| `localization_workspace/10_arabic_translation.csv` / `.jsonl` | Final merged corpus, 3,559 rows |
| `localization_workspace/10_full_qa_report.md` | Full-corpus QA results |
| `localization_workspace/scripts/` | Validator, merge/build, consistency sweep |
| `localization_workspace/release/README_DEPLOY.md` | Build log: every root cause and fix, dated |
| `installer/` | .NET 8 WinForms installer source |
| `NEXUSMODS_DESCRIPTION.txt` | Nexus page (BBCode, bilingual) |

## Stages

1. Recon (`00_file_audit.md`): UE 4.27, pak V11 Fnv64BugFix, encrypted index, mount `../../../`, path-hash seed 3431742785 (0xD4903541). AES key recovered with AESDumpster.
2. Extract: `repak` + UnrealLocres → per-culture CSVs (`ko` is the source of truth; EN/JA cross-reference only for gender/referents).
3. Translate: Korean → MSA in context-rich batches; register locked in the pilot; frozen glossary enforced.
4. QA: `scripts/40_qa_validate.py` (placeholder parity, Arabic punctuation, Western digits, no dialect, glossary presence) + cross-batch consistency sweep (`scripts/fix_consistency.py`).
5. Build: `scripts/merge_and_build.py` merges the CSV over the `ko` locres base into `ar-MA/Game.locres`.
6. Integration (all four gates, patched with UAssetGUI at `VER_UE4_27`):
   - `Game.locmeta` — add `ar-MA` to `CompiledCultures`
   - `WBP_OptionNew` — add `ar-MA` to `SupportedLanguages`
   - `WBP_GameSetting` — add `LANGUAGE_ARABIC` to `StringOptions`
   - `ST_CommonInterface` — add `LANGUAGE_ARABIC` → «العربية»
7. Font: SST Arabic Medium added as a new FontFace package + a third sub-typeface on the composite font `UI/DNFForgedBlade_Font` (Arabic Unicode ranges only; no original font replaced). `DefaultEngine.ini` adds `Slate.DefaultTextFlowDirection=2`.
8. Pack: `repak` V11 with the game's AES key and seed → `FatalClawArabic_P.pak` (14 files).

## Why culture `ar-MA`

Plain `ar` makes ICU format runtime numbers with Arabic-Indic digits (٠-٩), which also rendered as `? ? ?` in fonts lacking those glyphs. `ar-MA` ships real ICU data with Latin digits. Tradeoff: decimals show as `1,5`, thousands as `1.234`.

## Rebuilding

Needs the game installed (Steam AppID 2827750), `repak`, UnrealLocres, UAssetGUI, Python 3. Game files, extracted assets and built binaries are not committed.

- Installer: `cd installer && dotnet publish -c Release -r win-x64 --self-contained -p:PublishSingleFile=true -o publish` after regenerating `payload.zip` from the built pak.
