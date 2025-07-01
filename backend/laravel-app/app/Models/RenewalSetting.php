<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class RenewalSetting extends Model
{
    use HasFactory;

    protected $fillable = ['membership_type','fee','billing_cycle_months'];
}
