import pandas as pd

# تحميل الملف
csv_path = "sqls/membersAll - membersAll.csv"
df = pd.read_csv(csv_path)

# تحليل القيم الفارغة وأعلى القيم تكرارًا
for column in df.columns:
    print(f"\nالعمود: {column}")
    
    # عدد القيم الفارغة وغير الفارغة
    empty_count = df[column].isna().sum()
    non_empty_count = df[column].notna().sum()
    print(f"  عدد القيم الفارغة: {empty_count}")
    print(f"  عدد القيم غير الفارغة: {non_empty_count}")

    # أعلى 3 قيم متكررة
    top_values = df[column].value_counts().head(3)
    for value, count in top_values.items():
        print(f"  القيمة: {value}  ←  عدد مرات التكرار: {count}")

    print("-" * 50)
