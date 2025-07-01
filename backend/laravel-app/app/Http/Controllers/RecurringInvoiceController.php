<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\RecurringInvoice;

class RecurringInvoiceController extends Controller
{
    public function index()
    {
        return response()->json(RecurringInvoice::all());
    }

    public function store(Request $request)
    {
        $data = $request->validate([
            'member_id' => 'required|exists:members,id',
            'amount' => 'required|numeric',
            'interval_months' => 'required|integer',
            'next_run_at' => 'required|date'
        ]);
        $rec = RecurringInvoice::create($data);
        return response()->json($rec, 201);
    }

    public function update(Request $request, $id)
    {
        $rec = RecurringInvoice::findOrFail($id);
        $data = $request->validate([
            'amount' => 'sometimes|numeric',
            'interval_months' => 'sometimes|integer',
            'next_run_at' => 'sometimes|date'
        ]);
        $rec->update($data);
        return response()->json($rec);
    }

    public function destroy($id)
    {
        $rec = RecurringInvoice::findOrFail($id);
        $rec->delete();
        return response()->json(['message' => 'deleted']);
    }
}
