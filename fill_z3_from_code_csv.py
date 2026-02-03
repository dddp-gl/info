import csv
import unicodedata
from pathlib import Path

TARGET = Path('fa-jp----.csv')
CODE = Path('code.csv')

VOWELS = set('aeiou')


def _nfkc(s: str) -> str:
    return unicodedata.normalize('NFKC', s or '').strip()


KANJI_VARIANTS = str.maketrans({
    '惠': '恵',
    '檮': '梼',
})


def norm_name(s: str) -> str:
    return _nfkc(s).translate(KANJI_VARIANTS)


def kata_to_hira(text: str) -> str:
    out = []
    for ch in text:
        code = ord(ch)
        if 0x30A1 <= code <= 0x30F6:
            out.append(chr(code - 0x60))
        else:
            out.append(ch)
    return ''.join(out)


BASE = {
    'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
    'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
    'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
    'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
    'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
    'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
    'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
    'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
    'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
    'わ': 'wa', 'ゐ': 'wi', 'ゑ': 'we', 'を': 'o',
    'ん': 'n',

    'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
    'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
    'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
    'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
    'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',

    'ぁ': 'a', 'ぃ': 'i', 'ぅ': 'u', 'ぇ': 'e', 'ぉ': 'o',
    'ゎ': 'wa',
    'ゔ': 'vu',
}

DIGRAPH = {
    'きゃ': 'kya', 'きゅ': 'kyu', 'きょ': 'kyo',
    'ぎゃ': 'gya', 'ぎゅ': 'gyu', 'ぎょ': 'gyo',
    'しゃ': 'sha', 'しゅ': 'shu', 'しょ': 'sho',
    'じゃ': 'ja',  'じゅ': 'ju',  'じょ': 'jo',
    'ちゃ': 'cha', 'ちゅ': 'chu', 'ちょ': 'cho',
    'にゃ': 'nya', 'にゅ': 'nyu', 'にょ': 'nyo',
    'ひゃ': 'hya', 'ひゅ': 'hyu', 'ひょ': 'hyo',
    'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo',
    'ぴゃ': 'pya', 'ぴゅ': 'pyu', 'ぴょ': 'pyo',
    'みゃ': 'mya', 'みゅ': 'myu', 'みょ': 'myo',
    'りゃ': 'rya', 'りゅ': 'ryu', 'りょ': 'ryo',

    'ふぁ': 'fa', 'ふぃ': 'fi', 'ふぇ': 'fe', 'ふぉ': 'fo',
    'てぃ': 'ti', 'でぃ': 'di',
    'とぅ': 'tu', 'どぅ': 'du',
    'うぁ': 'wa', 'うぃ': 'wi', 'うぇ': 'we', 'うぉ': 'wo',
    'ゔぁ': 'va', 'ゔぃ': 'vi', 'ゔぇ': 've', 'ゔぉ': 'vo',
}


def kana_to_romaji(kana: str) -> str:
    s = _nfkc(kana)
    s = kata_to_hira(s)

    out: list[str] = []
    i = 0
    while i < len(s):
        ch = s[i]

        if ch == 'っ':
            nxt = ''
            if i + 1 < len(s):
                pair = s[i + 1:i + 3]
                if pair in DIGRAPH:
                    nxt = DIGRAPH[pair]
                else:
                    nxt = BASE.get(s[i + 1], '')
            if nxt.startswith('ch'):
                out.append('t')
            elif nxt:
                out.append(nxt[0])
            i += 1
            continue

        if ch == 'ー':
            if out:
                last = out[-1]
                for v in reversed(last):
                    if v in VOWELS:
                        out.append(v)
                        break
            i += 1
            continue

        pair = s[i:i + 2]
        if pair in DIGRAPH:
            out.append(DIGRAPH[pair])
            i += 2
            continue

        if ch == 'ん':
            nxt = ''
            if i + 1 < len(s):
                look = s[i + 1:i + 3]
                if look in DIGRAPH:
                    nxt = DIGRAPH[look]
                else:
                    nxt = BASE.get(s[i + 1], '')
            if nxt and (nxt[0] in VOWELS or nxt[0] == 'y'):
                out.append("n'")
            else:
                out.append('n')
            i += 1
            continue

        rom = BASE.get(ch)
        if rom is None:
            if ch.isspace() or ch in '・-－ー':
                i += 1
                continue
            out.append(ch)
        else:
            out.append(rom)
        i += 1

    return ''.join(out)


