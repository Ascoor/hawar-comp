<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

use Illuminate\Support\Facades\DB;
class MemberRelationsSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        DB::table('member_relations')->insert([
            [
                'relation_name' => 'Owner',

                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'relation_name' => 'Husband',

                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'relation_name' => 'Wife',

                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'relation_name' => 'Son',

                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'relation_name' => 'daughter',

                'created_at' => now(),
                'updated_at' => now(),
            ],

        ]);
    }
}
