import csv

# CSVファイルを読み込み
rows = []
with open('s.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)  # ヘッダー行を読み込み
    rows.append(header)
    
    # データ行を処理
    for row in reader:
        if len(row) >= 1:  # x1コラムがある場合
            x1_value = row[0]  # x1コラムの値
            # 後ろの4文字を削除
            x5_value = x1_value[:-4] if len(x1_value) > 4 else ""
            # x5コラム（5番目のコラム、インデックス4）に設定
            if len(row) >= 5:
                row[4] = x5_value
            else:
                # x5コラムが存在しない場合は追加
                while len(row) < 5:
                    row.append("")
                row[4] = x5_value
        rows.append(row)

# 結果をCSVファイルに保存
with open('s.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print("処理完了: x1コラムの後ろの4文字を削除した結果をx5コラムに設定しました")
print("最初の10行の結果:")
with open('s.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        if i < 10:
            print(','.join(row))
        else:
            break