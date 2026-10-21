# 1.1.1 验证范围

2026-10-21，使用 Windows 小狼毫的 Rime 1.13.1 引擎：

- 465 组单字编码、8,986 条字音对应均能在候选中找到。
- 新表头、两个特例与零声母的独立断言通过。
- 桌子 vozi/vozp、孩子 hdzi/hdzp、衣服 yifw/yifu 等轻声词测试通过。
- 负向样例确认单字不因双字词轻声兼容而放宽。
- 已安装编译文件核对：le/lw/lu/ly 首项分别为了/鲁/路/乐。
- 作者在实际输入后确认“ok了”。

构建另外检查旧源字典不变、保留原词条与权重，新增读音仅来自双字词末字轻声。

测试不保证任意词语均已收录。候选排序受词频、多音字及用户词库影响。Android 实机未验收；历史 Linux 1.0-dev 报告不算本版 Linux 验证。

[构建报告](validation.json) · [Windows 引擎记录](windows-engine-verification.json)

开发者可在构建后运行 tools/verify_windows.py，以 --library 指定 rime.dll、--shared-data 指定默认数据目录。脚本在 local-validation 中编译，不修改已安装的输入法。
