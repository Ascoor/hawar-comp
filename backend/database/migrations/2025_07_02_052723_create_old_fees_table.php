<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
public function up()
{
    Schema::create('old_fees', function (Blueprint $table) {
        $table->bigIncrements('id');
        $table->string('Fee_ID')->nullable();
        $table->string('Fee_Name')->nullable();
        $table->string('Fee_Mem_ID')->nullable();
        $table->string('Fee_Address')->nullable();
        $table->string('Fee_HomePhone')->nullable();
        $table->string('Fee_NID')->nullable();
        $table->string('Fee_Other1')->nullable();
        $table->string('Fee_Other2')->nullable();
        $table->string('Fee_Other3')->nullable();
        $table->string('Fee_Year')->nullable();
        $table->string('Fee_Amount')->nullable();
        $table->string('Fee_Date')->nullable();
        $table->string('Fee_RecieptNumber')->nullable();
        $table->string('Fee_Status')->nullable();
        $table->string('Mem_ID')->nullable();
        $table->string('Mem_Name')->nullable();
        $table->string('Mem_Code')->nullable();
        $table->string('Mem_BOD')->nullable();
        $table->string('Mem_NID')->nullable();
        $table->string('Mem_GraduationGrade')->nullable();
        $table->string('Mem_ParentMember')->nullable();
        $table->string('Mem_Sex')->nullable();
        $table->string('Mem_JobCategory')->nullable();
        $table->string('Mem_Job')->nullable();
        $table->string('Mem_MembershipType')->nullable();
        $table->string('Mem_Relegion')->nullable();
        $table->string('Mem_Address')->nullable();
        $table->string('Mem_JoinDate')->nullable();
        $table->string('Mem_Class')->nullable();
        $table->string('Mem_HomePhone')->nullable();
        $table->string('Mem_Mobile')->nullable();
        $table->string('Mem_Receiver')->nullable();
        $table->string('Mem_WorkPhone')->nullable();
        $table->string('Mem_Photo')->nullable();
        $table->text('Mem_Notes')->nullable();
        $table->string('Mem_LastPayedFees')->nullable();
        $table->string('Mem_Status')->nullable();
        $table->string('MemCard_MemberName')->nullable();
        $table->string('MemCard_MemberJobTitle')->nullable();
        $table->string('Mem_GraduationDesc')->nullable();
        $table->text('Mem_Notes_2')->nullable();
        $table->text('Mem_Notes_3')->nullable();
        $table->text('Mem_Notes_4')->nullable();
        $table->string('Mem_Relation')->nullable();
        $table->string('Mem_BoardDecision_Date')->nullable();
        $table->string('Mem_BoardDecision_Number')->nullable();
        $table->string('created_at')->nullable();
        $table->string('updated_at')->nullable();
    });
}

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('old_fees');
    }
};
