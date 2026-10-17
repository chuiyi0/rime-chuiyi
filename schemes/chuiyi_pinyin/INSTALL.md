# 安装：吹衣带调拼音 1.0-dev

ZIP 安装包内已有生成好的词库。若从 GitHub 克隆源码，先在仓库根目录运行 `python schemes/chuiyi_pinyin/tools/build.py` 生成词库和 ZIP；仓库避免重复保存大词库。

先备份 Rime 用户目录。不要删除旧方案、用户词典或 build 目录。

## Windows 小狼毫

1. 右击输入法托盘图标 → 用户文件夹。
2. 将以下三项复制到用户目录根部：
   - `chuiyi_pinyin.schema.yaml`
   - `chuiyi_pinyin.dict.yaml`
   - 整个 `chuiyi_pinyin_dicts` 文件夹
3. 编辑已有 `default.custom.yaml`。在其 `patch` 下的 `schema_list` 中保留原有项目，再增加 `- schema: chuiyi_pinyin`。不要重复创建 patch 或覆盖原方案列表。若没有该文件，可参考：

```yaml
patch:
  schema_list:
    - schema: chuiyi_1
    - schema: chuiyi_pinyin
```

如果没安装旧方案，应只列出本机已有的方案。

4. 托盘右键 → 重新部署。通过方案选单选择「吹衣带调拼音 1.0-dev」。
5. 测试 `mama` → 妈妈、`mwmw` → 妹妹、`bxbx` → 爸爸、`womf` → 我们。候选不保证排在第一位。

## Android 中州韵 / 同文（Rime 客户端）

1. 打开客户端设置，确认其用户资料目录或使用客户端提供的方案导入功能；路径随客户端版本变化，不假设固定目录。
2. 将上述两份 YAML 和整个词库文件夹放入用户资料目录根部，维持目录层级。
3. 按 Windows 部分的方法将 `chuiyi_pinyin` 追加到已有方案列表，重新部署并选择新方案。
4. 使用拼音字母键盘测试上面的编码。此包不包含独立 Android APK，也不更改客户端键盘布局；需实机检查字母键盘行为。

## 回退

切回原来方案即可。新版有独立用户词典，不会接管旧方案的学习记录。若不再使用，在方案列表移除新版这一项即可。

## 当前验证范围

静态验证及可用的 Rime 引擎结果见 TESTING.md。Windows 正在使用的输入法与 Android 实机尚未验证，不能把引擎测试当作这两项已通过。
