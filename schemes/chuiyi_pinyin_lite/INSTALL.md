# 安装说明：吹衣带调拼音轻量版 1.1.0

方案 ID：`chuiyi_pinyin_lite_1_0`

## Windows 小狼毫

通过小狼毫托盘菜单打开“用户文件夹”，将方案文件放入该目录。

安装包包含以下文件：
- `chuiyi_pinyin_lite_1_0.schema.yaml`
- `chuiyi_pinyin_lite_1_0.dict.yaml`
- `chuiyi_pinyin_lite_1_0_dicts\base.dict.yaml`
- `chuiyi_pinyin_lite_1_0_dicts\chars.dict.yaml`

将文件放进小狼毫用户目录，保持词库子目录结构。然后在 `default.custom.yaml` 的 `patch.schema_list` 中加入：

```yaml
- {schema: chuiyi_pinyin_lite_1_0}
```

保留现有列表项；不要用上面的单行覆盖整个配置。右键小狼毫托盘图标，选择“重新部署”，再切换到“吹衣带调拼音轻量版 1.1.0”。

## Android 同文（Trime）

将同样的 schema、主词典和 `chuiyi_pinyin_lite_1_0_dicts` 目录复制到同文的 Rime 用户目录。将方案 ID 加入该目录的 `default.custom.yaml` 中现有 `schema_list`，重新部署并选择本方案。

## 安全

- 不删除或覆盖其他方案。
- 修改 `default.custom.yaml` 前先备份。
- 若部署失败，先查看 Rime 部署日志；不要清空用户目录。
