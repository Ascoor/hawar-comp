<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

/**
 * Seed the member_category lookup table.
 */
class MemberCategorySeeder extends Seeder
{
    public function run(): void
    {
        DB::table('member_category')->insert([
            ['id' => 1, 'name' => 'Primary'],
            ['id' => 2, 'name' => 'Family'],
            ['id' => 3, 'name' => 'Honorary'],
        ]);
    }
}
