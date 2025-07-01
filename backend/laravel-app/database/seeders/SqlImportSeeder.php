<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Storage;

class SqlImportSeeder extends Seeder
{
    public function run()
    {
        $path = base_path('backend/sqls/members.sql');
        if (file_exists($path)) {
            DB::unprepared(file_get_contents($path));
        }
    }
}
