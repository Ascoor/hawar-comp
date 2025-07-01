<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Member extends Model
{
    use HasFactory;

    protected $table = 'members';
    protected $fillable = [
        'Mem_Name',
        'Mem_Code',
        'Mem_BOD',
        'Mem_Sex',
        'MembershipType',
        'Mem_Status'
    ];
}
