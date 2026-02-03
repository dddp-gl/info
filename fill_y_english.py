import csv
from pathlib import Path

TARGET = Path('fa-jp----.csv')
MAPPING = Path('fa-jp---- copy.csv')

# Build mappings from the copy file (which contains English names).
pref_code_to_en: dict[int, str] = {}
ja_muni_to_en: dict[str, str] = {}

MUNI_SUFFIXES = ('市', '区', '町', '村')

with MAPPING.open('r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)

    # Expected columns in mapping file
    idx_x2 = header.index('x2')
    idx_x2Name = header.index('x2Name')
    idx_x3Name = header.index('x3Name')
    idx_x4Name = header.index('x4Name')

    pending_muni_ja: str | None = None

    for row in reader:
        if not row:
            continue
        # pad
        if len(row) < len(header):
            row = row + [''] * (len(header) - len(row))

        x2 = row[idx_x2].strip()
        x2_en = row[idx_x2Name].strip()
        muni_en = row[idx_x3Name].strip()
        muni_ja = row[idx_x4Name].strip()

        if x2 and x2_en:
            try:
                pref_code_to_en[int(x2)] = x2_en
            except ValueError:
                pass

        # Municipality mapping: Japanese name -> English name.
        # The mapping CSV is not fully consistent:
        # - Sometimes muni_en and muni_ja are on the same row (aligned).
        # - Sometimes muni_en appears on the NEXT row (shifted by one).
        # We handle both by keeping a pending Japanese municipality name.

        # If we have a pending Japanese name and we see an English name, bind them.
        if pending_muni_ja and muni_en:
            ja_muni_to_en.setdefault(pending_muni_ja, muni_en)

            if '郡' in pending_muni_ja and (pending_muni_ja.endswith('町') or pending_muni_ja.endswith('村')):
                short = pending_muni_ja.split('郡', 1)[1]
                if short:
                    ja_muni_to_en.setdefault(short, muni_en)

            pending_muni_ja = None

        # If this row is aligned (both present), map directly.
        if muni_ja and muni_en and muni_ja.endswith(MUNI_SUFFIXES):
            ja_muni_to_en.setdefault(muni_ja, muni_en)
            if '郡' in muni_ja and (muni_ja.endswith('町') or muni_ja.endswith('村')):
                short = muni_ja.split('郡', 1)[1]
                if short:
                    ja_muni_to_en.setdefault(short, muni_en)

            pending_muni_ja = None
        elif muni_ja and muni_ja.endswith(MUNI_SUFFIXES) and not muni_en:
            # Start (or continue) a shifted sequence: store Japanese and wait for next English.
            pending_muni_ja = muni_ja
        elif muni_ja and muni_ja.endswith(MUNI_SUFFIXES) and muni_en:
            # Ambiguous (could be shifted): if we didn't map above, keep muni_ja as pending for next.
            # This helps sequences like: [青森市] -> Aomori, and keep [弘前市] pending for Hirosaki.
            pending_muni_ja = muni_ja

# Read target file
with TARGET.open('r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    target_header = next(reader)
    target_rows = list(reader)

# Ensure y1,y2,y3 exist
for col in ['y1', 'y2', 'y3']:
    if col not in target_header:
        target_header.append(col)

idx_x2_t = target_header.index('x2')
idx_x2Name_t = target_header.index('x2Name') if 'x2Name' in target_header else None
idx_x3Name_t = target_header.index('x3Name') if 'x3Name' in target_header else None
idx_y1 = target_header.index('y1')
idx_y2 = target_header.index('y2')
idx_y3 = target_header.index('y3')

updated = 0
filled_y2 = 0
filled_y3 = 0
missing_y3_samples: list[str] = []

out_rows: list[list[str]] = []

for row in target_rows:
    if not row:
        out_rows.append(row)
        continue

    if len(row) < len(target_header):
        row = row + [''] * (len(target_header) - len(row))

    # y1: always Japan
    row[idx_y1] = 'Japan'

    # y2: prefecture in English via x2 code
    x2_raw = row[idx_x2_t].strip()
    pref_en = ''
    if x2_raw:
        try:
            pref_en = pref_code_to_en.get(int(x2_raw), '')
        except ValueError:
            pref_en = ''
    row[idx_y2] = pref_en
    if pref_en:
        filled_y2 += 1

    # y3: municipality in English via Japanese municipality name (x3Name)
    muni_ja = ''
    if idx_x3Name_t is not None:
        muni_ja = row[idx_x3Name_t].strip()

    muni_en = ''
    if muni_ja:
        muni_en = ja_muni_to_en.get(muni_ja, '')
        if not muni_en and len(missing_y3_samples) < 20:
            missing_y3_samples.append(muni_ja)
    row[idx_y3] = muni_en
    if muni_en:
        filled_y3 += 1

    out_rows.append(row)
    updated += 1

with TARGET.open('w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(target_header)
    writer.writerows(out_rows)

print('Done: wrote y1,y2,y3 English names')
print(f'Rows processed: {updated}')
print(f'y2 (prefecture) filled: {filled_y2}')
print(f'y3 (municipality) filled: {filled_y3}')
if missing_y3_samples:
    print('Sample municipalities without mapping (first 20):')
    for s in missing_y3_samples:
        print(' - ' + s)
