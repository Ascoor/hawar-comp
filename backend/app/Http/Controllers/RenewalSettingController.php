<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\RenewalSetting;

class RenewalSettingController extends Controller
{
    public function index()
    {
        return response()->json(RenewalSetting::all());
    }

    public function show($id)
    {
        return response()->json(RenewalSetting::findOrFail($id));
    }

    public function update(Request $request, $id)
    {
        $setting = RenewalSetting::findOrFail($id);
        $data = $request->validate([
            'membership_type' => 'sometimes|string',
            'fee' => 'sometimes|numeric',
            'billing_cycle_months' => 'sometimes|integer'
        ]);
        $setting->update($data);
        return response()->json($setting);
    }
}
