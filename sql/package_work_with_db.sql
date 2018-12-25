Create or replace Package work_with_db as
    Procedure add_db(db_name in Database.database_name%TYPE, user_login in Database.user_login_fk%TYPE, message out STRING);
    
    Procedure delete_db(db_name in Database.database_name%TYPE, user_login in Database.user_login_fk%TYPE);
End work_with_db;
/

Create or replace package body work_with_db as
    Procedure add_db(db_name in Database.database_name%TYPE, user_login in Database.user_login_fk%TYPE, message out STRING) 
        is
            is_exist INTEGER :=0;
        Begin
            Select count(*) into is_exist
            From Database
            Where database_name = db_name;
            
            If is_exist = 0 Then
                Insert into Database (database_name, user_login_fk, database_size, database_time)
                    Values (db_name, user_login, 150.0, current_timestamp);
            Else
                Update Database
                Set deleted = null, database_time = current_timestamp
                Where database_name = db_name and user_login_fk = user_login;
            End if;
            
            Commit;
            message := 'Database '||db_name||' successfully created';
        Exception
            When OTHERS Then
                If INSTR(SQLERRM, 'DATABASE_NAME_CONTENT') != 0 Then
                    message := 'You entered invalid database path.';
                Elsif INSTR(SQLERRM, 'EXCEL_FILE_NAME_LENGTH') != 0 Then
                    message := 'Current database name is too long (database name length should be less or equal than 30 symbols).';
                Else
                    message := (SQLCODE || ' ' || SQLERRM);
                End if;
        end add_db;
        
    Procedure delete_db(db_name in Database.database_name%TYPE, user_login in Database.user_login_fk%TYPE) 
        is
        begin        
            Update Database
                Set deleted = current_timestamp
                Where database_name = db_name and user_login_fk = user_login;
            Commit;
        end delete_db;
    end work_with_db;
/