import csv
from pathlib import Path

TARGET = Path('fa-jp----.csv')
MAPPING = Path('fa-jp---- copy.csv')

MUNI_SUFFIXES = ('市', '区', '町', '村')

# Build mapping: English municipality name -> Japanese municipality name.
# We do NOT use x3Name from the target file.
en_to_ja: dict[str, str] = {}

def finalize_block(block_rows: list[tuple[str, str]]) -> None:
    """block_rows: list of (muni_en, muni_ja) for a prefecture."""
    # Detect whether this prefecture block is aligned or shifted.
    # Heuristic: if the first municipality-like Japanese name exists but English is empty -> shifted.
    first_muni = None
    for muni_en, muni_ja in block_rows:
        if muni_ja and muni_ja.endswith(MUNI_SUFFIXES):
            first_muni = (muni_en, muni_ja)
            break

    is_shifted = bool(first_muni and not first_muni[0] and first_muni[1])

    if is_shifted:
        prev_ja = ''
        for muni_en, muni_ja in block_rows:
            if muni_en and prev_ja:
                en_to_ja.setdefault(muni_en, prev_ja)
            if muni_ja:
                prev_ja = muni_ja
    else:
        for muni_en, muni_ja in block_rows:
            if muni_en and muni_ja:
                en_to_ja.setdefault(muni_en, muni_ja)


with MAPPING.open('r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    idx_x3 = header.index('x3')
    idx_en = header.index('x3Name')   # English municipality name
    idx_ja = header.index('x4Name')   # Japanese municipality name

    current_block: list[tuple[str, str]] = []

    for row in reader:
        if not row:
            continue
        if len(row) < len(header):
            row = row + [''] * (len(header) - len(row))

        x3 = (row[idx_x3] or '').strip()
        muni_en = (row[idx_en] or '').strip()
        muni_ja = (row[idx_ja] or '').strip()

        # Prefecture header row: x3 is empty. Start a new block.
        # Some prefectures also place the FIRST municipality Japanese name in x4Name on this header row.
        if x3 == '':
            if current_block:
                finalize_block(current_block)
                current_block = []

            if muni_ja:
                current_block.append(('', muni_ja))
            continue

        current_block.append((muni_en, muni_ja))

    if current_block:
        finalize_block(current_block)

with TARGET.open('r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames or [])
    rows = list(reader)

if 'z3' not in fieldnames:
    fieldnames.append('z3')

updated = 0
missing = 0

for row in rows:
    y3 = (row.get('y3') or '').strip()
    if y3:
        z3 = en_to_ja.get(y3, '')
        if not z3:
            missing += 1
        if row.get('z3') != z3:
            row['z3'] = z3
            updated += 1
    else:
        # keep z3 empty for non-municipality rows
        if (row.get('z3') or '') != '':
            row['z3'] = ''
            updated += 1

with TARGET.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)

print('Done: filled z3 from y3 (English name) using mapping CSV')
print(f'Rows updated: {updated}')
print(f'Municipality rows with y3 but no mapping for z3: {missing}')
