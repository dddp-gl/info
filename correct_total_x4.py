import csv

# 正確な集計を行う
total_all_x4 = 0  # 全行の合計
total_prefecture_x4 = 0  # 県行のみの合計
total_city_x4 = 0  # 市区町村行のみの合計
prefecture_count = 0
city_count = 0

print("=== x4コラムの詳細分析 ===")
print()

with open('s.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)  # ヘッダー行をスキップ
    
    for i, row in enumerate(reader, 1):
        if len(row) >= 4:
            x2_value = row[1]  # 都道府県名
            x3_value = row[2]  # x3コラム（市区町村名）
            x4_value = row[3]  # x4コラムの値
            
            try:
                x4_numeric = int(x4_value)
                total_all_x4 += x4_numeric
                
                if x3_value == "":  # 県の行（x3が空）
                    total_prefecture_x4 += x4_numeric
                    prefecture_count += 1
                    if prefecture_count <= 5:  # 最初の5県を表示
                        print(f"県行 {prefecture_count}: {x2_value} = {x4_numeric:,}人")
                else:  # 市区町村の行（x3に市区町村名あり）
                    total_city_x4 += x4_numeric
                    city_count += 1
                    
            except ValueError:
                print(f"数値変換エラー (行{i+1}): {row}")

print()
print("=== 集計結果 ===")
print(f"📊 x4コラム全体の合計値: {total_all_x4:,}人")
print()
print(f"🏛️  県の行の集計:")
print(f"   ・行数: {prefecture_count}行")
print(f"   ・合計: {total_prefecture_x4:,}人")
print()
print(f"🏘️  市区町村の行の集計:")
print(f"   ・行数: {city_count}行") 
print(f"   ・合計: {total_city_x4:,}人")
print()

print("💡 解説:")
if total_prefecture_x4 == total_city_x4:
    print("   ✅ 県の行の合計 = 市区町村の行の合計")
    print("   → 県の行には正しく県別人口合計が設定されています")
    print()
    print(f"   🔢 実際の日本の総人口: {total_city_x4:,}人")
    print(f"   🔢 データ上の合計値: {total_all_x4:,}人 (重複込み)")
    print(f"   📊 重複率: {total_all_x4 / total_city_x4:.1f}倍")
else:
    print("   ⚠️ 県の行と市区町村の行の合計が一致しません")
    print("   → データに不整合がある可能性があります")