set serveroutput on

Create or replace Package user_authorization as
    Procedure registration(login in "User".user_login%TYPE, pass in "User".user_password%TYPE, email in "User".user_email%TYPE);
    
    Function log_in(login in "User".user_login%TYPE, pass in "User".user_password%TYPE)
    Return "User".user_login%Type;
End user_authorization;
/
Create or replace Package  body user_authorization as
    Procedure registration(login in "User".user_login%TYPE, pass in "User".user_password%TYPE, email in "User".user_email%TYPE)
    is
    Begin
        INSERT INTO "User"(user_login, role_name_fk, user_password, user_email)
            Values(login, 'Default', pass, email);
        DBMS_OUTPUT.put_line('Registration successful');
        Commit;
    End registration;
    
    Function log_in(login in "User".user_login%TYPE, pass in "User".user_password%TYPE)
    Return "User".user_login%Type
    is
    Begin
        If login = output_for_user.get_user(login).user_login and pass = output_for_user.get_user(login).user_password Then
            DBMS_OUTPUT.put_line('Successfully logged in');
            Return login;
        Else
            DBMS_OUTPUT.put_line('You are not signed on yet. Please, sign on');
            Return Null;
        End if;
    End log_in;
End user_authorization;
/
Create or replace Package output_for_user as
    Type rowExcel is record(
        excel_file_name "Excel file".excel_file_name%TYPE,
        user_login "Excel file".user_login_fk%TYPE,
        excel_file_size "Excel file".excel_file_size%TYPE,
        excel_file_time "Excel file".excel_file_time%TYPE
    );
    
    Type tableExcel is table of rowExcel;
    
    Function get_excel_file(file_name in "Excel file".excel_file_name%TYPE)
        Return tableExcel
        Pipelined;
        
    Function get_excel_file_list
        Return tableExcel
        Pipelined;
        
    Type rowDB is record(
        db_name Database.database_name%TYPE,
        user_login Database.user_login_fk%TYPE,
        db_size Database.database_size%TYPE,
        db_time Database.database_time%TYPE
    );
    
    Type tableDB is table of rowDB;
    
    Function get_db(db_file_name in Database.database_name%TYPE)
        Return rowDB;
        
    Function get_db_list
        Return tableDB
        Pipelined;
        
    Type rowUser is record(
        user_login "User".user_login%TYPE,
        user_role "User".role_name_fk%TYPE,
        user_password "User".user_password%TYPE,
        user_email "User".user_email%TYPE
    );
    
    Type tableUser is table of rowUser;
    
    Function get_user(login in "User".user_login%TYPE)
        Return rowUser;
    
    Function get_user_list
        Return tableUser
        Pipelined;
End output_for_user;
/
Create or replace package body output_for_user as
    Function get_excel_file(file_name in "Excel file".excel_file_name%TYPE)
        return tableExcel
        Pipelined
        is
            is_exist Number(1, 0);
            
            Cursor file_list is
                Select *
                From "Excel file";
        begin
            is_exist := 0;
        
            For current_element in file_list
            Loop
                If file_name = current_element.excel_file_name Then
                    Pipe row(current_element);
                    is_exist := 1;
                    Exit;
                End If;
            End loop;
            
            If is_exist = 0 Then
                DBMS_OUTPUT.put_line('Excel file with current name does not exist');
            End if;
        end get_excel_file;
        
    Function get_excel_file_list
        return tableExcel
        Pipelined
        is
            Cursor file_list is
                Select * 
                from "Excel file";
        begin
            For current_element in file_list
            Loop
                Pipe row(current_element);      
            End loop;
        end get_excel_file_list;
        
    Function get_db(db_file_name in Database.database_name%TYPE)
        return rowDB
        is
            db_info rowDB;
        begin
            Select * into db_info
            from Database
            where database_name = db_file_name;
            
            If db_file_name != db_info.db_name Then
                DBMS_OUTPUT.put_line('\nDatabase with current name does not exist');
                return NULL;
            End if;
            
            return db_info;
        end get_db;
        
    Function get_db_list
        return tableDB
        Pipelined
        is
            Cursor db_list is
                Select * 
                from Database;
        begin
            For current_element in db_list
            Loop
                Pipe row(current_element);
            End loop;
        end get_db_list;
        
    Function get_user(login in "User".user_login%TYPE)
        return rowUser
        is
            user_info rowUser;
        begin
            Select * into user_info
            from "User"
            where user_login = login;
            
            If login != user_info.user_login Then
                DBMS_OUTPUT.put_line('\nUser with current login does not exist');
                return NULL;
            End if;
            
            return user_info;
        end get_user;
        
    Function get_user_list
        return tableUser
        Pipelined
        is
            Cursor user_list is
                Select * 
                from "User";
        begin
            For current_element in user_list
            Loop
                Pipe row(current_element);
            End loop;
        end get_user_list;
