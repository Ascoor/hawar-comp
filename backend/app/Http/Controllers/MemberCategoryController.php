<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\MemberCategory;

class MemberCategoryController extends Controller
{
    public function index()
    {
        return response()->json(MemberCategory::all());
    }

    public function store(Request $request)
    {
        $data = $request->validate(['name' => 'required']);
        $cat = MemberCategory::create($data);
        return response()->json($cat, 201);
    }

    public function update(Request $request, $id)
    {
        $cat = MemberCategory::findOrFail($id);
        $data = $request->validate(['name' => 'required']);
        $cat->update($data);
        return response()->json($cat);
    }

    public function destroy($id)
    {
        $cat = MemberCategory::findOrFail($id);
        $cat->delete();
        return response()->json(['message' => 'deleted']);
    }
}
