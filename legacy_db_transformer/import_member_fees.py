import pandas as pd
import mysql.connector
import glob

DB_CONFIG = {
    'host': 'localhost',
    'user': 'askar',
    'password': 'Askar@1984',
    'database': 'laravel'
}
csv_files = glob.glob("sqls/csv/members_with_fees_part*.csv")

for csv_file in csv_files:
    print(f"جاري رفع: {csv_file}")
    df = pd.read_csv(csv_file, encoding="utf-8-sig")
    # الأعمدة بالضبط زي الهيدر
    allowed_cols = [
        'Fee_ID','Fee_Name','Fee_Mem_ID','Fee_Address','Fee_HomePhone','Fee_NID',
        'Fee_Other1','Fee_Other2','Fee_Other3','Fee_Year','Fee_Amount','Fee_Date',
        'Fee_RecieptNumber','Fee_Status','Mem_ID','Mem_Name','Mem_Code','Mem_BOD',
        'Mem_NID','Mem_GraduationGrade','Mem_ParentMember','Mem_Sex','Mem_JobCategory',
        'Mem_Job','Mem_MembershipType','Mem_Relegion','Mem_Address','Mem_JoinDate',
        'Mem_Class','Mem_HomePhone','Mem_Mobile','Mem_Receiver','Mem_WorkPhone','Mem_Photo',
        'Mem_Notes','Mem_LastPayedFees','Mem_Status','MemCard_MemberName','MemCard_MemberJobTitle',
        'Mem_GraduationDesc','Mem_Notes_2','Mem_Notes_3','Mem_Notes_4','Mem_Relation',
        'Mem_BoardDecision_Date','Mem_BoardDecision_Number','created_at','updated_at'
    ]
    df = df[[c for c in allowed_cols if c in df.columns]]
    df = df.astype(str)
    df.replace("nan", "", inplace=True)
    df.replace("None", "", inplace=True)

    # الاتصال بقاعدة البيانات
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cols = ",".join([f"`{col}`" for col in df.columns])
    vals = ",".join(["%s"] * len(df.columns))
    sql = f"INSERT INTO old_fees ({cols}) VALUES ({vals})"
    data = df.values.tolist()
    batch = 500
    for i in range(0, len(data), batch):
        cursor.executemany(sql, data[i:i+batch])
        conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ تم رفع {csv_file} ({len(df)}) رسوم")

print("جميع الملفات تم رفعها بنجاح إلى جدول old_fees.")