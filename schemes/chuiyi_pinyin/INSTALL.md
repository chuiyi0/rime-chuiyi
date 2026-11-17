# 安装与升级：常规版 1.3

[下载 1.3 完整 ZIP](https://github.com/chuiyi0/rime-chuiyi/releases/download/v1.3/chuiyi_pinyin-1.3.zip)

这是 Rime 输入方案，不是独立的安装程序（EXE / APK）。请先装好小狼毫或同文输入法，**改动前先备份用户文件夹**。

## Windows 小狼毫

1. 右键任务栏的小狼毫图标 →「用户文件夹」。
2. 把 ZIP 里的 `chuiyi_pinyin_1_3.schema.yaml`、`chuiyi_pinyin_1_3.dict.yaml` 和整个 `chuiyi_pinyin_1_3_dicts` 文件夹复制进去。
3. 打开（或新建）`default.custom.yaml`，在 `schema_list` 里加上本方案：

   ```yaml
   patch:
     schema_list:
       - schema: chuiyi_pinyin_1_3
   ```

   已经有其他方案时，只加 `- schema: chuiyi_pinyin_1_3` 这一行，不要重复写 `patch:`。

4. 右键小狼毫图标 →「重新部署」，然后切换到「吹衣带调拼音 1.3」。
5. 试打：`lo` → 离 / 理，`lp` → 力，`go` → 简，`bt` → 被，`dy` → 顿，`vxzi` → 桌子。

## 安卓同文（Trime）

1. 在同文设置里找到用户目录（不同版本位置不同，一般叫 `rime`）。
2. 复制同样的三项文件，并按上面的方法修改 `default.custom.yaml`。
3. 在同文里点「部署」，再选择「吹衣带调拼音 1.3」。

手机要在手机上重新部署，不要把电脑上 `build` 文件夹里的编译结果复制过去。

可选：[安卓补丁](android/README.md)，只打第二个字的首字母（如 `wxm`）时也能出候选。

## 从 1.2 升级

1.3 把两个键对调了：

| | 1.2 | 1.3 |
|---|---|---|
| e / ei / ie 的四声 | `y`（被 `by`） | `t`（被 `bt`） |
| un | `t`（顿 `dt`） | `y`（顿 `dy`） |

其他编码完全不变。1.3 使用新的方案标识 `chuiyi_pinyin_1_3`，和 1.2 的用户词库分开，两个版本可以同时存在。确认 1.3 好用后，再从 `schema_list` 里删掉 `chuiyi_pinyin_1_2`。

想退回 1.2：把 `schema_list` 里的标识改回去，重新部署即可。1.2 的安装包仍在 [v1.2 发布页](https://github.com/chuiyi0/rime-chuiyi/releases/tag/v1.2)。

## 遇到问题

- **还是旧规则**：确认选的是「1.3」，然后重新部署，必要时重启输入法。
- **部署失败**：查看 Rime 的部署日志，不要清空用户文件夹。
- 安装包里不含皮肤、APK 和任何个人数据，也不会改动你的键盘布局和其他方案。
