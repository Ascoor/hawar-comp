import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

# إعداد الاتصال بقاعدة البيانات
DB_URL = 'mysql+pymysql://askar:Askar%401984@localhost:3306/laravel?charset=utf8mb4'
engine = create_engine(DB_URL)

# قراءة بيانات الجدول القديم
df_old = pd.read_sql("SELECT * FROM old_members", engine)

# تحميل جداول المرجع
category_map = pd.read_sql("SELECT id, category_name FROM member_category", engine).set_index('category_name')['id'].to_dict()
relation_map = pd.read_sql("SELECT id, relation_name FROM member_relations", engine).set_index('relation_name')['id'].to_dict()
status_map = pd.read_sql("SELECT id, status_name FROM member_status", engine).set_index('status_name')['id'].to_dict()

# دالة لتحويل التاريخ
def parse_date(val, default="1970-01-01"):
    try:
        return datetime.strptime(val, "%d-%m-%Y").strftime("%Y-%m-%d")
    except:
        return default

# استخراج الاسم المشترك بعد أول كلمة
def extract_common_name(name):
    if not isinstance(name, str): return ""
    parts = name.strip().split()
    return " ".join(parts[1:]) if len(parts) > 1 else ""

# مخرجات المزامنة
mem_id_to_new_id = {}
inserted_rows = []

with engine.begin() as conn:
    for index, row in df_old.iterrows():
        try:
            # تحديد أو إدخال category_id
            category_id = category_map.get(row['Mem_JobCategory'])
            if category_id is None and row['Mem_JobCategory']:
                result = conn.execute(
                    text("INSERT INTO member_category (category_name) VALUES (:val)"),
                    {"val": row['Mem_JobCategory']}
                )
                category_id = result.lastrowid
                category_map[row['Mem_JobCategory']] = category_id

            # relation_id
            relation_id = relation_map.get(row['Mem_Relation'])
            if relation_id is None and row['Mem_Relation']:
                result = conn.execute(
                    text("INSERT INTO member_relations (relation_name) VALUES (:val)"),
                    {"val": row['Mem_Relation']}
                )
                relation_id = result.lastrowid
                relation_map[row['Mem_Relation']] = relation_id

            # status_id
            status_id = status_map.get(row['Mem_Status'])
            if status_id is None and row['Mem_Status']:
                result = conn.execute(
                    text("INSERT INTO member_status (status_name) VALUES (:val)"),
                    {"val": row['Mem_Status']}
                )
                status_id = result.lastrowid
                status_map[row['Mem_Status']] = status_id

            # إعداد البيانات
            mem_id = str(row['Mem_ID']).strip()
            parent_mem_id = str(row['Mem_ParentMember']).strip()
            family_id = 0

            # 1️⃣ إذا كان العضو تابعًا
            if parent_mem_id:
                family_id = parent_mem_id

            # 2️⃣ إذا كان عضوًا عاملًا ولا يوجد Parent → حاول البحث بالاسم المشترك
            else:
                current_common_name = extract_common_name(row['Mem_Name'])
                for other_row in df_old.itertuples():
                    if str(other_row.Mem_ID) == mem_id:
                        continue
                    if extract_common_name(other_row.Mem_Name) == current_common_name:
                        family_id = other_row.Mem_ID
                        break
                if not family_id:
                    family_id = mem_id  # fallback

            # تجهيز بيانات الإدخال
            insert_data = {
                "member_id": mem_id,
                "family_id": int(family_id) if str(family_id).isdigit() else 0,
                "name": row['Mem_Name'] or "",
                "national_id": int(row['Mem_NID']) if pd.notna(row['Mem_NID']) and str(row['Mem_NID']).isdigit() else 0,
               
                "gender": row['Mem_Sex'] or "",
                "category_id": category_id or 1,
                "relation_id": relation_id or 1,
                "status_id": status_id or 1,
                "phone": row['Mem_Mobile'] or "",
                "date_of_birth": parse_date(row['Mem_BOD']) if pd.notna(row['Mem_BOD']) else "1970-01-01",
                "email": "",
                "address": row['Mem_Address'] or "",
                "city": "",
                "state": "",
                "age": "",
                "profession": row['Mem_Job'] or "",
                "religion": row['Mem_Relegion'] or "",
                "country_id": 64,
                "nationality_id": 64,
                "renewal_status": "renewed",
                "postal_code": "",
                "face_book": "",
                "twitter": "",
                "note": row['Mem_Notes'],
                "note_2": row['Mem_Notes_2'],
                "note_3": row['Mem_Notes_3'],
                "note_4": row['Mem_Notes_4'],
                "last_paid_fiscal_year": parse_date(row['Mem_LastPayedFees']) if pd.notna(row['Mem_LastPayedFees']) else "2000-01-01",
                "date_of_the_board_of_directors": parse_date(row['Mem_BoardDecision_Date']) if pd.notna(row['Mem_BoardDecision_Date']) else "2000-01-01",
                "decision_number": row['Mem_BoardDecision_Number'] or "",
                "memCard_MemberName": row['MemCard_MemberName'] or "",
                "remarks": row['MemCard_MemberJobTitle'] or "",
                "mem_GraduationDesc": row['Mem_GraduationDesc'] or "",
                "mem_WorkPhone": row['Mem_WorkPhone'] or "",
                "mem_HomePhone": row['Mem_HomePhone'] or "",
                "email_notifications": "yes",
                "player": None,
                "team_id": None,
            }

            result = conn.execute(
                text("""
                    INSERT INTO member_details (
                        member_id, family_id, name, national_id, user_id, gender, category_id,
                        relation_id, status_id, phone, date_of_birth, email, address, city,
                        state, age, profession, religion, country_id, nationality_id, renewal_status,
                        postal_code, face_book, twitter, note, note_2, note_3, note_4,
                        last_paid_fiscal_year, date_of_the_board_of_directors, decision_number,
                        memCard_MemberName, remarks, mem_GraduationDesc, mem_WorkPhone, mem_HomePhone,
                        email_notifications, player, team_id, created_at, updated_at
                    ) VALUES (
                        :member_id, :family_id, :name, :national_id, :user_id, :gender, :category_id,
                        :relation_id, :status_id, :phone, :date_of_birth, :email, :address, :city,
                        :state, :age, :profession, :religion, :country_id, :nationality_id, :renewal_status,
                        :postal_code, :face_book, :twitter, :note, :note_2, :note_3, :note_4,
                        :last_paid_fiscal_year, :date_of_the_board_of_directors, :decision_number,
                        :memCard_MemberName, :remarks, :mem_GraduationDesc, :mem_WorkPhone, :mem_HomePhone,
                        :email_notifications, :player, :team_id, NOW(), NOW()
                    )
                """), insert_data
            )

            new_id = result.lastrowid
            mem_id_to_new_id[mem_id] = new_id
            inserted_rows.append((new_id, str(family_id)))

        except Exception as e:
            print(f"خطأ في الصف {index}: {e}")

print("✅ تمت المزامنة بنجاح.")
