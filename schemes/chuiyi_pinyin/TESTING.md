# 常规版 1.3 测试记录

## 已完成（2026-11-17）

**打包检查**（`tools/build.py`，结果见 [validation.json](validation.json)）

- 49 条编码断言全部通过，包括这次改动的 被 `bt`、借 `jt`、顿 `dy`、论 `ly`、军 `jy`、得 `dt`、乐 `lt`。
- 和 1.2 逐音节对比：只有 e/ei/ie 的四声（44 个读音）和 un（85 个读音）改变，其余 1,946 个读音的编码完全不变。
- 跨音节同码的组数和组成与 1.2 完全一样，没有新增重码。
- 词库源文件未被改动（SHA-256 校验一致），共 571,180 条。

**Rime 引擎实测**（`tools/verify_engine.py`，Linux librime 1.10，结果见 [engine-verification.json](engine-verification.json)）

- 在隔离目录里真实编译方案并逐个试打，50 / 50 项通过。
- 覆盖：被 `bt`、顿 `dy`、准 `vy`、谢谢 `xtxe`、论文 `lywf`、特别 `ttbe`，以及 1.2 原有的全部检查（i 三组声调、jian/qian/xian/yan、lü、er、双字词轻声放宽、单字不放宽等）。
- 确认 `lt` 不会打出单字「雷」（雷只保留 lei2 → `le`）。

## 待验证

- **Windows 小狼毫**：尚未在 Windows 上实测 1.3。可运行 `python tools/verify_windows.py --library <rime.dll 路径> --shared-data <共享数据目录>`。
- **安卓同文**：尚未在手机上部署 1.3。

候选顺序会受词频、多音字和个人用户词库影响，以上测试只检查「能不能打出来」，不代表每个字都排第一。

1.2 及更早版本的测试记录见 [docs/archive](../../docs/archive/)。
