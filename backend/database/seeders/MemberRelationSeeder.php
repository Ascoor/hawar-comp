<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

/**
 * Seed the member_relation lookup table.
 */
class MemberRelationSeeder extends Seeder
{
    public function run(): void
    {
        DB::table('member_relation')->insert([
            ['id' => 1, 'name' => 'Self'],
            ['id' => 2, 'name' => 'Spouse'],
            ['id' => 3, 'name' => 'Child'],
            ['id' => 4, 'name' => 'Parent'],
        ]);
    }
}
