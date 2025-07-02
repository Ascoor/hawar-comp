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
        DB::table('renewal_settings')->insert([
            [
                'id' => 1,
                'membership_type' => 'Primary',
                'fee' => 75.00,
                'billing_cycle_months' => 12,
                'created_at' => Carbon::now(),
                'updated_at' => Carbon::now(),
            ],
            [
                'id' => 2,
                'membership_type' => 'Family',
                'fee' => 25.00,
                'billing_cycle_months' => 12,
                'created_at' => Carbon::now(),
                'updated_at' => Carbon::now(),
            ],
        ]);
    }
}
