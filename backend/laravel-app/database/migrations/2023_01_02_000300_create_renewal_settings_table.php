<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up()
    {
        Schema::create('renewal_settings', function (Blueprint $table) {
            $table->id();
            $table->string('membership_type');
            $table->decimal('fee', 8, 2);
            $table->integer('billing_cycle_months')->default(12);
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('renewal_settings');
    }
};
