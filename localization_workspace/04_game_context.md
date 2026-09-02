# Game Context — Fatal Claw

Sources: [SRC] Steam store page, Steam Community dev posts (lore-reveal posts), Club 250 mirror of dev lore posts, Inven Global launch article. [INF] inferred from KO source-string sampling. Confidence tags used throughout: [SRC]=official text, [INF]=inference from corpus, [?]=unresolved.

## Premise [SRC]
A destroyed ancient kingdom, revived by modern technology. The playable character is **Kisha**, a mysterious cat resurrected by his ancestors, exploring a vast underground realm where **Ancients** and **Commoners** coexist. Kisha's goal: complete the ultimate weapon **"Fatal Claw"** and uncover the mastermind behind the world's corruption/infection. Full 1.0 release: ~30 hours, multi-ending structure (NPC narrative branches → individual endings).

## World / factions [SRC]
- **Elord Kingdom** — the ancient kingdom, fell ~10,000 years ago. Ruled historically by a dynasty of **Yellow Cats**, later overthrown by **Black Cats** (흑묘족). Kisha is called "the Black Cat" by at least one NPC (Cain) — protagonist's faction/lineage marker.
- **Kannir** — the kingdom's fundamental energy source. Liquid state = highly toxic. Solid/condensed form = **Kannic**, used as currency and stable energy.
- **Origin Laboratory** — underground research facility built by the Commoners around the **Stone of Records** (containing sleeping Ancients), to study Elord technology and Kannir. Kisha awakens here.
- **The Sorr** — resilient wolf-warrior people, historically royal guards of the kingdom; stripped of status and exiled to the **Higasha Tundra** after the Black Cats seized power. Their leader in the current story is **Sorron**, feared even by Cain; his lieutenant is **Enma**, the "Golden Spirit Wolf," a sorceress who distorts reality/illusion.
- **King Odz** — sealed the only passage to the surface after the corruption outbreak.
- **Aphotic Marsh** — corrupted wetland, deepest/darkest region, source of the "black sludge" corruption; connected to a mysterious figure (referenced only as "someone who has endured alone for ages") who grants Kisha power and the **Silver Chain**.
- **Jayma's Dungeon** — hidden sealing-prison built by Examu (first king of Elord) to imprison anything chaotic (monsters, traitors, secrets) — entry requires royal-bloodline "King's Authority."
- **Imprint School** — a vanished faction/school associated with **Engraved Skills** (刻印技能/새김 스킬), located in the Black Canyon ruins.
- **Strigine Quarry** — mining site for Stone-of-Records raw material, maintained historically by "owl artisans" (Strigine = owl-coded).
- Regions confirmed: Kannir Belt/Kannir Drilling Site, Higasha Tundra, Strigine Quarry, Black Canyon, Aphotic Marsh, Elord Castle (Lower Elord Castle), Origin Laboratory.

## Cast (from corpus line-counts, `04_file_audit.md` roster)
Largest speaking roles by line count: **Skyle (117), Ortrinde (91), Iedart (76), Albus (68), Cain (65), Tiz (60)**, then a long tail of ~20 more named NPCs (Tomi, Nia, Max, Ainjaff, Cabo, Lara, Masa, Dotiman, Ain, Zack, Mark, Rotri, Fatum, Grimbill, Caiman, Sofoly, Helena, Ordo, Ratio, Deserter, Murant, Arcadia, EXODUS) plus a "Guide (Automata)" NPC.
- **Cain** — antagonist-aligned Sorr warrior/soldier, serves Sorron ("Master Sorron"), calls Kisha "the Black Cat," expresses grave/fatalistic register ("So this... was the meaning of my existence. How futile."). Sample lines show a soldier's clipped, intense delivery — short sentences, ellipses for hesitation/tension.
- **Sorron** — Sorr faction leader, the main antagonist driving the plot (obsessed with "Aisare's Stone," imprisoned innocents including children for his ambition — morally dark).
- **Enma** — "Golden Spirit Wolf," Sorron's lieutenant, illusion/reality-distorting sorceress.
- Character identities/genders/exact roles for the rest of the roster (Skyle, Ortrinde, Iedart, Albus, Tiz, etc.) are **not yet researched** — flagged for a follow-up recon pass (character wiki / trailer / store screenshots) before the pilot, since gender-correct Arabic requires this.

