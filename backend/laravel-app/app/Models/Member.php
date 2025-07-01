<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use App\Models\MemberCategory;
use App\Models\MemberRelation;
use App\Models\MemberStatus;
use App\Models\Fee;

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
        'Mem_Status',
        'category_id',
        'relation_id',
        'status_id',
        'family_id'
    ];

    public function category()
    {
        return $this->belongsTo(MemberCategory::class, 'category_id');
    }

    public function relation()
    {
        return $this->belongsTo(MemberRelation::class, 'relation_id');
    }

    public function status()
    {
        return $this->belongsTo(MemberStatus::class, 'status_id');
    }

    public function family()
    {
        return $this->belongsTo(Member::class, 'family_id');
    }

    public function fees()
    {
        return $this->hasMany(Fee::class, 'member_id');
    }
}
