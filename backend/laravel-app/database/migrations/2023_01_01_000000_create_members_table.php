<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up()
    {
        Schema::create('members', function (Blueprint $table) {
            $table->id();
            $table->string('Mem_Name');
            $table->string('Mem_Code')->nullable();
            $table->date('Mem_BOD')->nullable();
            $table->string('Mem_NID')->nullable();
            $table->string('Mem_GraduationGrade')->nullable();
            $table->integer('Mem_ParentMember')->nullable();
            $table->string('Mem_Sex', 10)->nullable();
            $table->string('Mem_JobCategory')->nullable();
            $table->string('Mem_Job')->nullable();
            $table->string('Mem_MembershipType')->nullable();
            $table->string('Mem_Relegion')->nullable();
            $table->string('Mem_Address')->nullable();
            $table->date('Mem_JoinDate')->nullable();
            $table->string('Mem_Class')->nullable();
            $table->string('Mem_HomePhone', 20)->nullable();
            $table->string('Mem_Mobile', 20)->nullable();
            $table->string('Mem_Receiver')->nullable();
            $table->string('Mem_WorkPhone', 20)->nullable();
            $table->string('Mem_Photo')->nullable();
            $table->text('Mem_Notes')->nullable();
            $table->string('Mem_LastPayedFees')->nullable();
            $table->integer('Mem_Status')->nullable();
            $table->string('MemCard_MemberName')->nullable();
            $table->string('MemCard_MemberJobTitle')->nullable();
            $table->string('Mem_GraduationDesc')->nullable();
            $table->text('Mem_Notes_2')->nullable();
            $table->text('Mem_Notes_3')->nullable();
            $table->text('Mem_Notes_4')->nullable();
            $table->string('Mem_Relation')->nullable();
            $table->date('Mem_BoardDecision_Date')->nullable();
            $table->string('Mem_BoardDecision_Number')->nullable();
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('members');
    }
};