## Tone / register signal [INF from corpus sampling]
Sampled Cain dialogue reads as **grave, literary, somewhat elevated** — not light/comic adventure banter: "...So this... was the meaning of my existence. How futile," "Only to end up as a sacrifice, fed to Kurtz..." Fits the game's own framing ("this dark, desperate world," corruption/infection, child imprisonment, multi-ending tragedy structure). Per `LOCALIZATION_METHODOLOGY.md`'s per-game register rule ("source-localization register + setting → target register"), this points toward **elevated-but-readable MSA** (closer to the FFT IVC calibration than Elliot's "warm everyday" default), but **register must be locked in the pilot**, not assumed from six sampled lines — confirm across NarrativeScene/Cinematic/ST_NPC_Event before freezing.

## Terminology candidates surfaced (feed into `05_glossary.csv`)
Kisha, Fatal Claw (weapon name), Elord Kingdom, Kannir / Kannic, Origin Laboratory, Stone of Records, Ancients / Commoners, Yellow Cats / Black Cats, the Sorr, Sorron, Enma (Golden Spirit Wolf), Higasha Tundra, Aphotic Marsh, Silver Chain, King's Authority, Jayma's Dungeon, Examu, King Odz, Imprint School / Engraved Skills, Strigine Quarry, Black Canyon, Stone of Immortality Chamber, Cabitz (ability-customization stone), Carox ("Kailox" — Cat+Radar+Codex portmanteau per dev commentary), Kurtz.

## NPC gender table [SRC — resolved via EN locres cross-reference, Rule 0 Case-B]
No fan wiki exists for this game yet (too new), so genders were recovered from the EN `Game.locres`'s explicit pronouns in `Journal_DESC_System/NPC_*` bio entries and corroborating dialogue/achievement text — exactly the master doc's Rule-0 Case-B technique (source drops gender, official other-language export doesn't).

**Male:** Skyle (ranger captain, "He deeply cares..."), Mark ("he is deeply interested..."), Max ("he has a profound interest..."), Sofoly ("He strives diligently..."), Zack ("He strives to restore..."), Dotiman ("he sealed the king in crystal"), Ainjaff ("he might have endured"), Cain ("wield a sword... as if it were part of his own body"), Grimbill ("he now devotes himself..."), Ain ("he is willing to take a risk"), Albus ("him" — Tiz/Albus dialogue cross-ref), Tiz ("him" — Albus dialogue cross-ref), Tomi ("He is eager to earn recognition"), Fatum ("He explains its history..."), Issac ("he was an influential figure"), Caiman ("he continues his own research"), Kurtz/White Kurtz ("his pursuit... his own life"), Sorron ("Under his orders... devote loyalty to him"), King Odz/Odds ("he sealed the gates... fought until his final").

**Female:** Iedart (researcher, "She is conducting her research" — matches achievement text "help complete her research"), Masa ("She is well-versed..."), Lara ("her attentive and bubbly nature... She is always on the lookout"), Nia ("She follows and deeply cares for her older brother" — confirms Ain is her older brother), Enma ("her true identity was..."), Helena ("she remains on the ruinous battlefield"), Rotri ("her/she" via Lara's rescue dialogue), Grande (recipient of a "congratulations on your pregnancy!" letter from Iedart — pregnant → female).

**Genderless/machine (treat as "it" in EN; Arabic convention TBD — likely default masculine grammatical agreement per house style for automata, confirm in pilot):** Ortrinde/Ortlinde ("Captain of the royal automaton guards. It continues to protect..."), Murant (boss, "an infected entity... it appears to retain...").

**Still unresolved — do not guess, flag for the pilot:** Cabo/Carbo, Ratio, Kuro, Ordo, Deserter, Arcadia, EXODUS. No explicit self-referential pronoun found in either bio or own-dialogue rows for these; needs either a targeted deeper corpus pass (search full dialogue trees, not just bios) or store/trailer screenshot check before their scenes are translated.

## Kisha (protagonist)
Confirmed **masculine** [SRC store copy: "you will join Kisha—a mysterious cat resurrected by his ancestors"].

## Opening cinematic — corrected reading [SRC: pilot-batch KO/EN text, `Cinematic/Cinematic_Opening_Dialogue_*`]
The prologue is a **divine council scene**, not a plain historical cave-painting narration. Speakers: several unnamed gods/elders (Female_A, Male_B, Male_C, Female_D — the deliberating council), a **King** (= **Examu**, the deified first king of Elord, addressed in third person by the others as "Lord Examu" — 엑사무님), and **Grande** (final blessing line, "Kisha... may you at least protect everyone you love..."). The council debates whether to grant "this child" (Kisha, called "impure-blooded," 순혈도 아닌 것) a second chance/resurrection despite taboo ("금기"); Examu overrules the majority's fatalism and revives Kisha as "warrior of the kin." Cross-reference: `Interactable/INTERACTABLE_LABOPHOTO_GRANDE_01` is a separate personal letter from Iedart to a pregnant Grande — same name, possibly the same divine figure in a mortal/village-life context, or two different characters sharing a name; **flag as unresolved** until more of Grande's material is translated.

## New terminology surfaced in pilot batch (added to `05_glossary.csv`)
Golden Claw (금빛 클로) / Silver Claw (은빛 클로) — Kisha's two weapon-artifacts, distinct from the game-title "Fatal Claw" (페이탈 클로) which is UI/credits-only in this batch. Vanrion's Gate (반리온의 문), Stone of Intelligence (지성의 돌), Aisare (아이사르, owl craftsman who made the Stone of Records shards), Nagaraja (나가라자, a self-sacrificing deity/legend tied to the Imprint School and Black Canyon), Mirkam (미르캄), Snaga (스나가, "lord of might"), Lyani (랴니), Irbes (이르베스), Jayma (제이마, owl leader — already had the Dungeon entry), the Deity/Avatar epithet (화신), Poppo (포뽀, a recurring nuisance creature).

## Open research items — final status
1. NPC genders — **resolved above** for 27/29.
2. Kisha gender — **resolved above**.
3. Register — **locked in the pilot as elevated-but-readable MSA**, confirmed across UI/item/skill/dialogue/cinematic in the pilot batch (see `06_arabic_style_guide.md` for the final call).
4. "Fatal Claw" (game title) — **resolved: translate**, see `05_glossary.csv` (المخلب القاتل). Distinct from "Golden Claw"/"Silver Claw," which are separate in-game weapon artifacts, also translated (not transliterated) for consistency.
