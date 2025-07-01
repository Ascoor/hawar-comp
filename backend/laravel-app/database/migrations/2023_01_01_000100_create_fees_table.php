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
            $table->decimal('amount', 8, 2);
            $table->string('fiscal_year');
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('fees');
    }
};
