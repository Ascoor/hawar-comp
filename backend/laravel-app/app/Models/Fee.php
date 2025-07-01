<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use App\Models\Member;

class Fee extends Model
{
    use HasFactory;

    protected $table = 'fees';
    protected $fillable = [
        'member_id',
        'amount',
        'fiscal_year'
    ];

    public function member()
    {
        return $this->belongsTo(Member::class);
    }
}
