import pandas as pd
import math
from pathlib import Path

# اسم ملف الـ CSV الكبير
csv_path = Path("sqls/csv/members_with_header.csv")  # عدّل المسار لو لزم الأمر

# اقرأ الملف دفعة واحدة (يفضل التأكد من الذاكرة عند وجود ملف ضخم جدًا)
df = pd.read_csv(csv_path, encoding='utf-8')

# احسب عدد الأسطر في كل جزء
total_rows = len(df)
rows_per_part = math.ceil(total_rows / 8)

# احفظ كل جزء في ملف جديد
for i in range(8):
    start = i * rows_per_part
    end = start + rows_per_part
    part_df = df.iloc[start:end]
    part_path = csv_path.parent / f"{csv_path.stem}_part{i+1}.csv"
    part_df.to_csv(part_path, index=False, encoding='utf-8-sig')
    print(f"✅ تم إنشاء {part_path} ({len(part_df)} صف)")

print("\nتم تقسيم الملف إلى 4 أجزاء بنجاح!")
