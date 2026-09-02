# File Audit — Fatal Claw

## Game / Studio
- **Fatal Claw** (Steam App ID 2827750), 2D Metroidvania. Developer **NDEV GAMES**, publisher **Com2uS Holdings** — both Korean. [SRC: Steam store page, Inven Global, Steam Community dev posts]
- Early Access → 1.0 full release 2026-08-26/27. Dev-language confirmed **Korean** (developer commentary video is in Chinese/Korean promotional context, but studio and publisher are Korean; Korean source strings read as the originals — shortest, most idiomatic, zero translationese — vs. EN/JA which read as translations of them). [INF, high confidence]

## Engine / format
- Unreal Engine, **legacy `.pak`** (NOT IoStore — no `.ucas`/`.utoc` found in archive). [SRC: file listing]
- Real shipping binary: `FatalClaw/Binaries/Win64/FatalClaw-Win64-Shipping.exe`. `FatalClaw.exe` at game root is a thin launcher stub (345 KB).
- Single pak: `FatalClaw/Content/Paks/FatalClaw-WindowsNoEditor.pak`, 3,622,634,519 bytes.
- `repak info` (no key): version detection fails → encrypted index.
- AES key (AESDumpster, confirmed via `repak info` with key): `0xD71ADCAE042720D77413E2C04FF19ECCA15E0AF497D88C1178E5C4016C06B6FF`
- Pak header: version **V11 (Fnv64BugFix)**, encrypted index=true, compression=**None**, path-hash seed **D4903541**, mount point `../../../`, **37,300 file entries**.
- Engine version not yet pinned (no `Build.version` found in pak listing; no exe-string engine-version grep hit yet). Needs `jmap`/FModel confirmation before any DataTable/widget edit (locres-only work doesn't need it).

## Where the text lives
- Standard **`.locres`** string tables at `FatalClaw/Content/Localization/Game/<culture>/Game.locres` — same delivery mechanism as Elliot (main UE track), NOT a custom DataTable/MessagePack format like Octopath's Kingship engine.
- Shipped culture folders: `de en es fr ja ko pt-BR ru zh-CN zh-TW` (10 locales). **No `it`, no `ar`.**
- `Game.locmeta` present alongside.
- Also present: `Engine/*.locres` and `OnlineSubsystem*.locres` — engine boilerplate, not game text, skip.

## Corpus size
- Per-locale row counts (UnrealLocres export): en=3,537 / ja=3,538 / ko=3,559 / de=3,536.
- **Union of KO/JA/EN keys = 3,559. Every key has a Korean source row — 100% parity, no fallback-only rows.** Small corpus relative to Elliot (16k) or Octopath (50k) — single-project-scale, no local-vLLM-bulk pipeline needed; direct primary translation (Gemini or Claude subagents) is appropriate per the master doc's "small full game" route.

## Category breakdown (by key namespace, from KO source, n=3559)
| Category | Rows | Notes |
|---|---:|---|
| ST_NPC_Event | 354 | Scripted NPC event/cutscene dialogue |
| CommonInterface | 351 | Core UI strings |
| Journal_DESC_System | 195 | Journal/codex system entries |
| Interactable | 193 | World object interaction prompts |
| Item | 187 | Item names/descriptions |
| Cinematic | 132 | Cutscene lines (matches earlier extracted sample) |
| Npc_Skyle..Npc_Murant | ~1,150 total across 29 named NPCs | Per-character dialogue, largest bucket overall — see roster below |
| MonsterNames | 102 | |
| RegionName | 101 | |
| LogBook | 97 | |
| Skill / SkillTree | 155 | |
| Journal_DESC_Kisha / _Quote | 130 | Protagonist-specific + quote journal entries |
| NarrativeScene | 80 | |
| NpcNames | 62 | |
| DocumentedStone | 45 | Lore item type ("Stone of Records" family per Steam lore) |
| InputRebind | 40 | Keybind labels — mostly non-translatable/short UI |
| ObjectName | 31 | |
| ST_Npc_Kuro | 19 | |
| Prologue | 15 | |
| Shop_Ainjaff | 10 | |

## NPC roster (line count, KO name)
Skyle/스카일 117 · Ortrinde/오르트린데 91 · Iedart/이에다트 76 · Albus/알버스 68 · Cain/카인 65 · Tiz/티즈 60 · Tomi/토미 52 · Nia/니아 50 · Max/맥스 45 · Guide(Automata) 41 · Ainjaff/아인자프 40 · Cabo/카보 40 · Lara/라라 40 · Masa/마사 40 · Dotiman/도티먼 36 · Ain/아인 32 · Zack/잭 32 · Mark/마크 31 · Rotri/로트리 31 · Fatum/파툼 30 · Grimbill/그림빌 30 · Caiman/카이만 24 · Sofoly/소폴리 24 · Helena/헬레나 23 · Ordo/오르도 19 · Ratio/레시오 19 · Deserter/탈영병 15 · Murant/뮤런트 13 · Arcadia/아르카디아 5 · EXODUS 3.

Key naming convention: `Npc_<EnglishName>/<KoreanName>_<scene/context>_<index>[_variant]`, e.g. `Npc_Cain/카인_보스전_시작이벤트_04` (Cain, boss-fight start event, line 4). **Speaker is derivable directly from the key** for all Npc_* rows — no separate speaker-tagging pass needed for those (~1,150 rows). ST_NPC_Event (354) and Cinematic (132) and NarrativeScene (80) rows need a speaker/addressee-resolution pass since the key alone doesn't always name the speaker for these.

## What to skip
- `InputRebind` (40 rows) — mostly key names ("Space", "Tab") — audit individually, likely mostly non-translatable.
- Any row whose KO/EN/JA are all identical to a placeholder-only string (`{0}` etc.) — check during corpus classification pass.
- Engine/OnlineSubsystem locres — not game content.

## Placeholder/tag inventory (from full KO corpus scan)
Small, familiar set — same style as Elliot: `\n` (literal newline), `<c0>`/`<c1>`/`<c2>`/`<c3>` + `</>` (rich-text color tags), `<img id="PC.Num_0..6"/>` (inline icon), `{0}`-`{4}` (format args, mostly `CommonInterface`/`SkillTree` key-guide/keybind strings). No printf `%s`/`%d` found — lower crash risk than the no-shaper engines' format-string class of bugs (not applicable here anyway; this is a modern UE title with native shaping).

**Bonus find:** the opening `Cinematic_Opening_Dialogue_NN_<Gender>_<Letter>` keys (e.g. `..._05_Male_B`, `..._06_Female_D`) already encode **speaker gender directly in the key** for the prologue's multi-elder/ancestor scene — not a player-gender branch, a multi-speaker cast tag. Free gender data for those ~6 rows, no resolution pass needed.

## Font
- Shipped `.ufont` faces (12 total, game-specific ones): `DNFForgedBlade-Bold/Light.ufont`, `NotoSansSC-Bold/Light.ufont`, `Togalite-Bold/Light.ufont`. **None have Arabic glyph coverage.** Standard fix: swap in `_shared/fonts/SST-Arabic-Medium_sanitized.ttf` per the playbook default, wrapped as `.ufont`.

## Culture-slot decision (open, needs owner call)
No unused slot matches Elliot's "Italian nobody uses" trick — closest analogues are `ru` or `pt-BR` (least likely to be actively used by an Arabic-speaking audience). Alternative: **add a genuine new `ar` locale folder** under `Content/Localization/Game/` — UE's locres system auto-discovers culture subfolders, so this doesn't require hijacking an existing slot at all, and `ar` is a first-class ICU RTL culture (cleaner than a hijack). Recommend the **add-new-`ar`-folder** route; needs a delivery-mechanism test (loose-pak override, since this is a legacy non-IoStore pak, matching the "loose pak works" branch of the playbook rather than Elliot's IoStore-triple branch) before committing.

## Toolbox
Copied Elliot's `scripts/_tools/` into `FatalClaw/localization_workspace/scripts/_tools/` per playbook step 1 (retoc, repak, UAssetGUI, UnrealLocres, EnExtract, WidgetEdit, AESDumpster, jmap, FModel). All confirmed working against this pak (repak info/list/get, UnrealLocres export all succeeded).

## Risks / unknowns
1. Engine version unconfirmed — needed only if DataTable/widget work becomes necessary (font swap, RTL widget alignment).
2. Culture-slot delivery mechanism (new `ar` folder vs. hijack) untested in-engine yet.
3. Whether `DT_AchievementDataTable` and similar `DT_*` assets carry inline text outside the locres system — not yet checked (achievement descriptions might live there instead of/alongside locres).
4. RTL config (`Slate.DefaultTextFlowDirection=2`) injection path for a legacy (non-IoStore) pak not yet tested — likely a loose `DefaultEngine.ini` override or base-pak rebuild; needs recon.
