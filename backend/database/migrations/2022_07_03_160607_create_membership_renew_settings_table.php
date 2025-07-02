<?php

// Import the classes that are needed for the migration
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

// Define the migration class that creates the membership_renew_settings table
class CreateMembershipRenewSettingsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        // Create the table using the Schema facade
        Schema::create('membership_renew_settings', function (Blueprint $table) {
            // Add an auto-incrementing id column as the primary key
            $table->increments('id');
            // Add a main_annual_fees column that stores the main annual fees for membership renewal
            $table->integer('main_annual_fees')->default(60);
            // Add an affiliate_annual_fees column that stores the affiliate annual fees for membership renewal
            $table->integer('affiliate_annual_fees')->default(30);
            // Add an administrative_expenses column that stores the administrative expenses for membership renewal
            $table->integer('administrative_expenses')->default(20);
            // Add a card_printing column that stores the card printing fees for membership renewal
            $table->integer('card_printing')->default(15);
            // Add a disabled_stamp column that stores the disabled stamp fees for membership renewal
            $table->integer('disabled_stamp')->default(5);
            // Add a martyr_stamp column that stores the martyr stamp fees for membership renewal
            $table->integer('martyr_stamp')->default(5);
            // Add an enhancing_constructions column that stores the enhancing constructions fees for membership renewal
            $table->integer('enhancing_constructions')->default(0);

            // Add timestamps columns to track the creation and update dates of the records
            $table->timestamps();
        });

    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        // Drop the table using the Schema facade
        Schema::dropIfExists('membership_renew_settings');
    }
}