def strip_admin_suffix(romaji: str, kanji_name: str) -> str:
    r = romaji
    kn = kanji_name

    if '郡' in kn:
        r = r.replace('gun', '', 1)

    if kn.endswith('市') and r.endswith('shi'):
        r = r[:-3]
    elif kn.endswith('区') and r.endswith('ku'):
        r = r[:-2]
    elif kn.endswith('町'):
        for suf in ('chou', 'cho', 'machi'):
            if r.endswith(suf):
                r = r[: -len(suf)]
                break
    elif kn.endswith('村'):
        for suf in ('mura', 'son'):
            if r.endswith(suf):
                r = r[: -len(suf)]
                break

    return r


def titlecase_compact(s: str) -> str:
    s = (s or '').replace("'", '')
    if not s:
        return s
    return s[0].upper() + s[1:]


# Build mapping: (pref_kanji, y3_romaji) -> muni_kanji, using code.csv only
mapping: dict[tuple[str, str], str] = {}

with CODE.open('r', encoding='utf-8', newline='') as f:
    reader = csv.reader(f)
    header = next(reader)
    h = [_nfkc(x).replace('\n', '') for x in header]

    try:
        idx_pref_kanji = h.index('都道府県名（漢字）')
        idx_muni_kanji = h.index('市区町村名（漢字）')
        idx_muni_kana = h.index('市区町村名（カナ）')
    except ValueError:
        idx_pref_kanji, idx_muni_kanji, idx_muni_kana = 0, 1, 3

    for row in reader:
        if not row or len(row) < 4:
            continue

        pref_kanji = norm_name(row[idx_pref_kanji])
        muni_kanji = norm_name(row[idx_muni_kanji])
        muni_kana = _nfkc(row[idx_muni_kana])

        if not (pref_kanji and muni_kanji and muni_kana):
            continue

        romaji = kana_to_romaji(muni_kana)
        romaji = strip_admin_suffix(romaji, muni_kanji)
        romaji = titlecase_compact(romaji)

        mapping.setdefault((pref_kanji, romaji), muni_kanji)


# Update z3 in fa-jp----.csv WITHOUT using x3Name
with TARGET.open('r', encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames or [])
    rows = list(reader)

if 'z3' not in fieldnames:
    fieldnames.append('z3')

updated = 0
missing = 0
missing_samples: list[tuple[str, str, str]] = []

for row in rows:
    y3 = (row.get('y3') or '').strip()
    if not y3:
        # Prefecture rows etc.
        if (row.get('z3') or '') != '':
            row['z3'] = ''
            updated += 1
        continue

    pref_kanji = norm_name(row.get('x2Name') or '')
    z3 = mapping.get((pref_kanji, y3), '')

    if not z3:
        missing += 1
        if len(missing_samples) < 30:
            missing_samples.append((row.get('Num', ''), pref_kanji, y3))

    if row.get('z3') != z3:
        row['z3'] = z3
        updated += 1

with TARGET.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)

print('Done: filled z3 (Japanese) from y3 using code.csv only (no x3Name)')
print(f'Rows updated: {updated}')
print(f'Municipality rows with y3 but no z3 mapping: {missing}')
if missing_samples:
    print('Missing samples (Num, pref, y3):')
    for num, pref, y3 in missing_samples:
        print(f' - {num} {pref} {y3}')
