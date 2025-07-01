import re
import pandas as pd
from pathlib import Path

def parse_inserts(file_path, table_name):
    """
    يحلل ملف SQL ويعيد DataFrame فيه كل البيانات من جمل INSERT INTO
    """
    with open(file_path, encoding='utf-8') as f:
        sql = f.read()
    # استخراج الأعمدة وقيم الإدخال
    pattern = re.compile(rf"INSERT INTO\s+`?{table_name}`?\s*\((.*?)\)\s*VALUES\s*(.*?);", re.DOTALL | re.IGNORECASE)
    matches = pattern.findall(sql)
    all_rows = []
    columns = []
    for cols_str, values_str in matches:
        columns = [c.strip(" `") for c in cols_str.split(",")]
        rows = re.findall(r"\((.*?)\)", values_str, re.DOTALL)
        for row in rows:
            # تقسيم القيم مع مراعاة النصوص المحتوية على فواصل
            vals = [v.strip().strip("'") for v in re.split(r",(?![^(]*\))", row)]
            if len(vals) == len(columns):
                all_rows.append(vals)
    if all_rows:
        df = pd.DataFrame(all_rows, columns=columns)
    else:
        df = pd.DataFrame(columns=columns)
    return df

# المسار لمجلد sqls
base_path = Path("sqls/")  # غيّر المسار لو لزم الأمر

# استخرج بيانات الأعضاء
members_file = base_path / "members.sql"
members = parse_inserts(members_file, "members")
members = members.dropna(axis=1, how='all')

# --- علاقات أسرية (بيانات الأب) ---
if "Mem_ParentMember" in members.columns and "Mem_ID" in members.columns:
    members_with_parent = members[members['Mem_ParentMember'].notnull() & (members['Mem_ParentMember'] != '')]
    parent_ids = members_with_parent['Mem_ParentMember'].unique()
    parents = members[members['Mem_ID'].isin(parent_ids)]
    # دمج الأعضاء وأولياء الأمور في عينة واحدة (بدون تكرار)
    full_members_sample = pd.concat([members_with_parent, parents]).drop_duplicates(subset=['Mem_ID'])
else:
    full_members_sample = members

# --- بيانات الاشتراكات إن وجدت ---
fees_file = base_path / "fees.sql"
if fees_file.exists():
    fees = parse_inserts(fees_file, "fees")
    fees = fees.dropna(axis=1, how='all')
    # ربط أول 10 أعضاء مع رسومهم
    sample10 = full_members_sample.head(10)
    if "Mem_ID" in sample10.columns and "Fee_Mem_ID" in fees.columns:
        result = sample10.merge(fees, left_on="Mem_ID", right_on="Fee_Mem_ID", how="left", suffixes=('_member', '_fee'))
    else:
        result = sample10
else:
    # لو ملف الرسوم غير موجود، عينة من الأعضاء فقط
    result = full_members_sample.head(10)

# تنظيف الأعمدة الفارغة
result = result.dropna(axis=1, how='all')
# حفظ العينة لملف CSV في نفس مجلد sqls
result.to_csv(base_path / "sample.csv", index=False, encoding='utf-8-sig')

print("✅ تم استخراج عينة بيانات sample.csv في sqls/")
print("إذا تريد تغيير عدد السجلات غير رقم 10 في الكود.")
