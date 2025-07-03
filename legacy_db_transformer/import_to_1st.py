from sqlalchemy import create_engine
import pandas as pd
import mysql.connector
import numpy as np
from datetime import datetime

# إعداد الاتصال عبر SQLAlchemy للقراءة فقط
DB_URL = 'mysql+pymysql://askar:Askar%401984@localhost:3306/laravel?charset=utf8mb4'
engine = create_engine(DB_URL)

# قراءة جداول lookup
category_df = pd.read_sql("SELECT id, category_name FROM member_category", engine)
relation_df = pd.read_sql("SELECT id, relation_name FROM member_relations", engine)
status_df = pd.read_sql("SELECT id, status_name FROM member_status", engine)
old_members = pd.read_sql("SELECT * FROM old_members", engine)

# تنظيف القيم NaN وتحويلها None
old_members = old_members.where(pd.notnull(old_members), None)
def get_id_from_lookup(name, df, col):
    if not name or str(name).strip().lower() in ["", "-", "nan", "none", "null"]:
        return None
    rec = df[df[col].str.strip() == name.strip()]
    if rec.empty:
        # بدلاً من إرجاع None، يمكن تعيين قيمة افتراضية (مثلاً id=1) أو تسجيل التحذير
        print(f"Warning: '{name}' not found in {col}")
        return 1  # أو قيمة ID مناسبة موجودة في جدول lookup
    return int(rec.iloc[0]['id'])


# بناء family_id
family_map = {}
current_family_id = 1

for idx, row in old_members.iterrows():
    parent = str(row.Mem_ParentMember).strip() if row.Mem_ParentMember else ""
    mem_id = str(row.Mem_ID).strip() if row.Mem_ID else ""
    if not parent or parent in ['0', 'nan', 'none', '-', '', None]:
        family_map[mem_id] = current_family_id
        current_family_id += 1

changed = True
while changed:
    changed = False
    for idx, row in old_members.iterrows():
        mem_id = str(row.Mem_ID).strip() if row.Mem_ID else ""
        if mem_id in family_map:
            continue
        parent = str(row.Mem_ParentMember).strip() if row.Mem_ParentMember else ""
        if parent in family_map:
            family_map[mem_id] = family_map[parent]
            changed = True

for idx, row in old_members.iterrows():
    mem_id = str(row.Mem_ID).strip() if row.Mem_ID else ""
    if mem_id not in family_map:
        family_map[mem_id] = current_family_id
        current_family_id += 1

old_members['family_id'] = old_members['Mem_ID'].astype(str).map(family_map)

# تعيين معرفات lookup
old_members['category_id'] = old_members['Mem_MembershipType'].apply(lambda x: get_id_from_lookup(str(x) if x else "", category_df, 'category_name'))
old_members['relation_id'] = old_members['Mem_Relation'].apply(lambda x: get_id_from_lookup(str(x) if x else "", relation_df, 'relation_name'))
old_members['status_id'] = old_members['Mem_Status'].apply(lambda x: get_id_from_lookup(str(x) if x else "", status_df, 'status_name'))

def safe_val(val):
    if val is None:
        return None
    if isinstance(val, float) and np.isnan(val):
        return None
    if isinstance(val, str) and val.strip().lower() in ['', 'nan', 'none', '-', 'null']:
        return None
    return val

def safe_date(val):
    if val is None:
        return None
    if isinstance(val, pd.Timestamp):
        return val.strftime('%Y-%m-%d')
    if isinstance(val, str) and val.strip() == '':
        return None
    return val

def convert_row(row):
    return (
        safe_val(row.Mem_ID),
        safe_val(row.family_id),
        safe_val(row.Mem_Name),
        safe_val(row.Mem_NID) if safe_val(row.Mem_NID) and str(safe_val(row.Mem_NID)).isdigit() else None,
        1,  # user_id
        safe_val(row.Mem_Sex),
        safe_val(row.category_id),
        safe_val(row.relation_id),
        safe_val(row.status_id),
        safe_val(row.Mem_Mobile),
        safe_date(row.Mem_BOD),
        None, None, None, None,  # email, city, state, age
        safe_val(row.Mem_Job),
        safe_val(row.Mem_Relegion),
        1,
        1,
        "renewed",
        None, None, None,
        safe_val(row.Mem_Notes),
        safe_val(row.Mem_Notes_2),
        safe_val(row.Mem_Notes_3),
        safe_val(row.Mem_Notes_4),
        None,
        None,
        safe_val(row.Mem_BoardDecision_Number),
        safe_val(row.MemCard_MemberName),
        safe_val(row.Mem_Notes),
        safe_val(row.Mem_GraduationDesc),
        safe_val(row.Mem_WorkPhone),
        safe_val(row.Mem_HomePhone),
        None,
        None, None,
        datetime.now(),
        datetime.now(),
    )

# تحويل أول 10 صفوف فقط
rows = [convert_row(row) for idx, row in old_members.head(10).iterrows()]
batch_size = 10

# اتصال للكتابة
DB_CONFIG = {
    'host': 'localhost',
    'user': 'askar',
    'password': 'Askar@1984',
    'database': 'laravel',
    'charset': 'utf8mb4'
}
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

insert_query = """
INSERT INTO member_details (
    member_id, family_id, name, national_id, user_id, gender,
    category_id, relation_id, status_id, phone, date_of_birth,
    email, city, state, age, profession, religion, country_id,
    nationality_id, renewal_status, postal_code, face_book, twitter,
    note, note_2, note_3, note_4, last_paid_fiscal_year,
    date_of_the_board_of_directors, decision_number,
    memCard_MemberName, remarks, mem_GraduationDesc, mem_WorkPhone,
    mem_HomePhone, email_notifications, player, team_id,
    created_at, updated_at
) VALUES (
    %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s,
    %s, %s, %s, %s,
    %s, %s, %s, %s,
    %s, %s
)
"""

cursor.executemany(insert_query, rows)
conn.commit()
print("✅ تم ترحيل 10 سجلات بنجاح.")

cursor.close()
conn.close()
