# Changelog（更新记录）

All notable changes to this project are documented here, following Keep a Changelog with semver versioning. / 本文件按 Keep a Changelog 规范记录本项目所有重要变更。

## [1.1.1] - 2026-08-11

### Patch Changes / 补丁

- [`51ef67c`](https://github.com/billyzhou0-0/verifiable-agent-skills-ai-rule-enforcement/commit/51ef67c) Add `CHANGELOG.md` and `CONTRIBUTING.md`; add an **Example usage（使用示例）** section to `SKILL.md` (scenario → steps → expected output). / 添加更新记录与贡献指南；SKILL.md 新增使用示例（场景→步骤→输出）。

## [1.1.0] - 2026-08-11

### Minor Changes / 次要版本：发布打磨（Release polish）

- [`a1abb07`](https://github.com/billyzhou0-0/verifiable-agent-skills-ai-rule-enforcement/commit/a1abb07), [`24caa34`](https://github.com/billyzhou0-0/verifiable-agent-skills-ai-rule-enforcement/commit/24caa34) — README overhaul: / README 改造：
  - Description rewritten pain-point-first (EN+CN) / 描述痛点驱动（双语）
  - Topics tags added / 添加 Topics 标签
  - License + Stars badges / License 和 Stars 徽章
  - 'Why this exists' pain-point story / '为什么做这个'痛点故事
  - README fully bilingual (native-level EN + CN, every paragraph and table cell) / README 全面中英双语

## [1.0.0] - 2026-08-11

### Initial open-source release / 初始开源发布

- [`3f8de93`](https://github.com/billyzhou0-0/verifiable-agent-skills-ai-rule-enforcement/commit/3f8de93) — Initial release. / 初始发布。

- **Three-layer architecture / 三层架构** — ① zero-cost health-check script (stdlib, checks naming/sync/sensitive-info/frontmatter/transcript coverage, reports sensitive info without auto-deleting); ② git pre-commit hook that BLOCKS violations (verified 8/8 categories); ③ injection-layer design (system prompt slimmed 25% → higher compliance). 零成本体检脚本（命名/同步/敏感/frontmatter/凭证五项，敏感只报告不处理）；提交前红绿灯钩子（8/8 验证）；提示词瘦身设计（-25% → 更高遵守率）。
- **Output-assertion discipline / 输出断言原则** — every claim of 'done/updated/synced' must carry evidence (path + line number or script output); report formats that include check results force the AI to actually run checks. 凡「已完成/已更新/已同步」必须附证据；输出格式反向强制验证。
- **Real-incident documentation / 真实事件记录** — the 0/451 fake-completion audit that triggered this method; the user's question 'how do you KNOW the AI will follow the rules?' answered by mechanism, not text; sync-obligation incident. 0/451 假完成审计、「怎么确认 AI 每次守规矩」的机制答案、联动同步被当可选项的教训。
- **Included scripts / 附带脚本** — `rule_health_check.py` (configurable vault path, optional transcript check module) + `pre-commit` hook. 体检脚本（路径可配置）+ 红绿灯钩子。

> Background / 背景：Built on 2026-08-10 after the user drove the 'soft→hard' evolution of the rule system; the SOUL.md slimming (5,387 → 4,018 chars) and the pre-commit hook were both verified in production before open-sourcing. / 2026-08-10 用户推动「软→硬」进化后构建；提示词瘦身（5,387→4,018 字）与钩子均在生产验证后开源。
