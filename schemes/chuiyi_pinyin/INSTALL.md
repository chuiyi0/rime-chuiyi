# 安装与升级：吹衣带调拼音 1.1.1

[下载完整 ZIP](https://github.com/chuiyi0/rime-chuiyi/releases/download/v1.1.1/chuiyi_pinyin-1.1.1.zip)。这是 Rime 方案，不是独立 EXE/APK。

## Windows 小狼毫

1. 托盘图标右键 → 用户文件夹，先备份。
2. 解压复制 `chuiyi_pinyin_1_1.schema.yaml`、`chuiyi_pinyin_1_1.dict.yaml` 和整个 `chuiyi_pinyin_1_1_dicts/` 到用户目录根部。
3. 编辑已有 `default.custom.yaml`，将方案添加到 `patch.schema_list`。只使用本方案时的最小示例：

```yaml
patch:
  schema_list:
    - schema: chuiyi_pinyin_1_1
```

已有 patch 或方案列表时请合并，保留需要的其他方案，不要重复创建同名键。

4. 托盘右键 → 重新部署，通过 Ctrl+反引号或 F4 选择“吹衣带调拼音 1.1.1”。
5. 测试 `le→了；lw→鲁；lu→路；ly→乐；vozi/vozp→桌子；yifw/yifu→衣服`。候选顺序受词频影响。

## 升级与回退

1.1 → 1.1.1 沿用 `chuiyi_pinyin_1_1` 标识，替换文件后重新部署即可，用户词库沿用。

1.0-dev 和早期测试版使用其他标识。新版可用后，从方案列表移除不需要的 `chuiyi_pinyin` 或 `chuiyi_pinyin_test` 等旧项；用户词库建议备份保留。如果切换后仍使用旧规则，确认选中新版并重新启动小狼毫。

回退时恢复备份或选择原方案。本包不包含个人词频、用户词库、编译缓存或电脑路径。

## Android 中州韵 / 同文（Rime 客户端）

通过客户端设置查找用户资料目录或导入入口，复制上述文件、添加同一方案标识并重新部署。目录路径随版本变化。

此包不带 APK 或皮肤，不修改键盘布局。Android 实机兼容性尚未验收。
