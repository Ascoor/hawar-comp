<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Member;
use App\Models\Fee;

class MemberController extends Controller
{
    public function memberCount()
    {
        $workMemberCount = Member::where('MembershipType', 'عضو عامل')->count();
        $partMemberCount = Member::where('MembershipType', 'عضو تابع')->count();
        $maleCount = Member::where('Mem_Sex', 'ذكر')->count();
        $femaleCount = Member::where('Mem_Sex', 'أنثى')->count();
        $countOver25 = Member::where('Mem_BOD', '<=', now()->subYears(25))->count();
        $countOver60 = Member::where('Mem_BOD', '<=', now()->subYears(60))->count();
        $membersPaidCurrentFiscalYear = Fee::where('fiscal_year', now()->year)->distinct('member_id')->count('member_id');
        $membersPaidPreviousFiscalYear = Fee::where('fiscal_year', now()->subYear()->year)->distinct('member_id')->count('member_id');
        $membersIgnored = Member::where('Mem_Status', 'مسقطة - مفصول')->count();

        return response()->json([
            'workMemberCount' => $workMemberCount,
            'partMemberCount' => $partMemberCount,
            'maleCount' => $maleCount,
            'femaleCount' => $femaleCount,
            'countOver25' => $countOver25,
            'countOver60' => $countOver60,
            'membersPaidCurrentFiscalYear' => $membersPaidCurrentFiscalYear,
            'membersPaidPreviousFiscalYear' => $membersPaidPreviousFiscalYear,
            'membersIgnored' => $membersIgnored
        ]);
    }

    public function search(Request $request)
    {
        $term = $request->query('searchTerm');
        $members = Member::where('Mem_Name', 'like', "%{$term}%")
            ->orWhere('Mem_Code', 'like', "%{$term}%")
            ->get();
        return response()->json($members);
    }
}
