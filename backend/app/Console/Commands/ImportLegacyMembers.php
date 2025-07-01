<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use App\Models\Member;
use App\Models\MemberCategory;
use App\Models\MemberRelation;
use App\Models\MemberStatus;
use App\Models\Fee;

class ImportLegacyMembers extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'import:legacy-members {file}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Import cleaned legacy member CSV into normalized tables';

    /**
     * Execute the console command.
     */
    public function handle(): int
    {
        $path = $this->argument('file');
        if (!file_exists($path)) {
            $this->error("File not found: $path");
            return 1;
        }

        DB::beginTransaction();
        try {
            $rows = array_map('str_getcsv', file($path));
            $header = array_map('trim', array_shift($rows));
            foreach ($rows as $row) {
                $data = array_combine($header, $row);
                $member = Member::create([
                    'Mem_Name'   => $data['name'] ?? null,
                    'Mem_Code'   => $data['member_code'] ?? null,
                    'Mem_BOD'    => $data['birth_date'] ?? null,
                    'Mem_NID'    => $data['national_id'] ?? null,
                    'Mem_JoinDate' => $data['join_date'] ?? null,
                    'Mem_Sex'    => $data['gender'] ?? null,
                    'category_id' => MemberCategory::where('name', $data['category'])->value('id'),
                    'relation_id' => MemberRelation::where('name', $data['relation'])->value('id'),
                    'status_id'   => MemberStatus::where('name', $data['status'])->value('id'),
                ]);

                if (!empty($data['fee_amount'])) {
                    Fee::create([
                        'member_id' => $member->id,
                        'fiscal_year' => $data['fee_year'] ?? null,
                        'amount' => $data['fee_amount'],
                    ]);
                }
            }
            DB::commit();
            Log::info('Legacy import finished successfully');
            $this->info('Import completed');
            return 0;
        } catch (\Throwable $e) {
            DB::rollBack();
            Log::error('Legacy import failed: '.$e->getMessage());
            $this->error($e->getMessage());
            return 1;
        }
    }
}
