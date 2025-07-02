<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Carbon\Carbon;

/**
 * Seed core member details using normalized sample records.
 */
class MemberDetailsSeeder extends Seeder
{
    public function run(): void
    {
        DB::table('members')->insert([
            [
                'id' => 1,
                'Mem_Code' => '1938',
                'Mem_Name' => 'إيمان عبد العليم محمد إسماعيل',
                'Mem_NID' => '1200121',
                'Mem_BOD' => '1974-08-21',
                'Mem_JoinDate' => '2006-08-14',
                'Mem_Sex' => 'F',
                'category_id' => 1,
                'relation_id' => 1,
                'status_id' => 1,
                'Mem_Address' => '10مساكن المينا ع 10 شقه8',
                'Mem_Mobile' => '0163448944',
                'Mem_Notes' => 'رقم الزوج1937',
                'created_at' => Carbon::now(),
                'updated_at' => Carbon::now(),
            ],
            [
                'id' => 2,
                'Mem_Code' => '1968',
                'Mem_Name' => 'أمجد أحمد إبراهيم إبراهيم النجار',
                'Mem_NID' => '1201938',
                'Mem_BOD' => '1975-03-20',
                'Mem_JoinDate' => '2006-08-14',
                'Mem_Sex' => 'M',
                'category_id' => 1,
                'relation_id' => 1,
                'status_id' => 1,
                'Mem_Address' => '5ش أبو هريرة تقسيم سامية الجمل',
                'Mem_Mobile' => '01221088209',
                'Mem_Notes' => 'رقم الزوجة 1969',
                'created_at' => Carbon::now(),
                'updated_at' => Carbon::now(),
            ],
            [
                'id' => 3,
                'Mem_Code' => '9093',
                'Mem_Name' => 'ولاء صبري محمود سالم صيام',
                'Mem_NID' => '28109120103706',
                'Mem_BOD' => '1981-09-12',
                'Mem_JoinDate' => '2022-07-13',
                'Mem_Sex' => 'F',
                'category_id' => 1,
                'relation_id' => 1,
                'status_id' => 1,
                'Mem_Address' => '11 ش الترعه بجوار مخازن ربيع للسيراميك',
                'Mem_Mobile' => '01222216237',
                'Mem_Notes' => null,
                'created_at' => Carbon::now(),
                'updated_at' => Carbon::now(),
            ],
        ]);
    }
}
