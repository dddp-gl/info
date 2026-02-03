import csv

# CSVファイルを読み込み、文字列置換を実行
input_rows = []
with open('fa-jp----.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        input_rows.append(row)

# 各行の各セルで「日本ニホン」を「日本」に置換
output_rows = []
replacement_count = 0

for row in input_rows:
    new_row = []
    for cell in row:
        if '日本ニホン' in cell:
            new_cell = cell.replace('日本ニホン', '日本')
            new_row.append(new_cell)
            replacement_count += 1
        else:
            new_row.append(cell)
    output_rows.append(new_row)

# 結果をCSVファイルに保存
with open('fa-jp----.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(output_rows)

print(f"処理完了: 「日本ニホン」を「日本」に変更しました")
print(f"置換された箇所の数: {replacement_count}")
print()

print("変更結果の確認（最初の10行）:")
with open('fa-jp----.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        if i < 10:
            # 国名のコラム（インデックス6）をチェック
            if len(row) > 6:
                print(f"行{i+1}: 国名コラム = '{row[6]}'")
            else:
                print(f"行{i+1}: {','.join(row)}")
        else:
            break

# 変更後に「日本ニホン」がまだ残っているかチェック
remaining_count = 0
with open('fa-jp----.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        for cell in row:
            if '日本ニホン' in cell:
                remaining_count += 1

print(f"\n確認: 残りの「日本ニホン」の数: {remaining_count}")