import csv

# fa-----.csvから人口データを読み取り、合計を計算
total_population = 0
country_count = 0

with open('fa-----.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # zzはGlobal（合計行）なのでスキップ
        if row['x1'] == 'zz':
            continue
        
        population_str = row['Population'].strip()
        if population_str:
            try:
                population = int(population_str)
                total_population += population
                country_count += 1
                print(f"{row['x1']}: {row['x1Name']}: {population:,}")
            except ValueError:
                print(f"エラー: {row['x1']} の人口データを変換できません: {population_str}")

print(f"\n合計: {country_count}カ国/地域")
print(f"世界人口合計: {total_population:,}")
