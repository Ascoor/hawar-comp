<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\MemberRelation;

class MemberRelationController extends Controller
{
    public function index()
    {
        return response()->json(MemberRelation::all());
    }

    public function store(Request $request)
    {
        $data = $request->validate(['name' => 'required']);
        $rel = MemberRelation::create($data);
        return response()->json($rel, 201);
    }

    public function update(Request $request, $id)
    {
        $rel = MemberRelation::findOrFail($id);
        $data = $request->validate(['name' => 'required']);
        $rel->update($data);
        return response()->json($rel);
    }

    public function destroy($id)
    {
        $rel = MemberRelation::findOrFail($id);
        $rel->delete();
        return response()->json(['message' => 'deleted']);
    }
}
