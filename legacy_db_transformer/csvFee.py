import pandas as pd

input_csv = 'sqls/csv/members_with_fees_part1.csv'  # اسم ملفك الأصلي
output_csv = 'vw_membersfees_cleaned.csv'  # اسم الملف الناتج

# الأعمدة المراد استخراجها بالترتيب حسب ما تحتاج
columns = [
    'Mem_ID','Mem_Name','Mem_Code','Mem_Address','Mem_HomePhone','Mem_Mobile','Mem_WorkPhone',
    'Fee_ID','Fee_Year','Fee_Amount','Fee_Date','Fee_RecieptNumber','Fee_Status','Fee_User_ID'
]

# قراءة الملف بكل أعمدته
df = pd.read_csv(input_csv, encoding='utf-8-sig')

# الاحتفاظ فقط بالأعمدة المطلوبة (يتم حذف أي أعمدة زيادة)
df = df[columns]

# حفظ الملف الناتج مع الهيدر
df.to_csv(output_csv, index=False, encoding='utf-8-sig')
print(f'✅ تم تجهيز ملف {output_csv} مع الرؤوس المطلوبة!')
