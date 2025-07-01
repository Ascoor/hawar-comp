<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up()
    {
        Schema::table('members', function (Blueprint $table) {
            $table->foreignId('category_id')->nullable()->constrained('member_categories');
            $table->foreignId('relation_id')->nullable()->constrained('member_relations');
            $table->foreignId('status_id')->nullable()->constrained('member_statuses');
            $table->foreignId('family_id')->nullable()->references('id')->on('members');
        });
    }

    public function down()
    {
        Schema::table('members', function (Blueprint $table) {
            $table->dropForeign(['category_id']);
            $table->dropForeign(['relation_id']);
            $table->dropForeign(['status_id']);
            $table->dropForeign(['family_id']);
            $table->dropColumn(['category_id','relation_id','status_id','family_id']);
        });
    }
};
