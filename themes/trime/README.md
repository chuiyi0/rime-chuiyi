# 吹衣皮肤 · 同文输入法（Trime 3.3.12）

12 套配色皮肤，配合吹衣带调拼音使用（也能搭配其他 Rime 方案）。**所有皮肤的键盘布局完全一样，只换颜色**：键位、上滑、长按、分词键、数字键盘都相同。

[返回首页](../../README.md) · [快捷主题面板](QUICK_THEMES.md) · [更新记录](CHANGELOG.md)

## 12 套皮肤

| 编号 | 名称 | 风格 | 文件 |
|---|---|---|---|
| 01 | 云瓷白 | 小米原生感 · 柔和蓝 | `light/cy_01_cloud-white.trime.yaml` |
| 02 | 冰川蓝 | 清透科技 · 天空色 | `light/cy_02_glacier-blue.trime.yaml` |
| 03 | 奶杏 | 温暖柔软 · 低饱和 | `light/cy_03_cream-apricot.trime.yaml` |
| 04 | 薄荷茶 | 自然舒缓 · 奶油绿 | `light/cy_04_mint-tea.trime.yaml` |
| 05 | 石墨灰 | 克制专业 · 暗金点缀 | `dark/cy_05_graphite.trime.yaml` |
| 06 | 深海蓝 | 夜间使用 · 青蓝光 | `dark/cy_06_deep-sea.trime.yaml` |
| 07 | 樱花糖 | 轻柔可爱 · 暖粉 | `color/cy_07_sakura.trime.yaml` |
| 08 | 黑曜夜 | 极简黑 · 青柠亮色 | `dark/cy_08_obsidian.trime.yaml` |
| 09 | 清纸白 | 纯净留白 · 无阴影 | `light/cy_09_paper-white.trime.yaml` |
| 10 | 暮光紫 | 轻雾层次 · 冷色系 | `color/cy_10_dusk-purple.trime.yaml` |
| 11 | 琥珀纸 | 复古书写 · 暖纸感 | `color/cy_11_amber-paper.trime.yaml` |
| 12 | 雾玻璃 | 轻盈半透明感 · 软阴影 | `texture/cy_12_mist-glass.trime.yaml` |

「雾玻璃」只是用颜色和轮廓模拟玻璃感，并不是真正的实时背景模糊。

**先看效果：** 下载 [`showcase/index.html`](showcase/index.html)，用手机或电脑的浏览器打开，可以离线对比 12 套配色。网页只是示意，和手机上的实际显示会有细微差别。

## 安装

1. **先备份**手机上同文现有的皮肤文件。
2. 把想用的 `.trime.yaml` 复制到同文的**共享目录**（一般是 `Android/data/com.osfans.trime/files/shared/`）。这个目录不分子文件夹，直接放进去。
3. 打开同文 →「键盘样式」，选择「吹衣 · 编号 名称」。
4. 如果没生效，点「部署」；还不行就先切到别的皮肤再切回来。
5. 试一下打字、上滑、长按、数字键、符号键。有问题随时切回原来的皮肤。

## 键盘特点

- **空输入工具栏**：没打字时，候选栏位置显示菜单、编辑、剪贴板、表情、设置；开始打字后自动换成候选。
- **编辑键盘**：全选、剪切、复制、粘贴、移动光标、删除，并有返回键。
- **快捷主题面板**：点顶部 🎨 可以一键切换收藏的 8 套皮肤，见 [快捷主题面板](QUICK_THEMES.md)。
- 底部一行：符号 16%、123 14%、逗号 9.75%、空格 24%（显示「吹衣拼音」）、句号 9.75%、中/英 11%、回车 15.5%。
- 候选字号 19，候选栏高 42；按键横向间距 6、行距 11；数字键盘四行五列。
- 每行显示几个候选，由同文的应用设置决定，不由皮肤决定。

## 已知限制

- Trime 3.3.12 不支持让顶部左上角按钮随键盘页面变化。所以在编辑页、表情页里，返回键放在页面内部，左上角仍是菜单按钮。要彻底解决，需要修改同文的安卓源码并重新打包，皮肤文件做不到。
- 只打第二个字的首字母（如 `wxm`）时没有候选，这不是皮肤问题，可以装常规版的 [安卓补丁](../../schemes/chuiyi_pinyin/android/README.md)。
- 工具栏按钮和各套皮肤的显示还没有逐套在手机上完整验收。
- 目前 01、02、03、09 四套的空格键用自定义的 `cy_space`（和基础模板一致），其余 8 套用普通 `space`，所以 `validate_palette_only.py` 会报不一致。两种空格键显示都是「吹衣拼音」，待确认用哪种后统一。

## 给开发者

- 所有皮肤从 `base/chuiyi_layout_reference.trime.yaml` 生成，**只允许改配色和名称**。改完运行 `python themes/trime/tools/validate_palette_only.py` 检查。
- `manifest.json` 记录 12 套皮肤的配色数据，`showcase/index.html` 的预览从这里取色。
- `tools/update_favorites.py` 用来修改快捷主题面板的收藏，用法见 [QUICK_THEMES.md](QUICK_THEMES.md)。

## 版权

皮肤基于同文输入法及其 GPL-3.0 预设主题改编，保留原文件的署名和许可要求；用到的资源与字体仍受原许可约束。
