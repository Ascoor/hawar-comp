<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\DB;

return new class extends Migration {
    public function up()
    {
        // Drop the view if it exists to avoid "already exists" error
        DB::statement('DROP VIEW IF EXISTS VW_MembersFees');

        // Create the view with the desired query
        DB::statement("
            CREATE VIEW VW_MembersFees AS
            SELECT m.id as Mem_ID, m.Mem_Name, m.Mem_Code, m.Mem_Address, m.Mem_HomePhone,
                   m.Mem_Mobile, m.Mem_WorkPhone, f.id as Fee_ID, f.Fee_Year, f.Fee_Amount,
                   f.Fee_Date, f.Fee_RecieptNumber, f.Fee_Status, f.Fee_User_ID
            FROM members m
            INNER JOIN fees f ON m.id = f.member_id
            WHERE m.Mem_Status = 21 AND f.Fee_Status = 1
        ");
    }

    public function down()
    {
        // Drop the view on rollback
        DB::statement('DROP VIEW IF EXISTS VW_MembersFees');
    }
};
