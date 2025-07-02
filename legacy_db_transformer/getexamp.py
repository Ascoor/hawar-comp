import pandas as pd

df = pd.read_csv('members_cleaned.csv', encoding='utf-8-sig')
df_sample = df.head(10000)
df_sample.to_csv('members_sample.csv', index=False, encoding='utf-8-sig')
print("✅ تم إنشاء ملف عينة: members_sample.csv")
