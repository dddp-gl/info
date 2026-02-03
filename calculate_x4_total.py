import csv

# CSVファイルを読み込んでx4コラムの合計を計算
total_x4 = 0
prefecture_rows = 0
city_rows = 0

with open('s.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)  # ヘッダー行をスキップ
    print(f"ヘッダー: {header}")
    print()
    
    for row in reader:
        if len(row) >= 4:  # x4コラムがある場合
            x3_value = row[2]  # x3コラム（市区町村名）
            x4_value = row[3]  # x4コラムの値
            
            try:
                x4_numeric = int(x4_value)
                
                # x3が空の場合は県の行、空でない場合は市区町村の行
                if x3_value == "":
                    prefecture_rows += 1
                    print(f"県行: {row[1]}, x4={x4_numeric}")
                else:
                    city_rows += 1
                    total_x4 += x4_numeric
                    
            except ValueError:
                print(f"数値変換エラー: {row}")

print(f"\n=== 集計結果 ===")
print(f"県の行数: {prefecture_rows}")
print(f"市区町村の行数: {city_rows}")
print(f"x4コラム（人口）の合計値: {total_x4:,}")

# 都道府県別の集計も表示（最初の5県分）
print(f"\n=== 都道府県別集計（最初の5県） ===")
prefecture_totals = {}
current_prefecture = None

with open('s.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # ヘッダー行をスキップ
    
    count = 0
    for row in reader:
        if len(row) >= 4:
            x2_value = row[1]  # 都道府県名
            x3_value = row[2]  # 市区町村名
            x4_value = row[3]  # 人口
            
            try:
                x4_numeric = int(x4_value)
                
                if x3_value == "":  # 県の行
                    current_prefecture = x2_value
                    prefecture_totals[current_prefecture] = 0
                else:  # 市区町村の行
                    if current_prefecture:
                        prefecture_totals[current_prefecture] += x4_numeric
                        
            except ValueError:
                pass
    
    # 最初の5県の結果を表示
    for i, (pref, total) in enumerate(prefecture_totals.items()):
        if i < 5:
            print(f"{pref}: {total:,}")
        else:
            break