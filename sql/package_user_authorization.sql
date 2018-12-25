Create or replace Package user_authorization as
    Procedure registration(login in "User".user_login%TYPE, pass in "User".user_password%TYPE, email in "User".user_email%TYPE, message out STRING, user_role in "User".role_name_fk%TYPE default 'Default');
    
    Function log_in(login in "User".user_login%TYPE, pass in "User".user_password%TYPE, message out STRING)
    Return "User".user_login%Type;
End user_authorization;
/

Create or replace Package  body user_authorization as
    Procedure registration(login in "User".user_login%TYPE, pass in "User".user_password%TYPE, email in "User".user_email%TYPE, message out STRING, user_role in "User".role_name_fk%TYPE default 'Default')
    is
    Begin
        
        INSERT INTO "User"(user_login, role_name_fk, user_password, user_email)
            Values(login, user_role, pass, email);
        
        message := 'Operation successful';
        Commit;
    Exception
        When OTHERS Then
            If INSTR(SQLERRM, 'USER_EMAIL_UNIQUE') != 0 Then
                message := 'Current e-mail is already used.';
            Elsif INSTR(SQLERRM, 'USER_PASSWORD_UNIQUE') != 0 Then
                message := 'Current password is already used.';
            Elsif INSTR(SQLERRM, 'USER_LOGIN_CONTENT') != 0 Then
                message := 'You entered a wrong login. Login could consist of latin letters and numbers. Please, repeat entering.';
            Elsif INSTR(SQLERRM, 'USER_PASSWORD_CONTENT') != 0 Then
                message := 'You entered a wrong password. Password could consist of latin letters and numbers. Please, repeat entering.';
            Else
                message := (SQLCODE || ' ' || SQLERRM);
            End if;
    End registration;
    
    Function log_in(login in "User".user_login%TYPE, pass in "User".user_password%TYPE, message out STRING)
    Return "User".user_login%Type
    is
        Cursor user_list is
            Select * 
            From "User";
    Begin
        For current_element in user_list
        Loop
            If current_element.user_login = login Then
                message := 'Successfully logged in';
                Return login;
            Else
                message := 'You are not signed on yet. Please, sign on';
                Return Null;
            End if;
        End loop;
    End log_in;
End user_authorization;
/