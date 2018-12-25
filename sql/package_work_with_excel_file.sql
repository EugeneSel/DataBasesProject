Create or replace Package work_with_excel_file as
    Type rowRule is record(
        data_address Rule.rule_data_address%TYPE
    );
    
    Type tableRule is table of rowRule;
    
    Procedure add_file(file_name in "Excel file".excel_file_name%TYPE, user_login in "Excel file".user_login_fk%TYPE, message out STRING);
    
    Procedure delete_file(file_name in "Excel file".excel_file_name%TYPE, user_login in "Excel file".user_login_fk%TYPE);
    
    Function update_data(file_name in "Excel file".excel_file_name%TYPE, chosen_cell in Rule.rule_data_address%TYPE, new_data in Rule.rule_data_content%TYPE, new_data_type in Rule.rule_data_type%TYPE)
    return STRING;
    
    Function delete_data(file_name in "Excel file".excel_file_name%TYPE, chosen_cell in Rule.rule_data_address%TYPE)
    return STRING;
    
    Function add_data(file_name in "Excel file".excel_file_name%TYPE, cell_address in Rule.rule_data_address%TYPE, cell_content in Rule.rule_data_content%TYPE, cell_type in Rule.rule_data_type%TYPE)
    return STRING;
End work_with_excel_file;
/

Create or replace package body work_with_excel_file as
    Procedure add_file(file_name in "Excel file".excel_file_name%TYPE, user_login in "Excel file".user_login_fk%TYPE, message out STRING) 
        is
            is_exist INTEGER :=0;
        Begin
            Select count(*) into is_exist
            From "Excel file"
            Where excel_file_name = file_name;
            
            If is_exist = 0 Then
                Insert into "Excel file" (excel_file_name, user_login_fk, excel_file_size, excel_file_time)
                    Values (file_name, user_login, 150.0, current_timestamp);
            Else
                Update "Excel file"
                    Set deleted = null, excel_file_time = current_timestamp
                    Where excel_file_name = file_name and user_login_fk = user_login;
            End if;
            
            Commit;
            message := 'File '||file_name||' successfully created.';
        Exception
            When OTHERS Then
                If INSTR(SQLERRM, 'EXCEL_FILE_NAME_CONTENT') != 0 Then
                    message := 'You entered invalid file path.';
                Elsif INSTR(SQLERRM, 'EXCEL_FILE_NAME_LENGTH') != 0 Then
                    message := 'Current file name is too long (file name length should be less or equal than 30 symbols).';
                Else
                    message := (SQLCODE || ' ' || SQLERRM);
                End if;
        end add_file;
        
    Procedure delete_file(file_name in "Excel file".excel_file_name%TYPE, user_login in "Excel file".user_login_fk%TYPE) 
        is
        begin   
            Update "Excel file"
                Set deleted = current_timestamp
                Where excel_file_name = file_name and user_login_fk = user_login;
            Commit;
        end delete_file;
    
    Function update_data(file_name in "Excel file".excel_file_name%TYPE, chosen_cell in Rule.rule_data_address%TYPE, new_data in Rule.rule_data_content%TYPE, new_data_type in Rule.rule_data_type%TYPE)
        return STRING
        is
            message STRING(200);
            
            rule_list rowRule;
            
            Cursor data_list is 
                Select *
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
                        If cur_data.rule_data_address = chosen_cell and cur_data.deleted is null Then
                            Update Rule
                                Set rule_data_content = new_data, rule_data_type = new_data_type
                                Where excel_file_name_fk = file_name and rule_data_address = chosen_cell;
                                
                            message := 'Updated '||chosen_cell||' successfully';
                            Commit;
                            Exit;
                        Else
                            message := 'Current cell '||chosen_cell||' is empty';
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
        Exception 
            When OTHERS Then
                If INSTR(SQLERRM, 'RULE_DATA_ADDRESS_CONTENT') != 0 Then
                    return 'You entered invalid cell address.';
                Elsif INSTR(SQLERRM, 'RULE_DATA_ADDRESS_LENGTH') != 0 Then
                    return 'Current cell address is too long (cell address length should be more or equal than 2 symbols and less or equal than 8 symbols).';
                Elsif INSTR(SQLERRM, 'RULE_DATA_CONTENT_LENGTH') != 0 Then
                    return 'Current data is too long (data length should be less or equal than 50 symbols).';                    
                Else
                    return SQLCODE || ' ' || SQLERRM;
                End if;
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
                            Update Rule
                                Set deleted = current_timestamp
                                Where excel_file_name_fk = file_name and rule_data_address = chosen_cell;
                                
                            message := 'Deleted '||chosen_cell||' successfully';
                            Commit;
                            Exit;
                        Else
                            message := 'Current cell '||chosen_cell||' is already empty';
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
                Select * 
                From Rule
                Where excel_file_name_fk = file_name;
                
            current_user_login Rule.user_login_fk%TYPE;
            
            is_empty Number(1, 0);
            
            Cursor file_list is
                Select *
                From "Excel file";
                
            is_exist Number(1, 0);
            
            is_deleted INTEGER := 0;
        begin
            is_exist := 0;
            
            Select count(*) into is_deleted
            From Rule
            Where excel_file_name_fk = file_name and rule_data_address = cell_address;
            
            For current_element in file_list
            Loop
                If file_name = current_element.excel_file_name Then
                    Select user_login_fk into current_user_login
                    From "Excel file"
                    Where excel_file_name = file_name;
                
                    is_empty := 1;
                    For current_cell in rule_list
                    Loop
                        If cell_address = current_cell.rule_data_address and current_cell.deleted is null Then
                            is_empty := 0;
                            exit;
                        End if;
                    End loop;
                    
                    If is_empty = 1 Then
                        If is_deleted = 0 Then
                            Insert Into Rule (excel_file_name_fk, user_login_fk, rule_data_address, rule_data_content, rule_data_type)
                                Values(file_name, current_user_login, cell_address, cell_content, cell_type);
                        Else
                            Update Rule
                            Set deleted = null, rule_data_content = cell_content, rule_data_type = cell_type
                            Where excel_file_name_fk = file_name and rule_data_address = cell_address;
                        End if;
                            
                        message := 'Inserted '||cell_address||' successfully';
                        Commit;
                    Else
                        message := 'Current cell '||cell_address||' is not empty';
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
        Exception 
            When OTHERS Then
                If INSTR(SQLERRM, 'RULE_DATA_ADDRESS_CONTENT') != 0 Then
                    return 'You entered invalid cell address.';
                Elsif INSTR(SQLERRM, 'RULE_DATA_ADDRESS_LENGTH') != 0 Then
                    return 'Current cell address is too long (cell address length should be more or equal than 2 symbols and less or equal than 8 symbols).';
                Elsif INSTR(SQLERRM, 'RULE_DATA_CONTENT_LENGTH') != 0 Then
                    return 'Current data is too long (data length should be less or equal than 50 symbols).';                    
                Else
                    return SQLCODE || ' ' || SQLERRM;
                End if;
        end add_data;
end work_with_excel_file;
/