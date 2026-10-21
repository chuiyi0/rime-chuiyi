"""Quickly inspect the read-only source dictionary using paths relative to this repository."""
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "chuiyi_1" / "chuiyi_dicts" / "base.dict.yaml"
lines = SOURCE.read_text(encoding="utf-8-sig").splitlines()
body = False
rows = []
for line in lines:
    if line.strip() == "...":
        body = True
        continue
    if not body or not line or line.startswith("#"):
        continue
    parts = line.split("\t")
    if len(parts) != 3:
        continue
    word, phones, weight = parts
    if weight.isdigit():
        rows.append((word, phones, int(weight)))
print("rows", len(rows), "unique word+phones", len(set((w, p) for w, p, _ in rows)))
print("weight counts top", Counter(weight for _, _, weight in rows).most_common(20))
for word in [
    "我们", "你好", "中国", "现在", "因为", "怎么", "可以", "不是", "一下",
    "今天", "明天", "时间", "问题", "输入法", "电脑", "手机", "工作", "学习",
    "没有", "已经", "需要", "然后", "如果", "觉得", "朋友", "谢谢", "再见",
    "大家", "这个", "那个", "什么", "为什么", "一个", "一起", "不要", "应该",
    "知道", "非常", "感觉", "继续"
]:
    matches = [(phones, weight) for w, phones, weight in rows if w == word]
    if matches:
        print(word, matches[:3])
