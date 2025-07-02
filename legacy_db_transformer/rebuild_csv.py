import pandas as pd

df = pd.read_csv("ready_for_import.csv", encoding="utf-8-sig")
# إذا فيه عمود Mem_Status انسخه إلى status، أو سيبه فاضي
if "Mem_Status" in df.columns:
    df["status"] = df["Mem_Status"]
else:
    df["status"] = ""

df.to_csv("ready_for_import.csv", index=False, encoding="utf-8-sig")
print("تم إضافة عمود status بنجاح!")
