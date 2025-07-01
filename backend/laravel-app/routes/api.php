<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\MemberController;

Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);
Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/member-count', [MemberController::class, 'memberCount']);
    Route::get('/members/search', [MemberController::class, 'search']);
    Route::get('/user/{id}', [AuthController::class, 'profile']);
});
