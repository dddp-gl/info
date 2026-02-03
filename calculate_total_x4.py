import csv

# CSVファイルを読み込んでx4コラムの合計を計算
total_all_x4 = 0  # 全行の合計
total_prefecture_x4 = 0  # 県行のみの合計
total_city_x4 = 0  # 市区町村行のみの合計
prefecture_count = 0
city_count = 0

with open('s.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)  # ヘッダー行をスキップ
    
    for row in reader:
        if len(row) >= 4:
            x3_value = row[2]  # x3コラム（市区町村名）
            x4_value = row[3]  # x4コラムの値
            
            try:
                x4_numeric = int(x4_value)
                total_all_x4 += x4_numeric
                
                if x3_value == "":  # 県の行
                    total_prefecture_x4 += x4_numeric
                    prefecture_count += 1
                else:  # 市区町村の行
                    total_city_x4 += x4_numeric
                    city_count += 1
                    
            except ValueError:
                print(f"数値変換エラー: {row}")

print("=== x4コラム（人口）の集計結果 ===")
print()
print(f"📊 全体の合計値: {total_all_x4:,}人")
print(f"   ├─ 県の行の合計: {total_prefecture_x4:,}人 ({prefecture_count}行)")
print(f"   └─ 市区町村の行の合計: {total_city_x4:,}人 ({city_count}行)")
print()

print("⚠️  注意事項:")
print("   県の行には県別人口合計が設定されているため、")
print("   全体の合計値には重複が含まれています。")
print(f"   実際の日本の総人口は: {total_city_x4:,}人")
print()

print("🔍 検証:")
print(f"   県別人口合計 = 市区町村人口の合計: {total_prefecture_x4 == total_city_x4}")
print(f"   全体合計 = 県合計 + 市区町村合計: {total_all_x4 == total_prefecture_x4 + total_city_x4}")

# いくつかの県の検証
print()
print("=== 県別検証（最初の3県） ===")
prefecture_totals = {}
current_prefecture = None
current_prefecture_total = 0

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
                    if current_prefecture:  # 前の県の結果を出力
                        if count < 3:
                            print(f"{current_prefecture}:")
                            print(f"  県行の値: {x4_numeric:,}人")
                            print(f"  市区町村合計: {current_prefecture_total:,}人")
                            print(f"  一致: {x4_numeric == current_prefecture_total}")
                            count += 1
                    
                    current_prefecture = x2_value
                    prefecture_totals[current_prefecture] = x4_numeric
                    current_prefecture_total = 0
                else:  # 市区町村の行
                    current_prefecture_total += x4_numeric
                        
            except ValueError:
                pass