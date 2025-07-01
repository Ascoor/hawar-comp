<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Member;
use App\Models\Fee;
use Illuminate\Validation\Rule;

class MemberController extends Controller
{
    public function index(Request $request)
    {
        $query = Member::with(['category','relation','status','family','fees']);
        if ($request->filled('category')) {
            $query->whereHas('category', function($q) use ($request) {
                $q->where('name', $request->category);
            });
        }
        if ($request->filled('status')) {
            $query->whereHas('status', function($q) use ($request) {
                $q->where('name', $request->status);
            });
        }
        if ($request->filled('family')) {
            $query->where('family_id', $request->family);
        }
        $members = $query->paginate(10);
        return response()->json($members);
    }

    public function show($id)
    {
        $member = Member::with(['category','relation','status','family','fees'])
            ->findOrFail($id);
        return response()->json($member);
    }

    public function store(Request $request)
    {
        $data = $request->validate([
            'Mem_Name' => 'required|string',
            'Mem_Code' => 'nullable|string',
            'category_id' => 'nullable|exists:member_categories,id',
            'relation_id' => 'nullable|exists:member_relations,id',
            'status_id' => 'nullable|exists:member_statuses,id',
            'family_id' => 'nullable|exists:members,id'
        ]);
        $member = Member::create($data);
        return response()->json($member, 201);
    }

    public function update(Request $request, $id)
    {
        $member = Member::findOrFail($id);
        $data = $request->validate([
            'Mem_Name' => 'sometimes|string',
            'Mem_Code' => 'sometimes|string',
            'category_id' => 'nullable|exists:member_categories,id',
            'relation_id' => 'nullable|exists:member_relations,id',
            'status_id' => 'nullable|exists:member_statuses,id',
            'family_id' => 'nullable|exists:members,id'
        ]);
        $member->update($data);
        return response()->json($member);
    }

    public function destroy($id)
    {
        $member = Member::findOrFail($id);
        $member->delete();
        return response()->json(['message' => 'deleted']);
    }

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
