import csv

# まず都道府県別の人口合計を計算
prefecture_totals = {}
current_prefecture = None

# CSVファイルを読み込んで都道府県別人口を計算
with open('s.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # ヘッダー行をスキップ
    
    for row in reader:
        if len(row) >= 4:
            x2_value = row[1]  # 都道府県名
            x3_value = row[2]  # 市区町村名
            x4_value = row[3]  # 人口
            
            try:
                x4_numeric = int(x4_value)
                
                if x3_value == "":  # 県の行
                    current_prefecture = x2_value
                    if current_prefecture not in prefecture_totals:
                        prefecture_totals[current_prefecture] = 0
                else:  # 市区町村の行
                    if current_prefecture:
                        prefecture_totals[current_prefecture] += x4_numeric
                        
            except ValueError:
                pass

# CSVファイルを再読み込みして県の行のx4コラムを更新
input_rows = []
with open('s.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        input_rows.append(row)

# 県の行のx4コラムを更新
output_rows = []
header = input_rows[0]  # ヘッダー行
output_rows.append(header)

for row in input_rows[1:]:  # データ行
    if len(row) >= 4:
        x2_value = row[1]  # 都道府県名
        x3_value = row[2]  # 市区町村名
        
        if x3_value == "":  # 県の行
            if x2_value in prefecture_totals:
                row[3] = str(prefecture_totals[x2_value])  # x4コラムを県別人口合計に更新
    
    output_rows.append(row)

# 結果をCSVファイルに保存
with open('s.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output_rows)

print("処理完了: 各県の行のx4コラムに県別人口合計を設定しました")
print("\n都道府県別人口:")
for pref, total in list(prefecture_totals.items())[:10]:  # 最初の10県を表示
    print(f"{pref}: {total:,}人")
print("...")

print(f"\n最初の20行の結果:")
with open('s.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        if i < 20:
            print(f"{i+1}: {','.join(row)}")
        else:
            break