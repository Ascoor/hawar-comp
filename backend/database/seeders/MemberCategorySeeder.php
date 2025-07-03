<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class MemberCategorySeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        DB::table('member_category')->insert([
            [
                'category_name' => 'working_member',
                
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'category_name' => 'affiliate_member',
                
                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'category_name' => 'founding_member',
                
                'created_at' => now(),
                'updated_at' => now(),
            ],
 [
                'category_name' => 'honorary_member',

                'created_at' => now(),
                'updated_at' => now(),
            ],
 [
                'category_name' => 'seasonal_member',

                'created_at' => now(),
                'updated_at' => now(),
            ],
 [
                'category_name' => 'athletic_member',

                'created_at' => now(),
                'updated_at' => now(),
            ],
            [
                'category_name' => 'a_permit',

                'created_at' => now(),
                'updated_at' => now(),
            ],

        ]);
    }
}
