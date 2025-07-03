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
            MemberRelationsSeeder::class,
            MemberStatusSeeder::class,
            MembershipRenewSettingSeeder::class,
        ]);

 
    }
}
