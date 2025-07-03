import pandas as pd
import mysql.connector

# إعدادات الاتصال بقاعدة البيانات
DB_CONFIG = {
    'host': 'localhost',
    'user': 'askar',
    'password': 'Askar@1984',
    'database': 'laravel',
    'charset': 'utf8mb4'
}
conn = mysql.connector.connect(**DB_CONFIG)

# اطبع عدد الأسطر في الجدولين المطلوبين
for table in ["old_members", "member_details"]:
    df_count = pd.read_sql(f"SELECT COUNT(*) as total_rows FROM {table}", conn)
    print(f"\nعدد الأسطر في جدول {table}: {df_count.iloc[0]['total_rows']}")

# طباعة أول 10 أسطر من جدول member_details فقط (لعينة البيانات)
print("\nعينة من أول 10 أسطر في جدول member_details:")
sample_df = pd.read_sql("SELECT * FROM member_details LIMIT 10", conn)
print(sample_df)

conn.close()
