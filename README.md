# AI Rule Enforcement

**Make AI agents follow rules by mechanism, not by asking nicely. A zero-cost local health-check script + a git pre-commit hook that BLOCKS rule violations, plus the prompt-design principles that make rules actually stick.**

Written rules are probabilistic: an AI reads them and complies maybe 80% of the time. This methodology converts soft rules into hard guarantees with three layers, each proven in production:

## The three layers

### Layer 1: A zero-token health-check script (`scripts/rule_health_check.py`)

A local Python script (stdlib only — **zero token cost**, runs in milliseconds) that checks the five things that matter:

1. **Naming compliance** — filename date at the END (`name-task-2026-08-11.md`, not `2026-08-11-name.md`)
2. **Sync compliance** — stale old names/paths still referenced anywhere in the vault
3. **Sensitive info** — API keys / tokens (OpenAI `sk-`, Google `AIza`, GitHub `ghp_`, AWS `AKIA`, Slack, Bearer) — **reports only, never auto-deletes** (human decides)
4. **Frontmatter integrity** — every production file has YAML frontmatter
5. **Credential transcription** — today's user messages actually made it into the transcript archive (real check against the conversation database, ≥80% hit)

Output: ✅/❌ per item with evidence (path + line number), paste-ready for reports.

### Layer 2: Git pre-commit hook (the "red light")

The same script runs automatically on every `git commit`. **Violations BLOCK the commit.** Not a warning — a physical traffic light:

- ✅ pass → commit proceeds
- ❌ fail → commit rejected with evidence, fix first
- ⚠️ human-confirm items → warning only, doesn't block

Emergency bypass exists (`git commit --no-verify`), and the hook itself is documented in the project's registration file so it can be rebuilt if the repo is cloned fresh. Verified: 8/8 check categories fire correctly.

### Layer 3: Injection-layer design (prompt discipline)

The deeper insight: **the fewer rules you inject, the more compliance you get** (attention dilution). The system prompt was slimmed 25% (5,387 → 4,018 chars) by moving detailed rules into referenced files and keeping only:

- Non-codeable core rules (understand intent / sensitive info is decided by the user / audits are immutable)
- Pointers to the single source of truth (one file, updated in one place)

Plus an output-discipline rule: **every claim of "done/updated/synced" must carry evidence (path + line number or script output)** — if you can't write the evidence, you didn't do it. The output-format itself forces verification: when a report must include check results, the AI must run the checks to fill them in.

## Why these skills exist (the incidents that produced them)

- A governance checklist existed on paper, but a 451-record audit found **0/451 claimed landings actually present** — the method described it, nothing executed it. Paper rules are not enforcement.
- The user asked: "how do you KNOW the AI will run the rules every time?" — the answer is mechanism, not text: hooks and scripts run deterministically, models don't.
- A "sync obligation" was treated as optional once; the rule is now: **linking updates is a duty, not a choice** — and the script checks it.

## Using the script

```bash
python3 scripts/rule_health_check.py [--vault <path>] [--fix]
# --vault: root of the governed knowledge base (default: current dir)
# --fix:   (optional) auto-fix what's safely fixable
```

Install the hook:

```bash
cat scripts/pre-commit > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

## Files

- `SKILL.md` — the full methodology (Chinese).
- `scripts/rule_health_check.py` — the zero-token checker (stdlib only, configurable paths).
- `scripts/pre-commit` — the red-light hook.
- `LICENSE` — MIT.

## Related

Pairs with [verifiable-agent-skills-multi-source-project-recovery](../verifiable-agent-skills-multi-source-project-recovery) ("done" must mean "verifiable evidence exists"). Hub: [verifiable-agent-skills](../verifiable-agent-skills).
