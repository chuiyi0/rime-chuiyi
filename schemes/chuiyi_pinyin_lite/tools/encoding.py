"""Parse the author-provided light-scheme matrix and expose tone-aware double-pinyin codes."""
from collections import defaultdict
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MATRIX_FILE = ROOT / "MATRIX.md"


def _clean_cell(value):
    return value.replace("\u3000", "").strip()


def load_matrix():
    rows = []
    for line in MATRIX_FILE.read_text(encoding="utf-8-sig").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [_clean_cell(x) for x in line.strip().strip("|").split("|")]
        if cells and all(not c or set(c) <= {"-", ":", " "} for c in cells):
            continue
        rows.append(cells)
    if len(rows) < 3:
        raise ValueError("No complete matrix table found")
    top, finals = rows[0], rows[1]
    if len(top) != 32 or len(finals) != 32:
        raise ValueError(f"Expected 32 cells in header rows; got {len(top)} and {len(finals)}")
    final_labels = finals[2:]
    specs = []
    inherited = ""
    for raw in top[2:]:
        if raw:
            inherited = raw
        if not inherited:
            raise ValueError("A blank final-key header has no key to inherit")
        spec = re.sub(r"4$", "", inherited)
        if not spec or len(spec) not in (1, 2) or not spec.isalpha():
            raise ValueError(f"Unsupported final key spec {inherited!r}")
        specs.append(spec)
    if len(final_labels) != 30 or len(specs) != 30:
        raise ValueError("Expected 32 final columns")
    syllables = defaultdict(list)
    row_labels = []
    for row_number, row in enumerate(rows[2:], start=3):
        if len(row) != 32:
            raise ValueError(f"Matrix row {row_number} has {len(row)} cells, expected 32: {row[:3]}")
        initial_key, actual_initial = row[0], row[1]
        if not initial_key or not actual_initial:
            raise ValueError(f"Missing initial key in row {row_number}")
        row_labels.append((initial_key, actual_initial))
        for index, cell in enumerate(row[2:]):
            if not cell:
                continue
            for spelling in cell.split("/"):
                spelling = spelling.strip()
                if not spelling:
                    continue
                spec = specs[index]
                for tone in range(1, 6):
                    second = spec[1] if len(spec) == 2 and tone == 4 else spec[0] if len(spec) == 2 else spec
                    code = initial_key + second
                    syllables[spelling + str(tone)].append({
                        "code": code, "final": final_labels[index], "initial_key": initial_key,
                        "actual_initial": actual_initial, "column_index": index, "spec": spec
                    })
    # Version 1.1.0: Xiaohe-style zero-initial syllables override the archived matrix.
    zero_initials = {
        "a": "aa", "e": "ee", "o": "oo", "ai": "ai", "ei": "ei",
        "ao": "ao", "ou": "ou", "an": "an", "en": "en", "er": "er",
        "ang": "ah", "eng": "eg", "ong": "os",
    }
    for spelling, code in zero_initials.items():
        for tone in range(1, 6):
            phone = spelling + str(tone)
            if phone in syllables:
                syllables[phone] = [dict(syllables[phone][0], code=code)]
    mapping = {}
    aliases = {}
    duplicate_sources = {}
    for phone, entries in sorted(syllables.items()):
        codes = list(dict.fromkeys(x["code"] for x in entries))
        mapping[phone] = codes[0]
        if len(codes) > 1:
            aliases[phone] = codes[1:]
            duplicate_sources[phone] = entries
    return {
        "rows": rows, "final_labels": final_labels, "specs": specs,
        "syllables": syllables, "mapping": mapping, "aliases": aliases,
        "duplicate_sources": duplicate_sources, "row_labels": row_labels
    }


def code(phone):
    data = load_matrix()
    try:
        return data["mapping"][phone]
    except KeyError:
        raise ValueError(f"Unmapped pinyin syllable: {phone}") from None


if __name__ == "__main__":
    data = load_matrix()
    print("initial_rows:", len(data["row_labels"]))
    print("final_columns:", len(data["final_labels"]))
    print("pinyin_tone_mappings:", len(data["mapping"]))
    print("same-syllable alternate codes:", len(data["aliases"]))
    for phone, codes in sorted(data["aliases"].items()):
        if phone.endswith("1"):
            print(phone, data["mapping"][phone], *codes)