end;
/

Create or replace Package work_with_excel_file as
    Type rowRule is record(
        data_address Rule.rule_data_address%TYPE
    );
    
    Type tableRule is table of rowRule;
    
    Procedure add_file(file_name in "Excel file".excel_file_name%TYPE, user_login in "Excel file".user_login_fk%TYPE);
    
    Procedure delete_file(file_name in "Excel file".excel_file_name%TYPE, user_login in "Excel file".user_login_fk%TYPE);
    
    Function update_data(file_name in "Excel file".excel_file_name%TYPE, chosen_cell in Rule.rule_data_address%TYPE, new_data in Rule.rule_data_content%TYPE)
    return STRING;
    
    Function delete_data(file_name in "Excel file".excel_file_name%TYPE, chosen_cell in Rule.rule_data_address%TYPE)
    return STRING;
    
    Function add_data(file_name in "Excel file".excel_file_name%TYPE, cell_address in Rule.rule_data_address%TYPE, cell_content in Rule.rule_data_content%TYPE, cell_type in Rule.rule_data_type%TYPE)
    return STRING;
End work_with_excel_file;
/

Create or replace package body work_with_excel_file as
    Procedure add_file(file_name in "Excel file".excel_file_name%TYPE, user_login in "Excel file".user_login_fk%TYPE) 
        is
        begin
            Insert into "Excel file" (excel_file_name, user_login_fk, excel_file_size, excel_file_time)
                Values (file_name, user_login, 150.0, Sysdate);
            Commit;
        end add_file;
        
    Procedure delete_file(file_name in "Excel file".excel_file_name%TYPE, user_login in "Excel file".user_login_fk%TYPE) 
        is
        begin
            Delete from "Database generation"
                    Where excel_file_name_fk = file_name;
                    
            Delete from Rule
                            Where excel_file_name_fk = file_name;
        
            Delete from "Excel file"
                Where excel_file_name = file_name and user_login_fk = user_login;
            Commit;
        end delete_file;
    
    Function update_data(file_name in "Excel file".excel_file_name%TYPE, chosen_cell in Rule.rule_data_address%TYPE, new_data in Rule.rule_data_content%TYPE)
        return STRING
        is
            message STRING(100);
            
            rule_list rowRule;
            
            Cursor data_list is 
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
                    For cur_data in data_list
                    Loop
                        If cur_data.rule_data_address = chosen_cell Then
                            Update Rule
                            Set rule_data_content = new_data
                            Where excel_file_name_fk = file_name and rule_data_address = chosen_cell;
                            message := 'Updated successfully';
                            Commit;
                            Exit;
                        Else
                            message := 'Current cell is empty';
                        End if;
                    End loop;
                    
                    is_exist := 1;
                    Exit;
                End if;
            End loop;
            
            If is_exist = 0 Then
                message := 'Current excel file does not exist';
            End if;
            
            return message;
        end update_data;
        
    Function delete_data(file_name in "Excel file".excel_file_name%TYPE, chosen_cell in Rule.rule_data_address%TYPE)
        return STRING
        is
            message STRING(100);
            
            rule_list rowRule;
            
            Cursor data_list is 
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
                    For cur_data in data_list
                    Loop
                        If cur_data.rule_data_address = chosen_cell Then
                            Delete from "Database generation"
                            Where excel_file_name_fk = file_name and rule_data_address_fk = chosen_cell;
                        
                            Delete from Rule
                            Where excel_file_name_fk = file_name and rule_data_address = chosen_cell;
                            message := 'Deleted successfully';
                            Commit;
                            Exit;
                        Else
                            message := 'Current cell is already empty';
                        End if;
                    End loop;    
                    
                    is_exist := 1;
                    Exit;
                End if;
            End loop;
            
            If is_exist = 0 Then
                message := 'Current excel file does not exist';
            End if;
            
            return message;
        end delete_data;
        
    Function add_data(file_name in "Excel file".excel_file_name%TYPE, cell_address in Rule.rule_data_address%TYPE, cell_content in Rule.rule_data_content%TYPE, cell_type in Rule.rule_data_type%TYPE)
        return STRING
        is
            message STRING(100);
            
            Cursor rule_list is
                Select rule_data_address 
                From Rule
                Where excel_file_name_fk = file_name;
                
            current_user_login Rule.user_login_fk%TYPE;
            
            is_empty Number(1, 0);
            
            Cursor file_list is
                Select *
                From "Excel file";
                
            is_exist Number(1, 0);
        begin
            is_exist := 0;
            
            For current_element in file_list
            Loop
                If file_name = current_element.excel_file_name Then
                    Select user_login_fk into current_user_login
                    From "Excel file"
                    Where excel_file_name = file_name;
                
                    is_empty := 1;
                    For current_cell in rule_list
                    Loop
                        If cell_address = current_cell.rule_data_address Then
                            is_empty := 0;
                            exit;
                        End if;
                    End loop;
                    
                    If is_empty = 1 Then
                        Insert Into Rule (excel_file_name_fk, user_login_fk, rule_data_address, rule_data_content, rule_data_type)
                            Values(file_name, current_user_login, cell_address, cell_content, cell_type);
                        message := 'Inserted successfully';
                        Commit;
                    Else
                        message := 'Current cell is not empty';
                        Commit;
                    End if;
                            
                    is_exist := 1;
                    Exit;
                End if;
            End loop;
            
            If is_exist = 0 Then
                message := 'Current excel file does not exist';
                Commit;
            End if;
            return message;
        end add_data;
