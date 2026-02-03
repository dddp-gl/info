import csv

# CSVファイルを読み込み
input_rows = []
with open('s.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        input_rows.append(row)

# 新しい行リストを作成
output_rows = []
header = input_rows[0]  # ヘッダー行
output_rows.append(header)

current_prefecture = None
data_rows = input_rows[1:]  # データ行のみ

# 都道府県別の人口合計を先に計算
prefecture_totals = {}
current_pref_for_calc = None
current_total = 0

for row in data_rows:
    if len(row) >= 2:
        prefecture = row[1]  # a2コラムの都道府県名
        
        if prefecture != current_pref_for_calc:
            if current_pref_for_calc:
                prefecture_totals[current_pref_for_calc] = current_total
            current_pref_for_calc = prefecture
            current_total = 0
        
        # 人口を合計に加算
        try:
            population = int(row[3])  # a4コラム
            current_total += population
        except ValueError:
            pass

# 最後の都道府県の合計を記録
if current_pref_for_calc:
    prefecture_totals[current_pref_for_calc] = current_total

# 県の行を挿入しながら新しいCSVを作成
current_prefecture = None

for row in data_rows:
    if len(row) >= 2:  # a2コラム（都道府県名）がある場合
        prefecture = row[1]  # a2コラムの都道府県名
        
        # 都道府県が変わった場合、県の行を挿入
        if prefecture != current_prefecture:
            # 県の行を作成（a3コラムを空に、a4コラムに県別人口合計を設定）
            prefecture_total = prefecture_totals.get(prefecture, 0)
            
            # a5（都道府県コードの前半）とa6（後半4文字）は元の行から取得
            original_a1 = row[0]  # 元のa1の値
            if len(original_a1) >= 4:
                a5_value = original_a1[:-4]  # 前半部分
            else:
                a5_value = ""
            
            prefecture_row = [row[0], prefecture, "", str(prefecture_total), a5_value, row[5]]
            output_rows.append(prefecture_row)
            current_prefecture = prefecture
        
        # 元の市区町村行を追加
        output_rows.append(row)

# 結果をCSVファイルに保存
with open('s.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output_rows)

print("処理完了: 各都道府県の市区町村グループの先頭に県の行を追加しました")
print()
print("追加された県の行の特徴:")
print("- a3コラム: 空文字（市区町村名なし）")
print("- a4コラム: 県別人口合計")
print()
print("最初の20行の結果:")
with open('s.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        if i < 20:
            if i == 0:
                print(f"ヘッダー: {','.join(row)}")
            else:
                row_type = "県行" if row[2] == "" else "市区町村"
                print(f"{i+1:2}: {row_type:4} | {row[1]:6} | {row[2]:10} | {row[3]:8}")
        else:
            break