"""Build the independent lightweight scheme from MATRIX.md and the existing dictionary source.

All generated files stay inside this scheme directory. Existing schemes and dictionaries are read-only.
"""
from collections import defaultdict
from pathlib import Path
import csv
import hashlib
import json
import re
from encoding import load_matrix

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "chuiyi_1" / "chuiyi_dicts"
SCHEMA_SOURCE = ROOT.parent / "chuiyi_1" / "chuiyi_1.schema.yaml"
SCHEMA_ID = "chuiyi_pinyin_lite_1_0"
DICT_DIR_NAME = SCHEMA_ID + "_dicts"
VERSION = "1.1.0"


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    data = load_matrix()
    mapping = data["mapping"]  # pinyin+tone -> two-key code
    assert len(mapping) == 2040, f"Expected 2040 tone mappings, got {len(mapping)}"
    assert len(data["row_labels"]) == 24
    assert len(data["final_labels"]) == 30
    if not SCHEMA_SOURCE.is_file():
        raise FileNotFoundError(f"Read-only base schema not found: {SCHEMA_SOURCE}")
    if not list(SOURCE.glob("*.dict.yaml")):
        raise FileNotFoundError(f"Read-only source dictionaries not found: {SOURCE}")

    # Rime algebra maps dictionary spellings to accepted input spellings.
    # Derive alternate codes before consuming each original phone.
    code_to_phones = defaultdict(set)
    rules = []
    for phone, entries in sorted(data["syllables"].items()):
        codes = list(dict.fromkeys(e["code"] for e in entries))
        for code in codes:
            code_to_phones[code].add(phone)
        for code in codes[1:]:
            rules.append(f"    - 'derive/^{phone}$/{code}/'")
        rules.append(f"    - 'xform/^{phone}$/{codes[0]}/'")

    schema = SCHEMA_SOURCE.read_text(encoding="utf-8-sig")
    schema = re.sub(r"(?m)^  schema_id:.*$", f"  schema_id: {SCHEMA_ID}", schema, count=1)
    schema = re.sub(r"(?m)^  name:.*$", f"  name: 吹衣带调拼音轻量版 {VERSION}", schema, count=1)
    schema = re.sub(r"(?m)^  version:.*$", f'  version: "{VERSION}"', schema, count=1)
    schema = re.sub(r"(?m)^  description:.*$", '  description: "基于小鹤双拼布局的自定义带调双拼；第四声使用指定替代键"', schema, count=1)
    start = schema.index("  algebra:\n") + len("  algebra:\n")
    end = schema.index("\ntranslator:", start)
    schema = schema[:start] + "\n".join(rules) + schema[end:]
    schema = schema.replace("dictionary: chuiyi_1", f"dictionary: {SCHEMA_ID}")
    schema = schema.replace("prism: chuiyi_1", f"prism: {SCHEMA_ID}")
    schema = schema.replace("user_dict: chuiyi_1", f"user_dict: {SCHEMA_ID}")
    schema = re.sub(r"(?m)^#.*\n", "", schema)
    schema += (
        "\n# 轻量版 1.1.0：保留 MATRIX.md 原始记录，零声母按 ZERO_INITIALS.md 覆盖。\n"
        "# speller algebra 将词库带调拼音转换为可输入的双键编码，并保留原矩阵多码。\n"
    )
    schema_path = ROOT / f"{SCHEMA_ID}.schema.yaml"
    schema_path.write_text(schema, encoding="utf-8")

    master_dict = (
        "# Independent dictionary entry for Chuiyi Pinyin Lite.\n---\n"
        f"name: {SCHEMA_ID}\nversion: \"{VERSION}\"\nsort: by_weight\n"
        "import_tables:\n"
        f"  - {DICT_DIR_NAME}/chars\n"
        f"  - {DICT_DIR_NAME}/base\n"
        "...\n"
    )
    (ROOT / f"{SCHEMA_ID}.dict.yaml").write_text(master_dict, encoding="utf-8")

    target = ROOT / DICT_DIR_NAME
    target.mkdir(exist_ok=True)
    sources = [SCHEMA_SOURCE, *sorted(SOURCE.glob("*.dict.yaml"))]
    source_hashes = {str(p.relative_to(ROOT.parents[1])): sha256(p) for p in sources}
    total_rows = 0
    omitted_rows = 0
    omitted_syllables = defaultdict(int)
    dictionary_outputs = {}
    for source in sorted(SOURCE.glob("*.dict.yaml")):
        text = source.read_text(encoding="utf-8-sig")
        header, sep, body = text.partition("\n...\n")
        if not sep:
            raise ValueError(f"Dictionary header separator missing: {source.name}")
        header = re.sub(r"(?m)^name:.*$", f"name: {DICT_DIR_NAME}/{source.name.removesuffix('.dict.yaml')}", header, count=1)
        header = re.sub(r"(?m)^version:.*$", f'version: "{VERSION}"', header, count=1)
        output = []
        seen = set()
        kept = 0
        for line_no, line in enumerate(body.splitlines(), start=1):
            if not line or line.startswith("#"):
                if line:
                    output.append(line)
                continue
            parts = line.split("\t")
            if len(parts) != 3:
                raise ValueError(f"Malformed row in {source.name}:{line_no}: expected 3 tab fields")
            word, phones_text, weight = parts
            phones = phones_text.split()
            missing = sorted(set(phones) - mapping.keys())
            if missing:
                omitted_rows += 1
                for phone in missing:
                    omitted_syllables[phone] += 1
                continue
            key = (word, phones_text)
            if key in seen:
                continue
            seen.add(key)
            output.append(line)
            kept += 1
        destination = target / source.name
        destination.write_text(header + sep + "\n".join(output) + "\n", encoding="utf-8")
        total_rows += kept
        dictionary_outputs[source.name] = {
            "rows_kept": kept,
            "size_bytes": destination.stat().st_size,
            "sha256": sha256(destination),
        }

    with (ROOT / "mapping.tsv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["pinyin_tone", "primary_code", "alternate_codes"])
        for phone, code in sorted(mapping.items()):
            writer.writerow([phone, code, ",".join(sorted({e["code"] for e in data["syllables"][phone]} - {code}))])

    # Small, representative checks only; preserve all author-defined collisions.
    sample_expected = {
        "yi1": "yi", "yi4": "yp", "wu1": "ww", "wu4": "wu",
        "e1": "ee", "e4": "ee", "bei1": "be", "bei4": "by",
        "ju1": "jw", "ju4": "ju", "qu1": "qw", "qu4": "qu",
        "xu1": "xw", "xu4": "xu", "yu1": "yw", "yu4": "yu",
        "er2": "er", "er4": "er", "nve4": "no", "lve4": "lo",
        "an4": "an", "xia4": "xx", "wo3": "wo",
    }
    for phone, expected in sample_expected.items():
        actual = mapping.get(phone)
        if actual != expected:
            raise AssertionError(f"Sample mapping {phone}: expected {expected}, got {actual}")

    # Check sampled many-to-many mappings without changing matrix assignments.
    inverse = {code: phones for code, phones in code_to_phones.items()}
    inverse_samples = {
        "yp": "yi4", "wu": "wu4", "ee": "e4", "by": "bei4",
        "jw": "ju1", "ju": "ju4", "jv": "ju4", "er": "er4",
        "no": "nve4", "lo": "lve4", "an": "an4", "xx": "xia4",
    }
    for code, phone in inverse_samples.items():
        if phone not in inverse.get(code, set()):
            raise AssertionError(f"Sample inverse mapping {code} -> {phone} missing")

    collision_codes = {code: sorted(phones) for code, phones in code_to_phones.items() if len(phones) > 1}
    report = {
        "name": "吹衣带调拼音轻量版",
        "version": VERSION,
        "schema_id": SCHEMA_ID,
        "matrix_initial_rows": len(data["row_labels"]),
        "matrix_final_columns": len(data["final_labels"]),
        "pinyin_tone_mappings": len(mapping),
        "distinct_input_codes": len(code_to_phones),
        "same_code_multiple_readings": len(collision_codes),
        "sample_mapping_checks": len(sample_expected),
        "sample_inverse_checks": len(inverse_samples),
        "dictionary_rows_kept": total_rows,
        "dictionary_rows_omitted_for_unmapped_syllables": omitted_rows,
        "omitted_syllables_top20": sorted(omitted_syllables.items(), key=lambda x: (-x[1], x[0]))[:20],
        "dictionary_outputs": dictionary_outputs,
        "source_sha256_before": source_hashes,
        "source_unchanged": all(sha256(p) == source_hashes[str(p.relative_to(ROOT.parents[1]))] for p in sources),
        "rime_runtime_test": "see windows-smoke.json and android-smoke.json when present",
    }
    (ROOT / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    import zipfile
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    with zipfile.ZipFile(dist / "chuiyi-pinyin-lite-1.1.0.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        files = [*ROOT.glob("*.yaml"), *ROOT.glob("*.md"), ROOT/"mapping.tsv", ROOT/"validation.json", *target.glob("*.dict.yaml")]
        files += [p for p in [ROOT/"windows-smoke.json", ROOT/"android-smoke.json"] if p.exists()]
        for file in files:
            archive.write(file, file.relative_to(ROOT))
        for file in [ROOT.parents[1]/"LICENSE", ROOT.parents[1]/"NOTICE.md"]:
            if file.exists():archive.write(file, "licenses/"+file.name)
        for file in (ROOT.parents[1]/"LICENSES").glob("*"):
            if file.is_file():archive.write(file, "LICENSES/"+file.name)
    print(json.dumps({
        "schema": str(schema_path),
        "dictionary_entry": str(ROOT / f"{SCHEMA_ID}.dict.yaml"),
        "matrix_mappings": len(mapping),
        "input_codes": len(code_to_phones),
        "multi_reading_codes": len(collision_codes),
        "sample_mapping_checks_passed": len(sample_expected),
        "sample_inverse_checks_passed": len(inverse_samples),
        "dictionary_rows_kept": total_rows,
        "dictionary_rows_omitted": omitted_rows,
        "source_unchanged": report["source_unchanged"],
        "output_files_all_within_scheme_dir": True,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
