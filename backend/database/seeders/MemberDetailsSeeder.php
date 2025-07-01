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
        DB::table('member_details')->insert([
            [
                'id' => 1,
                'member_code' => '1938',
                'name' => 'إيمان عبد العليم محمد إسماعيل',
                'national_id' => '1200121',
                'birth_date' => '1974-08-21',
                'join_date' => '2006-08-14',
                'gender' => 'F',
                'category_id' => 1,
                'relation_id' => 1,
                'status_id' => 1,
                'address' => '10مساكن المينا ع 10 شقه8',
                'phone' => '0163448944',
                'notes' => 'رقم الزوج1937',
                'created_at' => Carbon::now(),
                'updated_at' => Carbon::now(),
            ],
            [
                'id' => 2,
                'member_code' => '1968',
                'name' => 'أمجد أحمد إبراهيم إبراهيم النجار',
                'national_id' => '1201938',
                'birth_date' => '1975-03-20',
                'join_date' => '2006-08-14',
                'gender' => 'M',
                'category_id' => 1,
                'relation_id' => 1,
                'status_id' => 1,
                'address' => '5ش أبو هريرة تقسيم سامية الجمل',
                'phone' => '01221088209',
                'notes' => 'رقم الزوجة 1969',
                'created_at' => Carbon::now(),
                'updated_at' => Carbon::now(),
            ],
            [
                'id' => 3,
                'member_code' => '9093',
                'name' => 'ولاء صبري محمود سالم صيام',
                'national_id' => '28109120103706',
                'birth_date' => '1981-09-12',
                'join_date' => '2022-07-13',
                'gender' => 'F',
                'category_id' => 1,
                'relation_id' => 1,
                'status_id' => 1,
                'address' => '11 ش الترعه بجوار مخازن ربيع للسيراميك',
                'phone' => '01222216237',
                'notes' => null,
                'created_at' => Carbon::now(),
                'updated_at' => Carbon::now(),
            ],
        ]);
    }
}
