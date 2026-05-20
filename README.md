# name-wizard-skill

A Claude Code slash command for naming projects, products, and companies.

`/name-wizard` runs a 7-step workflow that goes from a raw brief to a ranked shortlist to brand-strategist-grade deep-dives on the top 3 picks — with real-time domain availability and competitive web research.

## What it does

1. **Context gathering** — prompts for industry, target buyers, known competitors, and tone.
2. **Parallel candidate generation** — two sub-agents run at the same time:
   - **creative-namer** — 20-30 candidates across every naming strategy (portmanteau, coined Latin/Greek roots, truncation, compound words, metaphor, prefix/suffix play, foreign words, onomatopoeia, etc.)
   - **domain-hacker** — 15-25 domain-hack candidates across hackable TLDs (`.io .ly .ai .me .co .sh .app .dev` and more)
3. **Dedupe** — collects all unique names.
4. **Domain availability check** — batches the candidates against a public domain status API (see *Domain check* below).
5. **Score and rank** — the **name-analyst** sub-agent scores every candidate 1-10 across memorability, pronunciation, spellability, brevity, distinctiveness, emotional fit, global safety, and domain quality. Presents three tiers: TOP PICKS (≥75/80), STRONG CONTENDERS (60-74), WORTH CONSIDERING (<60).
6. **Brand-strategist deep-dive on top 3** — for each of the top 3 names, the **brand-strategist** sub-agent uses web research to produce:
   - Etymology (linguistic roots, semantic construction)
   - 3-5 tagline directions, each tagged with tone and target audience
   - 2-3 logo concept directions
   - Positioning angles per buyer persona
   - Competitive naming landscape (informed by the user's named competitors + web research)
   - "Why this name works" closing narrative
7. **Final recommendation** — picks one and says why.

## Repository contents

```
name-wizard.md              # The /name-wizard slash command
agents/
  creative-namer.md         # Generates broad pool of candidates
  domain-hacker.md          # Generates TLD-as-word candidates
  name-analyst.md           # Scores and tiers candidates
  brand-strategist.md       # Deep-dive on shortlisted names
scripts/
  check_domains.py          # Domain availability checker (stdlib only)
install.sh                  # One-shot installer for Claude Code
```

## Install

Run the installer (copies the command, all four sub-agents, and the domain-check script into your Claude Code config):

```bash
./install.sh
```

Files land at:

```
~/.claude/commands/name-wizard.md
~/.claude/agents/{creative-namer,domain-hacker,name-analyst,brand-strategist}.md
~/.claude/name-wizard/check_domains.py
```

Restart Claude Code (or open a new session) and `/name-wizard` will be available.

## Use

```
/name-wizard a regulatory compliance platform for pharma
```

The skill prompts for the remaining context (buyers, competitors, tone) before generating.

## Domain check

Step 4 of the workflow runs the bundled `check_domains.py` script via Bash:

```bash
~/.claude/name-wizard/check_domains.py foo.com bar.io baz.app
# foo.com: AVAILABLE
# bar.io: taken
# baz.app: AVAILABLE
```

The script:
- Uses **only the Python standard library** (no `pip install` required, Python 3.8+)
- Hits the public, unauthenticated **Revved domain status API** (`https://domains.revved.com/v1/domainStatus`)
- Batches up to 25 domains per request internally — pass as many as you want
- Accepts space-separated, comma-separated, or stdin (`-`) input
- Prints stable `name: AVAILABLE|taken|unknown` lines, one per domain

You can also run it standalone outside the skill:

```bash
./scripts/check_domains.py mutaris.com mutaris.io mutaris.ai
echo "foo.com bar.io" | ./scripts/check_domains.py -
```

If you'd rather use a different domain availability service, swap out the URL in `scripts/check_domains.py` — the response format expected is `{"status": [{"name": "...", "available": true|false}, ...]}`.

## Web research

Step 6 (brand-strategist) uses Claude Code's built-in `WebSearch` and `WebFetch` to research the competitive landscape. No API keys required.

## License

MIT
