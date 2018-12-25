Create or replace package work_with_user as
    Procedure delete_user(login in "User".user_login%TYPE);
    
    Procedure change_user_role(login in "User".user_login%TYPE);
end work_with_user;
/

Create or replace package body work_with_user as    
    Procedure delete_user(login in "User".user_login%TYPE)
    is
    Begin
        Delete from Database
            Where user_login_fk = login;
            
        Delete from "Database generation"
            Where user_login_fk = login;  
            
        Delete from Rule
            Where user_login_fk = login;  
    
        Delete from "Excel file"
            Where user_login_fk = login;
            
        Delete from "User"
            Where user_login = login;  
        Commit;
    end delete_user;
    
    Procedure change_user_role(login in "User".user_login%TYPE)
    is
        current_role "User".role_name_fk%TYPE;
    Begin
        Select user_role into current_role
        From table(output_for_user.get_user_list(login));
        
        If current_role = 'Banned' Then
            Update "User"
                Set role_name_fk = 'Default'
                Where user_login = login;
            Commit;
        Else
            Update "User"
                Set role_name_fk = 'Banned'
                Where user_login = login;
            Commit;
        End if;
    end change_user_role;
end work_with_user;
/