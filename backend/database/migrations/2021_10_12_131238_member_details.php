<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class MemberDetails extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {

        Schema::create('member_details', function (Blueprint $table) {
            $table->id();
            $table->string('member_id');
            $table->unsignedInteger('family_id');
            $table->string('name');
            $table->unsignedBigInteger('national_id')->unique();
            $table->unsignedInteger('user_id');
            $table->string('gender');
            $table->unsignedInteger('category_id');
            $table->unsignedInteger('relation_id');
            $table->unsignedInteger('status_id');
            $table->string('phone');
            $table->string('date_of_birth');
            $table->string('email');
            $table->string('address');
            $table->string('city');
            $table->string('state');
            $table->string('age');
            $table->string('profession');
            $table->string('religion');
            $table->unsignedInteger('country_id');
            $table->unsignedBigInteger('nationality_id');
            $table->string('renewal_status')->default('renewed');
            $table->string('postal_code')->nullable();
            $table->string('face_book')->nullable();
            $table->string('twitter')->nullable();
            $table->text('note')->nullable();
            $table->text('note_2')->nullable();
            $table->text('note_3')->nullable();
            $table->text('note_4')->nullable();
            $table->date('last_paid_fiscal_year');
            $table->date('date_of_the_board_of_directors');
            $table->string('decision_number');
            $table->string('memCard_MemberName');
            $table->string('remarks');
            $table->string('mem_GraduationDesc');
            $table->string('mem_WorkPhone');
            $table->string('mem_HomePhone');
            $table->string('email_notifications');
            $table->unsignedInteger('player')->nullable();
            $table->unsignedInteger('team_id')->nullable();
            // $table->unique(['id', 'national_id']);
            $table->timestamps();
            //            $table->foreign('category_id')->references('id')->on('member_category')->onUpdate('cascade');

        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('member_details');
    }
}