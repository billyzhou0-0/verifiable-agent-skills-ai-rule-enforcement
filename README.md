# AI Rule Enforcement（AI 规矩强制机制）

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/billyzhou0-0/verifiable-agent-skills-ai-rule-enforcement.svg)](https://github.com/billyzhou0-0/verifiable-agent-skills-ai-rule-enforcement/stargazers)

**Make AI agents follow rules by mechanism, not by asking nicely. A zero-cost local health-check script + a git pre-commit hook that BLOCKS rule violations, plus the prompt-design principles that make rules actually stick.**
**让 AI 守规矩不靠自觉、靠机制：零成本本地体检脚本 + git 提交前自动拦截违规的红绿灯钩子，外加让规矩真正"长在"提示词层的设计原则。**

Written rules are probabilistic: an AI reads them and complies maybe 80% of the time. This methodology converts soft rules into hard guarantees with three layers, each proven in production.
文字规矩是概率性的：AI 读了，遵守率可能只有 80%。本方法论用三层机制把"软规矩"变成"硬保证"，每层都在真实生产环境验证过。

## Why this exists（为什么做这个）

A governance checklist said "add the msg_type field to 10,000+ records." The audit found **0 of 10,000+**. Paper rules are probabilistic: an AI reads them and complies maybe 80% of the time — less after context compression.
一份治理清单写着"给 10,000+ 条记录加 msg_type 字段"。审计发现 **10,000+ 条里 0 条做了**。纸面规矩是概率性的：AI 读了，遵守率可能只有 80%——上下文压缩之后更低。

This skill is the answer to the question "how do you KNOW the AI will follow the rules?": mechanisms, not text. A zero-cost local health-check script, a git pre-commit hook that physically blocks violations, and an injection-layer design that maximizes compliance by injecting less.
本技能回答的是"你怎么知道 AI 每次都会守规矩？"——答案是机制，不是文字：零成本本地体检脚本、物理阻止违规提交的 git 钩子、以及"注入越少、遵守率越高"的提示词层设计。

## The three layers（三层架构）

### Layer 1: A zero-cost health-check script（第一层：零成本体检脚本）

`scripts/rule_health_check.py` — stdlib only (**zero cost — it doesn't consume AI credits**), runs in milliseconds, checks five things:
纯标准库本地脚本（**零成本，不消耗 AI 额度**，毫秒级），检查五类违规：

1. **Naming compliance / 命名合规** — filename date at the END (`name-task-2026-08-11.md`, not `2026-08-11-name.md`). 日期在文件名末尾。
2. **Sync compliance / 引用同步** — stale old names/paths still referenced anywhere in the vault. 全库扫描旧文件名/旧路径残留。
3. **Sensitive info / 敏感信息** — API keys / tokens (OpenAI `sk-`, Google `AIza`, GitHub `ghp_`, AWS `AKIA`, Slack, Bearer) — **reports only, never auto-deletes** (human decides). API key/token 模式——**只报告不处理**（判断权在用户）。
4. **Frontmatter integrity / frontmatter 完整性** — every production file has YAML frontmatter. 正式层文件应有 YAML frontmatter。
5. **Credential transcription / 凭证转录** — today's user messages actually made it into the transcript archive (real check against the conversation database, ≥80% hit). 今天的用户消息是否已转录进档案（对对话数据库做真检查，≥80% 命中）。

Output: ✅/❌ per item with evidence (path + line number), paste-ready for reports.
输出：每项 ✅/❌ + 证据（路径+行号），可直接粘贴进汇报。

### Layer 2: Git pre-commit hook（第二层：git 提交前红绿灯）

The same script runs automatically on every `git commit`. **Violations BLOCK the commit.** Not a warning — a physical traffic light:
体检脚本挂到每次 `git commit` 自动运行。**违规阻止提交**——不是提醒，是物理红绿灯：

- ✅ pass → commit proceeds / 通过 → 正常提交
- ❌ fail → commit rejected with evidence, fix first / 违规 → 提交被拒，附证据，先修复
- ⚠️ human-confirm items → warning only, doesn't block / 人工确认项 → 警告不阻止

Emergency bypass exists (`git commit --no-verify`), and the hook is documented in the project's registration file so it can be rebuilt. Verified: 8/8 check categories fire correctly.
有紧急绕过（`git commit --no-verify`），钩子的重建方法登记在项目登记册。已验证 8/8 检查类别正确触发。

### Layer 3: Injection-layer design（第三层：提示词层设计）

The deeper insight: **the fewer rules you inject, the more compliance you get** (attention dilution). The system prompt was slimmed 25% (5,387 → 4,018 chars) by moving detailed rules into referenced files and keeping only non-codeable core rules (understand intent / sensitive info is decided by the user / audits are immutable) plus pointers to the single source of truth.
更深的洞察：**注入的规矩越少，遵守率越高**（注意力稀释原理）。系统提示词从 5,387 字瘦身到 4,018 字（-25%）：细则搬进承接文件，注入层只留不可代码化核心（理解指令/敏感由用户判断/审计不改）+ 指向单一事实源的指针。

Plus the output-discipline rule: **every claim of "done/updated/synced" must carry evidence (path + line number or script output)** — if you can't write the evidence, you didn't do it. The output format itself forces verification: when a report must include check results, the AI must run the checks to fill them in.
外加输出断言原则：**凡声明"已更新/已完成/已同步"必须附证据（路径+行号/脚本输出）**——写不出证据就是没真做。输出格式本身反向强制验证：报告必须包含检查结果时，AI 必须先跑检查才能填。

## Why these skills exist（实战教训——产生本方法的真实事件）

- A governance checklist existed on paper, but a 10,000+-record audit found **0/10,000+ claimed landings actually present** — the method described it, nothing executed it. Paper rules are not enforcement. / 治理清单纸面上存在，但 10,000+ 条声称的落地实际 0 条存在——方法描述了，什么都没执行。纸面规矩不是强制。
- The user asked: "how do you KNOW the AI will run the rules every time?" — the answer is mechanism, not text: hooks and scripts run deterministically, models don't. / 用户问："你怎么知道 AI 每次都会执行规矩？"——答案是机制不是文字：钩子和脚本确定性执行，模型不是。
- A "sync obligation" was treated as optional once; the rule is now: **linking updates is a duty, not a choice** — and the script checks it. / "同步义务"曾被当成可选项；现在的规矩是：**联动更新是义务不是选项**——脚本直接检查它。

## Using the script（使用方法）

```bash
python3 scripts/rule_health_check.py [--vault <path>] [--fix]
# --vault: root of the governed knowledge base (default: current dir)
# --fix:   (optional) auto-fix what's safely fixable
```

Install the hook（安装红绿灯钩子）:

```bash
cat scripts/pre-commit > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

## Files（文件）

- `SKILL.md` — the full methodology（完整方法论，中文）.
- `scripts/rule_health_check.py` — the zero-cost checker (stdlib only, configurable paths). 零成本体检器（纯标准库，路径可配置，凭证检查为可选模块）。
- `scripts/pre-commit` — the red-light hook（红绿灯钩子）.
- `LICENSE` — MIT.

## Related（相关）

Pairs with [verifiable-agent-skills-multi-source-project-recovery](../verifiable-agent-skills-multi-source-project-recovery) ("done" must mean "verifiable evidence exists"). Hub: [verifiable-agent-skills](../verifiable-agent-skills).
与「多源项目恢复」（"做完了"= 拿得出可验证证据）配套。主仓库：[verifiable-agent-skills](../verifiable-agent-skills)。
