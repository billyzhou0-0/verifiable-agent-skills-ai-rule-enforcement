#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rule_health_check.py — AI 规矩体检（0 token，本地脚本）
用法: python3 rule_health_check.py [--vault <路径>] [--fix]
检查项:
  1. 命名格式（AI名-事项-日期，日期在末尾）
  2. 引用同步（旧文件名/旧路径残留）
  3. 敏感信息（API key/token 格式，只报告不处理）
  4. frontmatter 完整性
  5. 凭证转录（可选：检测到对话数据库时，对比今天的用户消息 vs 转录档案）
输出: 每项 ✅/❌ + 证据（路径+行数），可直接粘贴进汇报
"""
import os, re, sys, datetime, argparse

EXCLUDE_DIRS = {'.git', '.obsidian', 'node_modules', '__pycache__', '归档'}
# 豁免名单（按需修改）：
# - 第三方源码目录：非本库产出，不归我们管
# - 收件箱：验收后才补 frontmatter，缺是正常
# - 历史转录：按历史不动原则豁免
EXEMPT_PREFIX = ()
EXEMPT_SUBDIRS = ('/收件箱/', '/对话原始凭证/')
EXEMPT_FILES = {'AGENTS.md', 'INDEX.md', 'README.md', 'STRUCTURE.md', '00_说明.md'}
EXEMPT_NAME_PATTERNS = ('00_说明.md', 'README.md')
SENSITIVE_PATTERNS = [
    (r'sk-[A-Za-z0-9]{20,}', 'OpenAI API Key'),
    (r'AIza[A-Za-z0-9_-]{20,}', 'Google API Key'),
    (r'ghp_[A-Za-z0-9]{20,}', 'GitHub Token'),
    (r'AKIA[A-Z0-9]{16}', 'AWS Key'),
    (r'xox[baprs]-[A-Za-z0-9-]{10,}', 'Slack Token'),
    (r'Bearer\s+[A-Za-z0-9._-]{20,}', 'Bearer Token'),
]

results = []

def report(ok, item, evidence=''):
    results.append((ok, item, evidence))

def walk_md(root):
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in EXCLUDE_DIRS]
        for f in fns:
            if f.endswith('.md'):
                yield os.path.join(dp, f)

def check_naming(vault):
    """1. 命名格式：日期在末尾（排除归档层）"""
    bad = []
    for p in walk_md(vault):
        if '/归档/' in p: continue
        if any(p.startswith(os.path.join(vault, x)) for x in EXEMPT_PREFIX): continue
        if any(s in p for s in EXEMPT_SUBDIRS): continue
        name = os.path.basename(p)
        if re.match(r'^\d{4}[-_]?\d{2}[-_]?\d{2}', name):
            bad.append(p)
    if bad:
        report(False, '命名格式：日期在末尾', f'发现 {len(bad)} 个日期开头的文件：{bad[0]} 等')
    else:
        report(True, '命名格式：日期在末尾', f'扫描 {vault} 全部 md，0 违规')

def check_sync(vault):
    """2. 引用同步：找旧名/旧路径残留（在此配置你的旧名清单）"""
    stale_markers = ['旧库路径/旧文件名示例']  # ← 按你的实际旧名修改
    hits = []
    for p in walk_md(vault):
        try:
            c = open(p, encoding='utf-8').read()
        except: continue
        for m in stale_markers:
            if m in c:
                hits.append((p, m))
    if hits:
        report(False, '引用同步', f'{len(hits)} 处旧路径残留：{hits[0]}')
    else:
        report(True, '引用同步', '0 处旧路径/旧名残留')

def check_sensitive(vault):
    """3. 敏感信息扫描（只报告，不处理——敏感判断权在用户）"""
    hits = []
    for p in walk_md(vault):
        try:
            c = open(p, encoding='utf-8').read()
        except: continue
        for pat, label in SENSITIVE_PATTERNS:
            for m in re.finditer(pat, c):
                ctx = c[max(0,m.start()-30):m.start()]
                if any(k in ctx for k in ('示例', 'example', 'placeholder', 'sk-xxx', '占位')):
                    continue
                hits.append((p, label))
                break
    if hits:
        report(False, '敏感信息', f'{len(hits)} 处疑似敏感（只报告不处理，请用户判断）：{hits[0]}')
    else:
        report(True, '敏感信息', '0 处疑似真实密钥（示例/占位/已知项已排除）')

def check_frontmatter(vault):
    """4. frontmatter 完整性：正式层文件应有 frontmatter"""
    missing = []
    for p in walk_md(vault):
        if '/归档/' in p: continue
        if any(p.startswith(os.path.join(vault, x)) for x in EXEMPT_PREFIX): continue
        if any(s in p for s in EXEMPT_SUBDIRS): continue
        name = os.path.basename(p)
        if name in EXEMPT_FILES: continue
        if name.endswith(EXEMPT_NAME_PATTERNS): continue
        try:
            c = open(p, encoding='utf-8').read()
        except: continue
        if not c.startswith('---'):
            missing.append(p)
    if missing:
        report(False, 'frontmatter 完整性', f'{len(missing)} 个缺 frontmatter：{missing[0]} 等')
    else:
        report(True, 'frontmatter 完整性', '全部合规')

def check_credential(vault):
    """5. 凭证检查（可选模块）：检测到对话数据库时，对比今天的用户消息 vs 转录档案"""
    # 不同 agent 的对话数据库路径不同——按需配置
    DB_CANDIDATES = [os.path.expanduser('~/.hermes/state.db')]
    db_path = next((p for p in DB_CANDIDATES if os.path.exists(p)), None)
    if not db_path:
        report(None, '凭证检查（可选）', '未检测到对话数据库，跳过（本检查为 Hermes 等本地 agent 专用）')
        return
    import sqlite3
    try:
        db = sqlite3.connect(db_path)
        start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        rows = db.execute("SELECT content FROM messages WHERE role='user' AND timestamp>=? ", (start,)).fetchall()
        db.close()
        today_msgs = [r[0] for r in rows if r[0] and not r[0].startswith(('[CONTEXT','[ASYNC','[IMPORTANT'))]
        sigs = set()
        for m in today_msgs:
            s = m.strip()[:20]
            if s: sigs.add(s)
    except Exception as e:
        report(None, '凭证检查', f'对话数据库读取失败（{e}），需人工确认')
        return
    if not sigs:
        report(True, '凭证检查', '今天尚无用户消息（或已过零点），无需转录')
        return
    found = 0
    for dp, dns, fns in os.walk(vault):
        for f in fns:
            if not f.endswith('.md'): continue
            try:
                content = open(os.path.join(dp, f), encoding='utf-8').read()
            except: continue
            for s in sigs:
                if s in content:
                    found += 1
    if found >= len(sigs) * 0.8:
        report(True, '凭证检查', f'今天 {len(sigs)} 条用户消息签名，凭证中已找到 {found} 条（≥80%）')
    else:
        report(False, '凭证检查', f'⚠️ 今天 {len(sigs)} 条用户消息签名，凭证中仅找到 {found} 条（<80%）——先转录再提交！')

def main():
    ap = argparse.ArgumentParser(description='AI 规矩体检（0 token 本地脚本）')
    ap.add_argument('--vault', default='.', help='治理根目录（默认当前目录）')
    ap.add_argument('--fix', action='store_true', help='（预留）自动修复可安全修复项')
    args = ap.parse_args()
    vault = os.path.abspath(args.vault)

    print('=' * 60)
    print('AI 规矩体检 — ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    print(f'治理根目录: {vault}')
    print('=' * 60)
    check_naming(vault)
    check_sync(vault)
    check_sensitive(vault)
    check_frontmatter(vault)
    report(None, '落位检查（需人工）', '产出放对位置了吗？（未验收→收件箱 / 提到过→ai暂存 / 用户明确要求→待办）')
    check_credential(vault)

    print()
    ok_n = sum(1 for ok,_,_ in results if ok)
    warn_n = sum(1 for ok,_,_ in results if ok is None)
    fail_n = sum(1 for ok,_,_ in results if ok is False)
    for ok, item, ev in results:
        mark = '✅' if ok else ('⚠️' if ok is None else '❌')
        print(f'{mark} {item}')
        print(f'   证据: {ev}')
    print()
    print(f'结论: {ok_n} 通过 / {warn_n} 需人工确认 / {fail_n} 未通过')
    if fail_n:
        print(f'❌ {fail_n} 项未通过——修复后再提交/汇报！')
        sys.exit(1)
    else:
        print('✅ 全部通过（含人工确认项）')

if __name__ == '__main__':
    main()
