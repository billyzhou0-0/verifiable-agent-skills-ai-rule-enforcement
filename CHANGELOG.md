# Changelog（更新记录）

All notable changes to this project are documented here, following Keep a Changelog with semver versioning. / 本文件按 Keep a Changelog 规范记录本项目所有重要变更。

## [1.0.0] - 2026-08-11

### Initial open-source release / 初始开源发布

- Make AI follow rules by mechanism, not by asking: zero-cost health-check script (naming/sync/sensitive-info/frontmatter/transcript), git pre-commit hook that blocks violations, injection-layer slimming design. / 让 AI 守规矩靠机制：零成本体检脚本（命名/同步/敏感/frontmatter/凭证）、提交前红绿灯钩子、提示词瘦身设计。

## Pre-release evolution（开源前演进史）

Each fix below was proven in real production. / 以下每条修复均在真实生产中验证。

### 1. 纸面规矩不被执行

- **Fix / 修复**：治理清单写「给 451 条记录加字段」，审计发现 0 条落地——方法描述了，代码从未执行。修复：声称落地必验 + 机器强制层（体检脚本+提交前钩子，违规物理阻止提交）。

### 2. AI 遵守率是概率性的

- **Fix / 修复**：文字规矩遵守率约 80%，上下文压缩后更低。修复：三层架构——0 成本体检脚本（五项检查附证据）、git 红绿灯钩子、注入层瘦身（系统提示词 -25%，注入越少遵守率越高）。

### 3. 输出断言无法验证

- **Fix / 修复**：「已更新/已完成/已同步」全靠自觉。修复：输出断言附证据原则（路径+行号/脚本输出）；输出格式反向强制验证——报告必须含检查结果时 AI 必须先跑检查。

### 4. 联动同步被当可选项

- **Fix / 修复**：改名后同步引用曾被当选项询问。修复：联动同步是义务不是选项，体检脚本直接检查旧名/旧路径残留。
