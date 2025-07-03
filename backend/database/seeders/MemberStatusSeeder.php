<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

use Illuminate\Support\Facades\DB;
class MemberStatusSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        DB::table('member_status')->insert([
            [
                'status_name' => 'Active',

                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'status_name' => 'Dropped',

                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'status_name' => 'Expired',

                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'status_name' => 'Suspended',

                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'status_name' => 'SonsOver25',

                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'status_name' => 'Deceased',

                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'status_name' => 'Paid',

                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'status_name' => 'Unpaid',

                'created_at' => now(),
                'updated_at' => now(),
            ],

        ]);
    }
}
