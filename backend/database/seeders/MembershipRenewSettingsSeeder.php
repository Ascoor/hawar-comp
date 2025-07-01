<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Carbon\Carbon;

/**
 * Seed membership renewal fees and settings.
 */
class MembershipRenewSettingsSeeder extends Seeder
{
    public function run(): void
    {
        DB::table('membership_renew_settings')->insert([
            [
                'id' => 1,
                'category_id' => 1,
                'year' => 2024,
                'fee_amount' => 75.00,
                'created_at' => Carbon::now(),
                'updated_at' => Carbon::now(),
            ],
            [
                'id' => 2,
                'category_id' => 2,
                'year' => 2024,
                'fee_amount' => 25.00,
                'created_at' => Carbon::now(),
                'updated_at' => Carbon::now(),
            ],
        ]);
    }
}
