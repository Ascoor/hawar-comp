<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up()
    {
        Schema::create('recurring_invoices', function (Blueprint $table) {
            $table->id();
            $table->foreignId('member_id')->constrained('members');
            $table->decimal('amount', 8, 2);
            $table->integer('interval_months')->default(12);
            $table->date('next_run_at');
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('recurring_invoices');
    }
};
