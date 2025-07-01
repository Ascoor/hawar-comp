<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Invoice;

class NotificationController extends Controller
{
    public function index()
    {
        $upcoming = Invoice::where('paid', false)->whereDate('due_date', '>=', now())
            ->whereDate('due_date', '<=', now()->addDays(30))->get();
        $unpaid = Invoice::where('paid', false)->whereDate('due_date', '<', now())->get();
        return response()->json([
            'upcoming_renewals' => $upcoming,
            'unpaid_invoices' => $unpaid,
        ]);
    }
}
