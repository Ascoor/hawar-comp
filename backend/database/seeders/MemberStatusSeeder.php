<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

/**
 * Seed the member_status lookup table.
 */
class MemberStatusSeeder extends Seeder
{
    public function run(): void
    {
        DB::table('member_status')->insert([
            ['id' => 1, 'name' => 'Active'],
            ['id' => 2, 'name' => 'Suspended'],
            ['id' => 3, 'name' => 'Expired'],
        ]);
    }
}
