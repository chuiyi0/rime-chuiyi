# 开发与打包

普通用户不需要看这一页，直接从 [首页](README.md) 下载 ZIP 就行。

只需要 Python 3，不用装任何第三方库。所有命令都在仓库根目录运行。

## 常规版 1.3

```bash
python schemes/chuiyi_pinyin/tools/build.py
```

- 输出 `dist/chuiyi_pinyin-1.3.zip`，同时重新生成方案文件、`MATRIX.md`、`mapping.tsv` 和 `validation.json`。
- **编码规则只在 `schemes/chuiyi_pinyin/tools/encoding.py` 里定义**。改键位就改这个文件，再重新打包。
- 版本号在 `build.py` 顶部的 `VERSION`，方案标识（如 `chuiyi_pinyin_1_3`）由它自动生成。升级版本时，还要同步修改 `.github/workflows/package-release.yml` 和 `.gitignore`。
- 词库来自 `schemes/chuiyi_1/chuiyi_dicts/`，打包时只读不写，并校验 SHA-256，确认源文件没被改过。

用真实 Rime 引擎验证：

```bash
# Linux（Ubuntu: apt install librime-bin librime-dev librime-data）
cd schemes/chuiyi_pinyin/tools
python verify_engine.py --library /usr/lib/x86_64-linux-gnu/librime.so.1 \
  --api-header /usr/include/rime_api.h --shared-data /usr/share/rime-data \
  --deployer /usr/bin/rime_deployer

# Windows（已安装小狼毫）
python verify_windows.py --library <rime.dll 路径> --shared-data <小狼毫 data 目录>
```

结果分别写入 `engine-verification.json` 和 `windows-engine-verification.json`。手机要在手机上自己部署，不要把电脑的编译缓存当成安卓测试结果。

## 轻量版 1.1.0

```bash
python schemes/chuiyi_pinyin_lite/tools/build.py
```

- 输出 `schemes/chuiyi_pinyin_lite/dist/chuiyi-pinyin-lite-1.1.0.zip`。
- **编码直接从 `MATRIX.md` 的表格读取**，零声母按 `ZERO_INITIALS.md` 覆盖。改这两个文件里的表格就会改变编码。
- `tools/check_privacy.py` 检查安装包里有没有混进个人数据。
- 方案标识保持 `chuiyi_pinyin_lite_1_0`（为了保留已有用户的学习记录），显示名称是 1.1.0。

## 自动发布

推送到 `main` 分支时，GitHub Actions 会自动打包并上传到对应的发布页：

| 工作流 | 触发条件 | 发布到 |
|---|---|---|
| `package-release.yml` | `schemes/chuiyi_pinyin/` 有改动 | `v1.3` |
| `package-lite-release.yml` | `schemes/chuiyi_pinyin_lite/` 有改动 | `lite-v1.1.0` |

## 安卓皮肤

见 [themes/trime/README.md](themes/trime/README.md)。改完皮肤后运行：

```bash
python themes/trime/tools/validate_palette_only.py
```

它会检查 12 套皮肤除了配色和名称之外是否和基础模板完全一致。

## 旧方案

`schemes/chuiyi_1/` 是最早的「吹衣带调双拼」，已不再更新，但常规版的词库从这里生成，所以不能删。`docs/research/` 里的统计针对旧方案，不代表当前版本的效果。
