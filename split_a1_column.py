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

data_rows = input_rows[1:]  # データ行のみ

for row in data_rows:
    if len(row) >= 1:  # a1コラムがある場合
        a1_value = str(row[0])  # a1コラムの値を文字列として取得
        
        # a1の値を後ろの4文字と残りに分割
        if len(a1_value) >= 4:
            a5_value = a1_value[:-4]  # 後ろの4文字を除いた残り
            a6_value = a1_value[-4:]  # 後ろの4文字
        else:
            # 4文字未満の場合は全てa6に、a5は空文字
            a5_value = ""
            a6_value = a1_value
        
        # a5コラム（インデックス4）とa6コラム（インデックス5）に設定
        # 必要に応じて配列を拡張
        while len(row) < 6:
            row.append("")
        
        row[4] = a5_value  # a5コラムに残りの文字
        row[5] = a6_value  # a6コラムに後ろの4文字
    
    output_rows.append(row)

# 結果をCSVファイルに保存
with open('s.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output_rows)

print("処理完了: a1コラムの文字を分割しました")
print("a1コラムの値 → a5（残りの文字）+ a6（後ろの4文字）")
print()
print("最初の10行の結果:")
with open('s.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        if i < 10:
            if i == 0:
                print(f"ヘッダー: {','.join(row)}")
            else:
                print(f"行{i+1}: a1={row[0]} → a5='{row[4]}' + a6='{row[5]}'")
        else:
            break

print()
print("分割例:")
print("'11002' → a5='1' + a6='1002'")
print("'12025' → a5='1' + a6='2025'")