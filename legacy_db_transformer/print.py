import pandas as pd
import mysql.connector


import glob# إعدادات الاتصال بقاعدة البيانات
DB_CONFIG = {
    'host': 'localhost',
    'user': 'askar',
    'password': 'Askar@1984',
    'database': 'laravel'
}
conn = mysql.connector.connect(**DB_CONFIG)

# 1. عدد الأسطر في كل جدول
for table in ["old_members", "old_fees"]:
    df_count = pd.read_sql(f"SELECT COUNT(*) as total_rows FROM {table}", conn)
    print(f"\nعدد الأسطر في جدول {table}: {df_count.iloc[0]['total_rows']}")

# 2. عينة من البيانات في كل جدول (مثال لأول صفين)
for table in ["old_members", "old_fees"]:
    df = pd.read_sql(f"SELECT * FROM {table} LIMIT 2", conn)
    print(f"\nعينتان من جدول {table}:\n")
    for col in df.columns:
        values = df[col].tolist()
        print(f"  [{col}]: {values}")

conn.close()