end work_with_excel_file;
/

Create or replace Package work_with_db as
    Procedure add_db(db_name in Database.database_name%TYPE, user_login in Database.user_login_fk%TYPE);
    
    Procedure delete_db(db_name in Database.database_name%TYPE, user_login in Database.user_login_fk%TYPE);
End work_with_db;
/

Create or replace package body work_with_db as
    Procedure add_db(db_name in Database.database_name%TYPE, user_login in Database.user_login_fk%TYPE) 
        is
        begin
            Insert into Database (database_name, user_login_fk, database_size, database_time)
                Values (db_name, user_login, 150.0, Sysdate);
            Commit;
        end add_db;
        
    Procedure delete_db(db_name in Database.database_name%TYPE, user_login in Database.user_login_fk%TYPE) 
        is
        begin
            Delete from "Database generation"
                Where new_database_name = db_name;
        
            Delete from Database
                Where database_name = db_name and user_login_fk = user_login;
            Commit;
        end delete_db;
    end work_with_db;
/    

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
    
    Procedure choose_data(file_name in "Excel file".excel_file_name%TYPE, current_user_login in Rule.user_login_fk%TYPE, cell_address in Rule.rule_data_address%TYPE, db_name in Database.database_name%TYPE);
    
    Function create_new_db(db_name "Database generation".new_database_name%TYPE)
    Return tableDBGeneration
    Pipelined;
End db_generation;
/
Create or replace package body db_generation as
    Procedure choose_data(file_name in "Excel file".excel_file_name%TYPE, current_user_login in Rule.user_login_fk%TYPE, cell_address in Rule.rule_data_address%TYPE, db_name in Database.database_name%TYPE) 
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
                            Values(file_name, current_user_login, cell_address, CURRENT_TIMESTAMP, db_name, '');
                        Commit;
                    Else
                        DBMS_OUTPUT.put_line('Current cell is empty');
                    End if;
                    
                    is_exist := 1;
                    DBMS_OUTPUT.put_line('Database created successfully');
                    Exit;
                End if;
            End loop;
            
            If is_exist = 0 Then
                DBMS_OUTPUT.put_line('Current excel file does not exist');
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
end;
/