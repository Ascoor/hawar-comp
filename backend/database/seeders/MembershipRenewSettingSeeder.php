<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

use Illuminate\Support\Facades\DB;

class MembershipRenewSettingSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        DB::table('membership_renew_settings')->insert([
            [
                'main_annual_fees'=>60,
                'affiliate_annual_fees'=>30,
                'administrative_expenses'=>20,
                'card_printing'=>15,
                'disabled_stamp'=>5,
                'martyr_stamp'=>5,
                'enhancing_constructions'=>0,

                'created_at' => now(),
                'updated_at' => now(),
            ],
        ]);
    }
}
