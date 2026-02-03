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

for row in data_rows:
    if len(row) >= 2:  # x2コラム（都道府県名）がある場合
        prefecture = row[1]  # x2コラムの都道府県名
        
        # 都道府県が変わった場合、県の行を挿入
        if prefecture != current_prefecture:
            # 県の行を作成（x3コラムを空に、x4コラムを0に設定）
            prefecture_row = [row[0], prefecture, "", "0", row[4]]
            output_rows.append(prefecture_row)
            current_prefecture = prefecture
        
        # 元の市区町村行を追加
        output_rows.append(row)

# 結果をCSVファイルに保存
with open('s.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output_rows)

print("処理完了: 各都道府県の市区町村の前に県の行を挿入しました")
print("最初の20行の結果:")
with open('s.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        if i < 20:
            print(f"{i+1}: {','.join(row)}")
        else:
            break