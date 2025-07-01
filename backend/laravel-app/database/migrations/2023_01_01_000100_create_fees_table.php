<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up()
    {
        Schema::create('fees', function (Blueprint $table) {
            $table->id();
            $table->foreignId('member_id')->constrained('members');
            $table->integer('Fee_Year');
            $table->decimal('Fee_Amount', 10, 2);
            $table->date('Fee_Date')->nullable();
            $table->string('Fee_RecieptNumber')->nullable();
            $table->integer('Fee_Status')->nullable();
            $table->integer('Fee_User_ID')->nullable();
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('fees');
    }
};
