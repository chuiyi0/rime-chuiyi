# 吹衣带调拼音 1.2 验证

2026-10-21，使用 Windows 的 Rime 1.13.1 在独立目录编译并枚举候选。结果以 [windows-engine-verification.json](windows-engine-verification.json) 为准，构建断言见 [validation.json](validation.json)。

重点检查：

- iop4 按 i=1/5、o=2/3、p=4 分组。
- jian/qian/xian/yan 按新行码和 i 列编码；lv 使用 fi/fo/fp。
- 双字词第二音节轻声允许其他声调，桌子 vxzi/vxzo/vxzp 均命中。
- 单字不增加全声调别名；子 zp 不命中。
- 雷保留 le 读音，ly 不出现单字雷。
- 字典源文件不变，只对明确的雷 lei4 单字条目作生成时修正；其他原词条和权重保留。

构建报告和引擎报告对应当前版本。历史版本的测量不用于本版性能结论；候选顺序仍受词频、多音字和个人词库影响。

红米 K70／同文 3.3.12／Rime 1.17.0 已在手机本机生成四项编译文件；2,075 条映射与电脑一致，方案列表已切换1.2。未自动向聊天窗口输入测试文字，实际手机候选仍待用户试打。见 android-verification.json。

回车修复：Return 与 KP_Enter 均显式绑定 commit_raw_input。Windows 原生引擎测试 58/58，通过英文原样上屏、空输入回车透传、空格选择中文及完整单字检查。尚未在具体应用输入框内验证。
