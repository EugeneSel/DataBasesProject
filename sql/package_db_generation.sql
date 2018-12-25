Create or replace package db_generation as
    Type rowRule is record(
        data_address Rule.rule_data_address%TYPE
    );
    
    Type tableRule is table of rowRule;
    
    Type rowDBGeneration is record(
        db_generation_time "Database generation".database_generation_time%TYPE,
        new_db_name "Database generation".new_database_name%TYPE,
        excel_file_name "Database generation".excel_file_name_fk%TYPE,
        user_login "Database generation".user_login_fk%TYPE,
        rule_data_address "Database generation".rule_data_address_fk%TYPE,
        db_name "Database generation".database_name_fk%TYPE
    );
    
    Type tableDBGeneration is table of rowDBGeneration;
    
    Procedure choose_data(file_name in "Excel file".excel_file_name%TYPE, current_user_login in Rule.user_login_fk%TYPE, cell_address in Rule.rule_data_address%TYPE, db_name in Database.database_name%TYPE, message out STRING);
    
    Function create_new_db(db_name "Database generation".new_database_name%TYPE)
    Return tableDBGeneration
    Pipelined;
End db_generation;
/

Create or replace package body db_generation as
    Procedure choose_data(file_name in "Excel file".excel_file_name%TYPE, current_user_login in Rule.user_login_fk%TYPE, cell_address in Rule.rule_data_address%TYPE, db_name in Database.database_name%TYPE, message out STRING) 
    is
        is_empty Number(1, 0);
        
        Cursor rule_list is
            Select rule_data_address 
            From Rule
            Where excel_file_name_fk = file_name;
            
            Cursor file_list is
                Select *
                From "Excel file";
                
            is_exist Number(1, 0);
        begin
            is_exist := 0;
            
            For current_element in file_list
            Loop
                If file_name = current_element.excel_file_name Then
                    is_empty := 0;
                    For current_element in rule_list
                    Loop
                        If cell_address = current_element.rule_data_address Then
                            is_empty := 1;
                            exit;
                        End if;
                    End loop;
                    
                    If is_empty = 1 Then
                        Insert Into "Database generation" (excel_file_name_fk, user_login_fk, rule_data_address_fk, database_generation_time, new_database_name, database_name_fk)
                            Values(file_name, current_user_login, cell_address, current_timestamp, db_name, '');
                        Commit;
                    Else
                        message := 'Current '||cell_address||' cell is empty';
                    End if;
                    
                    is_exist := 1;
                    message := 'Database '||db_name||' generated successfully';
                    Exit;
                End if;
            End loop;
            
            If is_exist = 0 Then
                message := 'Current excel file does not exist';
            End if;
        Exception
            When OTHERS Then
                If INSTR(SQLERRM, 'DATABASE_NAME_CONTENT') != 0 Then
                    message := 'You entered invalid database path.';
                Elsif INSTR(SQLERRM, 'EXCEL_FILE_NAME_LENGTH') != 0 Then
                    message := 'Current database name is too long (database name length should be less or equal than 30 symbols).';
                Else
                    message := (SQLCODE || ' ' || SQLERRM);
                End if;
        end choose_data;
    
    Function create_new_db(db_name in "Database generation".new_database_name%TYPE)
    Return tableDBGeneration
    Pipelined
    is
        Cursor chosen_data is
            Select *
            From "Database generation"
            Where new_database_name = db_name;
    begin
        For current_element in chosen_data
        Loop
            Pipe row(current_element);
        End loop;
    end create_new_db;  
end db_generation;
/