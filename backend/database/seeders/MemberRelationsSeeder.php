<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class MemberRelationsSeeder extends Seeder
{
    public function run(): void
    {
        $relations = [
            'ابن',
            'ابنة',
            'زوج',
            'زوجة',
            'والد الزوج',
            'والدة الزوج',
            'والد الزوجة',
            'والدة الزوجة',
        ];

        foreach ($relations as $name) {
            DB::table('member_relations')->insert([
                'name' => $name,
                'created_at' => now(),
                'updated_at' => now(),
            ]);
        }
    }
}
