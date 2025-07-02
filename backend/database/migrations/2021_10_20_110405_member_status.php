    <?php

    use Illuminate\Database\Migrations\Migration;
    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    class MemberStatus extends Migration
    {
        /**
         * Run the migrations.
         *+
        * @return void
        */
        public function up()
        {
            Schema::create('member_status', function (Blueprint $table) {
                $table->BigIncrements('id');
                $table->string('status_name');
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
            Schema::dropIfExists('member_status');

        }
    }
