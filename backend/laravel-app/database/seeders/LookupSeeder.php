<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\MemberCategory;
use App\Models\MemberRelation;
use App\Models\MemberStatus;

class LookupSeeder extends Seeder
{
    public function run()
    {
        MemberCategory::insert([
            ['name' => 'work'],
            ['name' => 'affiliate'],
            ['name' => 'founding']
        ]);

        MemberRelation::insert([
            ['name' => 'parent'],
            ['name' => 'child'],
            ['name' => 'spouse']
        ]);

        MemberStatus::insert([
            ['name' => 'active'],
            ['name' => 'inactive'],
            ['name' => 'suspended']
        ]);
    }
}
