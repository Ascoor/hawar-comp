import mysql.connector

def insert_and_get_ids(cursor, conn, table, values):
    mapping = {}
    for val in values:
        val_clean = val.strip() if val and val.strip() else "بدون"
        cursor.execute(f"SELECT id FROM {table} WHERE name = %s", (val_clean,))
        row = cursor.fetchone()
        if row:
            mapping[val] = row[0]
        else:
            cursor.execute(
                f"INSERT INTO {table} (name, created_at, updated_at) VALUES (%s, NOW(), NOW())",
                (val_clean,)
            )
            conn.commit()
            mapping[val] = cursor.lastrowid
    return mapping

# مثال على استخدام الدالة:

DB_CONFIG = {
    'host': 'localhost',
    'user': 'askar',
    'password': 'Askar@1984',
    'database': 'laravel'
}

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# افترض أنك جمعت القيم الفريدة من DataFrame كالتالي:
unique_relations = {"عضو عامل", "تابع", "مؤسس"}  # استبدل بالقيم الحقيقية
unique_statuses = {"مفعل", "متوقف"}
unique_categories = {"عضو عامل", "عضو تابع", "عضو مؤسس"}

relation_map = insert_and_get_ids(cursor, conn, 'member_relations', unique_relations)
status_map = insert_and_get_ids(cursor, conn, 'member_statuses', unique_statuses)
category_map = insert_and_get_ids(cursor, conn, 'member_categories', unique_categories)

print("Relations:", relation_map)
print("Statuses:", status_map)
print("Categories:", category_map)

cursor.close()
conn.close()
