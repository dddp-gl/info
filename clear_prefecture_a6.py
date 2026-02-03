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

prefecture_count = 0
city_count = 0

for row in input_rows[1:]:  # データ行のみ
    if len(row) >= 6:  # 全てのコラムがある場合
        a3_value = row[2]  # a3コラム（市区町村名）
        
        if a3_value == "":  # 県の行（a3が空）
            # a6コラム（インデックス5）を空白に設定
            row[5] = ""
            prefecture_count += 1
            print(f"県行更新: {row[1]} のa6コラムを空白に設定")
        else:  # 市区町村の行
            city_count += 1
    
    output_rows.append(row)

# 結果をCSVファイルに保存
with open('s.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output_rows)

print()
print("処理完了: 県の行のa6コラムを空白に設定しました")
print(f"更新された県の行数: {prefecture_count}")
print(f"市区町村の行数: {city_count}")
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
                a6_display = f"'{row[5]}'" if len(row) > 5 else "N/A"
                print(f"{i+1:2}: {row_type:4} | {row[1]:6} | a6={a6_display}")
        else:
            break