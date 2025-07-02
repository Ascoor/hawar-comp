# خطة ترحيل البيانات

توضح هذه الوثيقة خطوات ترحيل بيانات الأعضاء والاشتراكات من الملفات القديمة إلى قاعدة البيانات الجديدة داخل تطبيق Laravel.

## 1. تجهيز الجداول

```bash
php artisan migrate
php artisan db:seed
```

يتم إنشاء الجداول الجديدة مع تعبئة جداول القوائم (`member_categories` وغيرها).

## 2. تنظيف البيانات القديمة

استخدم أحد سكربتات Python في مجلد `backend/scripts` لتنظيف الملفات القديمة وتحويلها إلى CSV منسق. للملفات الصغيرة يكفي تشغيل `transform_members.py`:

```bash
python backend/scripts/transform_members.py path/to/legacy.sql --csv > clean.csv
```

أما عند التعامل مع ملفات كبيرة أو عناوين حقول مختلطة بالعربية والإنجليزية فينصح باستخدام السكربت الجديد `normalize_membership_csv.py` الذي يتعرف على الحقول المختلفة ويطبع النتيجة بالتنسيق التالي:

```bash
python backend/scripts/normalize_membership_csv.py path/to/legacy.csv > clean.csv
```

الملف الناتج يحتوي على الأعمدة:
`id,name,code,national_id,birth_date,gender,category,relation_type,status,parent_member_id,join_date,address,phone,mobile,notes,last_paid_fee`.

لدمج ملفات CSV الكبيرة الموجودة في `legacy_db_transformer/sqls/csv` وتحويلها
إلى نفس البنية النهائية يمكن تشغيل السكربت:

```bash
python legacy_db_transformer/rebuild_csv.py
```

سيقوم بإنشاء ملف `members_restructured.csv` بنفس أعمدة جدول `members` في
Laravel.

## 3. استيراد البيانات

بعد الحصول على الملف النظيف يتم تشغيل الأمر الآتي:

```bash
php artisan import:legacy-members clean.csv
```

يقوم الأمر بإضافة الأعضاء والرسوم في جداول النظام الجديدة ضمن معاملة واحدة، وتتم كتابة سجل بالنتيجة في `storage/logs/laravel.log`.

## 4. الجدولة التلقائية

يمكن إضافة جدولة في `app/Console/Kernel.php` لتشغيل الأمر دوريًا:

```php
protected function schedule(Schedule $schedule): void
{
    $schedule->command('import:legacy-members clean.csv')->daily();
}
```

## 5. التحقق بعد الترحيل

- تنفيذ اختبارات PHPUnit:

```bash
phpunit
```

- مراجعة عدد السجلات في جدول `members` ومطابقتها مع الملف النظيف.
- التأكد من عدم وجود سجلات رسوم في جدول `fees` بدون عضو مرتبط.

