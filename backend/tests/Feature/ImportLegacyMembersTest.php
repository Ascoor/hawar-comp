<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\MemberCategory;
use App\Models\MemberRelation;
use App\Models\MemberStatus;

class ImportLegacyMembersTest extends TestCase
{
    use RefreshDatabase;

    public function test_import_command_inserts_member(): void
    {
        MemberCategory::create(['id' => 1, 'name' => 'Primary']);
        MemberRelation::create(['id' => 1, 'name' => 'Self']);
        MemberStatus::create(['id' => 1, 'name' => 'Active']);

        $csv = tempnam(sys_get_temp_dir(), 'legacy');
        file_put_contents($csv, "name,member_code,birth_date,join_date,gender,status,relation\n".
            "اختبار,100,1970-01-01,2024-01-01,M,Active,Self\n");

        $this->artisan('import:legacy-members '.$csv)
            ->assertExitCode(0);

        $this->assertDatabaseHas('members', [
            'Mem_Name' => 'اختبار',
            'Mem_Code' => '100',
        ]);
    }
}
