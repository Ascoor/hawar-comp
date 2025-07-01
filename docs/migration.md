# خطة ترحيل البيانات

توضح هذه الوثيقة خطوات ترحيل بيانات الأعضاء والاشتراكات من الملفات القديمة إلى قاعدة البيانات الجديدة داخل تطبيق Laravel.

## 1. تجهيز الجداول

```bash
php artisan migrate
php artisan db:seed
```

يتم إنشاء الجداول الجديدة مع تعبئة جداول القوائم (`member_categories` وغيرها).

## 2. تنظيف البيانات القديمة

استخدم السكربت Python الموجود في `backend/scripts/transform_members.py` لتحويل ملف SQL أو CSV القديم إلى ملف CSV نظيف:

```bash
python backend/scripts/transform_members.py path/to/legacy.csv > clean.csv
```

يجب أن يحتوي الملف الناتج على الحقول:
`name,member_code,national_id,birth_date,join_date,gender,status,relation,fee_year,fee_amount`.

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

