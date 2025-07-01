<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\MemberStatus;

class MemberStatusController extends Controller
{
    public function index()
    {
        return response()->json(MemberStatus::all());
    }

    public function store(Request $request)
    {
        $data = $request->validate(['name' => 'required']);
        $status = MemberStatus::create($data);
        return response()->json($status, 201);
    }

    public function update(Request $request, $id)
    {
        $status = MemberStatus::findOrFail($id);
        $data = $request->validate(['name' => 'required']);
        $status->update($data);
        return response()->json($status);
    }

    public function destroy($id)
    {
        $status = MemberStatus::findOrFail($id);
        $status->delete();
        return response()->json(['message' => 'deleted']);
    }
}
