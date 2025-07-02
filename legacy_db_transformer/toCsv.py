import pandas as pd
import numpy as np
import mysql.connector
from datetime import datetime

# 1. قراءة ملف الأعضاء
df = pd.read_csv('membersAll_cleaned_first5000.csv', encoding='utf-8-sig', low_memory=False)

# 2. تنظيف القيم الفارغة وتهيئة None بدلاً من nan
df = df.replace({np.nan: None, 'nan': None, 'NaN': None, 'none': None, '': None, 'null': None})

# 3. دالة لتحويل التواريخ
def fix_date(val):
    if not val:
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(str(val), fmt).strftime("%Y-%m-%d")
        except:
            continue
    return None

# 4. تنظيف التواريخ
for col in ['Mem_BOD', 'Mem_JoinDate', 'Mem_BoardDecision_Date']:
    if col in df.columns:
        df[col] = df[col].apply(fix_date)

# 5. دالة لتحويل القيم الرقمية لـ int أو None
def fix_int(val):
    try:
        if val is None:
            return None
        return int(float(val))
    except:
        return None

# 6. تنظيف الأعمدة الرقمية
for col in ['Mem_ParentMember', 'Mem_Code']:
    if col in df.columns:
        df[col] = df[col].apply(fix_int)

# 7. قص أعمدة الهاتف لأقصى 20 حرف
for col in ['Mem_WorkPhone', 'Mem_HomePhone', 'Mem_Mobile']:
    if col in df.columns:
        df[col] = df[col].astype(str).str[:20]

# 8. التحقق من العلاقات في جداول DB أو إضافتها
DB_CONFIG = {
    'host': 'localhost',
    'user': 'askar',
    'password': 'Askar@1984',
    'database': 'laravel'
}

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

def insert_and_get_map(table, unique_values):
    mapping = {}
    for name in unique_values:
        if not isinstance(name, str):
            name_clean = str(name) if name is not None else "بدون"
        else:
            name_clean = name.strip() or "بدون"
        cursor.execute(f"SELECT id FROM {table} WHERE name = %s", (name_clean,))
        row = cursor.fetchone()
        if row:
            mapping[name] = row[0]
        else:
            cursor.execute(f"INSERT INTO {table} (name, created_at, updated_at) VALUES (%s, NOW(), NOW())", (name_clean,))
            mapping[name] = cursor.lastrowid
    conn.commit()
    return mapping

# 9. جلب القيم الفريدة للعلاقات والحالات والفئات
unique_relations = set(df['Mem_Relation'].dropna().unique())
unique_statuses = set(df['Status'].dropna().unique())
unique_categories = set(df['MembershipType'].dropna().unique())

relation_map = insert_and_get_map('member_relations', unique_relations)
status_map = insert_and_get_map('member_statuses', unique_statuses)
category_map = insert_and_get_map('member_categories', unique_categories)

# 10. استبدال النصوص بمعرفاتهم
df['relation_id'] = df['Mem_Relation'].map(lambda x: relation_map.get(x))
df['status_id'] = df['Status'].map(lambda x: status_map.get(x))
df['category_id'] = df['MembershipType'].map(lambda x: category_map.get(x))

# 11. حذف الأعمدة النصية الأصلية (اختياري)
df.drop(['Mem_Relation', 'Status', 'MembershipType'], axis=1, inplace=True)

# 12. الأعمدة للإدخال في جدول members
insert_columns = [
    'Mem_Name', 'Mem_Code', 'Mem_BOD', 'Mem_NID', 'Graduation',
    'Mem_ParentMember', 'Gender', 'JobCategory', 'Mem_Job', 'Relegion',
    'Mem_Address', 'Mem_JoinDate', 'Class', 'Mem_HomePhone', 'Mem_Mobile',
    'Mem_Receiver', 'Mem_WorkPhone', 'Mem_Photo', 'Mem_Notes', 'Mem_LastPayedFees',
    'MemCard_MemberName', 'MemCard_MemberJobTitle', 'Mem_GraduationDesc', 'Mem_Notes_2',
    'Mem_Notes_3', 'Mem_Notes_4', 'Mem_BoardDecision_Date', 'Mem_BoardDecision_Number',
    'relation_id', 'status_id', 'category_id'
]

insert_query = f"""
INSERT INTO members ({', '.join(insert_columns)})
VALUES ({', '.join(['%s'] * len(insert_columns))})
"""

# 13. تنظيف الصفوف قبل الإدخال
def clean_row(row):
    cleaned = []
    for v in row:
        if v is None or (isinstance(v, float) and pd.isna(v)):
            cleaned.append(None)
        elif isinstance(v, str) and v.strip().lower() in ['', 'none', 'nan', 'null']:
            cleaned.append(None)
        else:
            cleaned.append(v)
    return cleaned

data_to_insert = [clean_row(row) for row in df[insert_columns].values.tolist()]

# 14. إدخال البيانات بدفعات batch
batch_size = 500
for start in range(0, len(data_to_insert), batch_size):
    batch = data_to_insert[start:start + batch_size]
    cursor.executemany(insert_query, batch)
    conn.commit()

print(f"✅ تم نقل {len(data_to_insert)} عضو بنجاح!")

cursor.close()
conn.close()
