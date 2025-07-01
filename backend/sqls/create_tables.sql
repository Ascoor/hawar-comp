-- SQL schema for hawar-comp application
-- This script creates the core tables along with foreign-key
-- relationships used by the view VW_MembersFees.

-- Drop tables if they already exist
DROP TABLE IF EXISTS Fees;
DROP TABLE IF EXISTS Members;

-- Members table stores basic information about club members
CREATE TABLE Members (
    Mem_ID INT PRIMARY KEY,
    Mem_Name VARCHAR(255) NOT NULL,
    Mem_Code VARCHAR(50),
    Mem_BOD DATE,
    Mem_NID VARCHAR(50),
    Mem_GraduationGrade VARCHAR(100),
    Mem_ParentMember INT,
    Mem_Sex VARCHAR(10),
    Mem_JobCategory VARCHAR(100),
    Mem_Job VARCHAR(100),
    Mem_MembershipType VARCHAR(50),
    Mem_Relegion VARCHAR(50),
    Mem_Address VARCHAR(255),
    Mem_JoinDate DATE,
    Mem_Class VARCHAR(50),
    Mem_HomePhone VARCHAR(20),
    Mem_Mobile VARCHAR(20),
    Mem_Receiver VARCHAR(255),
    Mem_WorkPhone VARCHAR(20),
    Mem_Photo VARCHAR(255),
    Mem_Notes TEXT,
    Mem_LastPayedFees VARCHAR(50),
    Mem_Status INT,
    MemCard_MemberName VARCHAR(255),
    MemCard_MemberJobTitle VARCHAR(255),
    Mem_GraduationDesc VARCHAR(255),
    Mem_Notes_2 TEXT,
    Mem_Notes_3 TEXT,
    Mem_Notes_4 TEXT,
    Mem_Relation VARCHAR(50),
    Mem_BoardDecision_Date DATE,
    Mem_BoardDecision_Number VARCHAR(50),
    created_at DATETIME,
    updated_at DATETIME
);

-- Fees table stores annual membership fees
CREATE TABLE Fees (
    Fee_ID INT PRIMARY KEY AUTO_INCREMENT,
    Fee_Mem_ID INT NOT NULL,
    Fee_Year INT NOT NULL,
    Fee_Amount DECIMAL(10,2) NOT NULL,
    Fee_Date DATE,
    Fee_RecieptNumber VARCHAR(50),
    Fee_Status INT,
    Fee_User_ID INT,
    CONSTRAINT fk_fees_member FOREIGN KEY (Fee_Mem_ID)
        REFERENCES Members(Mem_ID)
);
