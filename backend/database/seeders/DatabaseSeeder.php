<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        // Lookup tables first
        $this->call([
            MemberCategorySeeder::class,
            MemberRelationSeeder::class,
            MemberStatusSeeder::class,
            MembershipRenewSettingsSeeder::class,
        ]);

        // Core member data
        $this->call([
            MemberDetailsSeeder::class,
        ]);
    }
}
