Create or replace Package output_for_user as
    Type rowExcel is record(
        excel_file_name "Excel file".excel_file_name%TYPE,
        user_login "Excel file".user_login_fk%TYPE,
        excel_file_size "Excel file".excel_file_size%TYPE,
        excel_file_time "Excel file".excel_file_time%TYPE,
        deleted "Excel file".deleted%TYPE
    );
    
    Type tableExcel is table of rowExcel;
        
    Function get_excel_file_list(user_login in "User".user_login%TYPE, file_name in "Excel file".excel_file_name%TYPE default null)
        Return tableExcel
        Pipelined;
        
    Type rowDB is record(
        db_name Database.database_name%TYPE,
        user_login Database.user_login_fk%TYPE,
        db_size Database.database_size%TYPE,
        db_time Database.database_time%TYPE,
        deleted Database.deleted%TYPE
    );
    
    Type tableDB is table of rowDB;
        
    Function get_db_list(user_login in "User".user_login%TYPE, db_name in Database.database_name%TYPE default null)
        Return tableDB
        Pipelined;
        
    Type rowUser is record(
        user_login "User".user_login%TYPE,
        user_role "User".role_name_fk%TYPE,
        user_password "User".user_password%TYPE,
        user_email "User".user_email%TYPE
    );
    
    Type tableUser is table of rowUser;
    
    Function get_user_list(login in "User".user_login%TYPE default null)
        Return tableUser
        Pipelined;
        
    Type rowRule is record(
        file_name Rule.excel_file_name_fk%TYPE,
        user_login Rule.user_login_fk%TYPE,
        data_address Rule.rule_data_address%TYPE,
        data_content Rule.rule_data_content%TYPE,
        data_type Rule.rule_data_type%TYPE,
        deleted Rule.deleted%TYPE
    );
    
    Type tableRule is table of rowRule;
    
    Function get_rule_list(login in Rule.user_login_fk%TYPE, file_name in Rule.excel_file_name_fk%TYPE default null, cell_address in Rule.rule_data_address%TYPE default null)
        Return tableRule
        Pipelined;
    
    Type rowDBData is record(
        db_time "Database generation".database_generation_time%TYPE,
        new_db_name "Database generation".new_database_name%TYPE,
        file_name "Database generation".excel_file_name_fk%TYPE,
        user_login "Database generation".user_login_fk%TYPE,
        data_address "Database generation".rule_data_address_fk%TYPE,
        db_name "Database generation".database_name_fk%TYPE
    );
    
    Type tableDBData is table of rowDBData;
    
    Function get_DBData_list(login in Rule.user_login_fk%TYPE, db_name in "Database generation".new_database_name%TYPE default null)
        Return tableDBData
        Pipelined;
End output_for_user;
/

Create or replace package body output_for_user as
    Function get_excel_file_list(user_login in "User".user_login%TYPE, file_name in "Excel file".excel_file_name%TYPE default null)
        return tableExcel
        Pipelined
        is
            TYPE file_cursor_type IS REF CURSOR;
            file_list  file_cursor_type;
            
            string_query VARCHAR2(300);
            current_element rowExcel;
        begin
            string_query := 'Select * 
                                from "Excel file"
                                where user_login_fk = trim('''||user_login||''') and deleted is null';
                                
            If file_name is not null Then
                string_query := string_query || ' and trim(excel_file_name) = trim('''||file_name||''')';
            End if;
        
            Open file_list for string_query;
            Loop
                Fetch file_list into current_element;
                Exit when (file_list %NOTFOUND);
                
                Pipe row(current_element);      
            End loop;
        end get_excel_file_list;
        
    Function get_db_list(user_login in "User".user_login%TYPE, db_name in Database.database_name%TYPE default null)
        return tableDB
        Pipelined
        is
            TYPE db_cursor_type IS REF CURSOR;
            db_list  db_cursor_type;
            
            string_query VARCHAR2(300);
            current_element rowDB;
        begin
            string_query := 'Select * 
                                from Database
                                where user_login_fk = trim('''||user_login||''') and deleted is null';
                                
            If db_name is not null Then
                string_query := string_query || ' and trim(database_name) = trim('''||db_name||''')';
            End if;
        
            Open db_list for string_query;
            Loop
                Fetch db_list into current_element;
                Exit when (db_list %NOTFOUND);
                
                Pipe row(current_element);      
            End loop;
        end get_db_list;
        
    Function get_user_list(login in "User".user_login%TYPE default null)
        return tableUser
        Pipelined
        is
            TYPE user_cursor_type IS REF CURSOR;
            user_list  user_cursor_type;
            
            string_query VARCHAR2(300);
            current_element rowUser;
        begin
            string_query := 'Select * 
                                from "User"';
                                
            If login is not null Then
                string_query := string_query || ' where trim(user_login) = trim('''||login||''')';
            End if;
        
            Open user_list for string_query;
            Loop
                Fetch user_list into current_element;
                Exit when (user_list %NOTFOUND);
                
                Pipe row(current_element);      
            End loop;
        end get_user_list;
        
    Function get_rule_list(login in Rule.user_login_fk%TYPE, file_name in Rule.excel_file_name_fk%TYPE default null, cell_address in Rule.rule_data_address%TYPE default null)
        Return tableRule
        Pipelined
        is
            TYPE rule_cursor_type IS REF CURSOR;
            rule_list  rule_cursor_type;
            
            string_query VARCHAR2(300);
            current_element rowRule;
        Begin
            string_query := 'Select * 
                                from Rule
                                where trim(user_login_fk) = trim('''||login||''') and deleted is null';
            
            If file_name is not null Then
                string_query := string_query || ' and trim(excel_file_name_fk) = trim('''||file_name||''')';
                If cell_address is not null Then
                    string_query := string_query || ' and trim(rule_data_address) = trim('''||cell_address||''')';
                End if;
            End if;
        
            Open rule_list for string_query;
            Loop
                Fetch rule_list into current_element;
                Exit when (rule_list %NOTFOUND);
                
                Pipe row(current_element);      
            End loop;
        end get_rule_list;
        
    Function get_DBData_list(login in Rule.user_login_fk%TYPE, db_name in "Database generation".new_database_name%TYPE default null)
        Return tableDBData
        Pipelined
        is
            TYPE data_cursor_type IS REF CURSOR;
            data_list  data_cursor_type;
            
            string_query VARCHAR2(300);
            current_element rowDBData;
        Begin
            string_query := 'Select * 
                                from "Database generation"
                                where trim(user_login_fk) = trim('''||login||''')';
            
            If db_name is not null Then
                string_query := string_query || ' and trim(new_database_name) = trim('''||db_name||''')';
            End if;
        
            Open data_list for string_query;
            Loop
                Fetch data_list into current_element;
                Exit when (data_list %NOTFOUND);
                
                Pipe row(current_element);      
            End loop;
        end get_DBData_list;
end output_for_user;
/