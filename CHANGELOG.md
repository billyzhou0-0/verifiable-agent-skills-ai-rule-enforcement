# Changelog（更新记录）

## Open-source release / 开源发布

- Make AI follow rules by mechanism, not by asking: zero-cost health-check script (naming/sync/sensitive/frontmatter/transcript), pre-commit red-light hook, prompt-layer slimming design. / 让 AI 守规矩靠机制不靠自觉：零成本体检脚本（命名/同步/敏感/frontmatter/凭证）、提交前红绿灯钩子、提示词瘦身设计。

## Initial version / 最初版本

- Paper rules were not enforced — a checklist said "add a field to 10,000+ records," the audit found 0 landed: the method was described, the code never executed. Fix: a machine-enforcement layer — a zero-cost health-check script (five checks with evidence) + a git pre-commit red-light hook (violations physically block commits). / 纸面规矩不被执行——治理清单写「给 10,000+ 条记录加字段」，审计发现实际 0 条落地：方法描述了，代码从未执行。修复：机器强制层——零成本体检脚本（五项检查附证据）+ git 提交前红绿灯钩子（违规物理阻止提交）。

## Second update / 第二次更新

- AI compliance is probabilistic (text rules ~80%, lower after context compression) → a prompt-layer slimming design (system prompt cut 25%: the less you inject, the higher the compliance); output-assertion discipline (every "updated/done/synced" claim ships with a path + line number or script output). / AI 遵守率是概率性的（文字规矩约 80%、上下文压缩后更低）→ 注入层瘦身设计（系统提示词精简 25%：注入越少遵守率越高）；输出断言附证据原则（已更新/已完成/已同步必须附路径+行号或脚本输出）。

## Third update / 第三次更新

- Link-sync was once treated as optional → a hard rule: keeping references in sync is a duty, not a choice — the health-check script scans for stale names/paths directly. / 联动同步被当可选项 → 新增铁律：联动更新是义务不是选项，体检脚本直接检查旧名/旧路径残留。
