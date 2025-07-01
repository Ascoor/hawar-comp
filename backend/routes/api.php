<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\MemberController;
use App\Http\Controllers\MemberCategoryController;
use App\Http\Controllers\MemberRelationController;
use App\Http\Controllers\MemberStatusController;
use App\Http\Controllers\RenewalSettingController;
use App\Http\Controllers\InvoiceController;
use App\Http\Controllers\RecurringInvoiceController;
use App\Http\Controllers\NotificationController;
use Illuminate\Http\Request;

Route::middleware(['auth:sanctum'])->get('/user', function (Request $request) {
    return $request->user();
});

Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);
Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/member-count', [MemberController::class, 'memberCount']);
    Route::get('/members/search', [MemberController::class, 'search']);
    Route::get('/user/{id}', [AuthController::class, 'profile']);

    Route::apiResource('members', MemberController::class);
    Route::apiResource('member-categories', MemberCategoryController::class);
    Route::apiResource('member-relations', MemberRelationController::class);
    Route::apiResource('member-statuses', MemberStatusController::class);
    Route::apiResource('renewal-settings', RenewalSettingController::class)->only(['index','show','update']);
    Route::apiResource('invoices', InvoiceController::class);
    Route::apiResource('recurring-invoices', RecurringInvoiceController::class);
    Route::get('/notifications', [NotificationController::class, 'index']);
});
