import pandas as pd
import mysql.connector
from datetime import datetime

# إعداد اتصال قاعدة البيانات
DB_CONFIG = {
    'host': 'localhost',
    'user': 'askar',
    'password': 'Askar@1984',
    'database': 'laravel'
}

# 1. قراءة الملف مع تجاهل التحذيرات
df = pd.read_csv('membersAll_cleaned_first5000.csv', encoding='utf-8-sig', low_memory=False)

# 2. دالة للحصول على أو إنشاء المعرفات من جداول العلاقات والفئات والحالات
def insert_and_get_map(table, unique_values, cursor):
    mapping = {}
    for name in unique_values:
        if not isinstance(name, str):
            name_clean = str(name) if pd.notna(name) else "بدون"
        else:
            name_clean = name.strip() if name.strip() else "بدون"

        cursor.execute(f"SELECT id FROM {table} WHERE name = %s", (name_clean,))
        row = cursor.fetchone()
        if row:
            mapping[name] = row[0]
        else:
            cursor.execute(f"INSERT INTO {table} (name, created_at, updated_at) VALUES (%s, NOW(), NOW())", (name_clean,))
            mapping[name] = cursor.lastrowid
    return mapping

# 3. اتصال بقاعدة البيانات
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# 4. استخراج القيم الفريدة
unique_relations = set(df['Mem_Relation'].dropna().unique())
unique_statuses = set(df['Status'].dropna().unique())
unique_categories = set(df['MembershipType'].dropna().unique())

# 5. الحصول على الخرائط (name -> id)
relation_map = insert_and_get_map('member_relations', unique_relations, cursor)
status_map = insert_and_get_map('member_statuses', unique_statuses, cursor)
category_map = insert_and_get_map('member_categories', unique_categories, cursor)

conn.commit()

# 6. استبدال النصوص بمعرفاتها في DataFrame
df['relation_id'] = df['Mem_Relation'].map(lambda x: relation_map.get(x, None))
df['status_id'] = df['Status'].map(lambda x: status_map.get(x, None))
df['category_id'] = df['MembershipType'].map(lambda x: category_map.get(x, None))

# 7. حذف الأعمدة النصية الأصلية
df.drop(['Mem_Relation', 'Status', 'MembershipType', 'parentName'], axis=1, inplace=True, errors='ignore')

# 8. إعادة تسمية الأعمدة لتتطابق مع أسماء أعمدة قاعدة البيانات (إذا تريد)
df.rename(columns={
    'Gender': 'Mem_Sex',
    'Graduation': 'Mem_GraduationGrade',
    'JobCategory': 'Mem_JobCategory',
    'Class': 'Mem_Class',
    'Status': 'Mem_Status',  # حذف أعلاه، هذه للتوثيق فقط
}, inplace=True)

# 9. تأكد من تنظيف التواريخ وتحويلها لصيغة yyyy-mm-dd حسب حاجتك (أضف كود تنظيف هنا إذا لزم)

# 10. حفظ الملف الجديد مع المعرفات
df.to_csv('membersAll_with_ids.csv', index=False, encoding='utf-8-sig')

cursor.close()
conn.close()

print("✅ تم استبدال العلاقات بالنصوص بمعرفات وأُنشئ ملف CSV جديد بنجاح.")
