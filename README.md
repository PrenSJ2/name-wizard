# name-wizard

A Claude Code slash command for naming projects, products, and companies.

`/name-wizard` runs a 7-step workflow that goes from raw brief to ranked shortlist to brand-strategist-grade deep-dives on the top 3 picks.

## What it does

1. **Context gathering** — prompts for industry, target buyers, known competitors, and tone.
2. **Parallel candidate generation** — a creative-namer sub-agent produces 20-30 candidates across every naming strategy (portmanteau, coined Latin/Greek roots, truncation, compound words, metaphor, prefix/suffix play, foreign words, onomatopoeia, etc.), while a domain-hacker sub-agent produces 15-25 domain-hack candidates across hackable TLDs.
3. **Dedupe** — collects all unique names.
4. **Domain availability check** — batches the candidates against a public domain status API.
5. **Score and rank** — a name-analyst sub-agent scores every candidate 1-10 across memorability, pronunciation, spellability, brevity, distinctiveness, emotional fit, global safety, and domain quality. Presents three tiers: TOP PICKS (≥75/80), STRONG CONTENDERS (60-74), WORTH CONSIDERING (<60).
6. **Brand-strategist deep-dive on top 3** — for each of the top 3 names, a brand-strategist sub-agent uses web research to produce:
   - Etymology (linguistic roots, semantic construction)
   - 3-5 tagline directions, each tagged with tone and target audience
   - 2-3 logo concept directions
   - Positioning angles per buyer persona
   - Competitive naming landscape (informed by the user's named competitors + web research)
   - "Why this name works" closing narrative
7. **Final recommendation** — picks one and says why.

## Install

Drop `name-wizard.md` into `~/.claude/commands/` and Claude Code will pick it up as `/name-wizard`.

```bash
cp name-wizard.md ~/.claude/commands/
```

## Use

```
/name-wizard a regulatory compliance platform for pharma
```

The skill will prompt for the remaining context (buyers, competitors, tone) before generating.

## License

MIT
