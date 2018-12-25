INSERT INTO Role (role_name)
    VALUES('Banned');
INSERT INTO Role (role_name)
    VALUES('Admin');
INSERT INTO Role (role_name)
    VALUES('Default');

INSERT INTO "User"(user_login, user_password, role_name_fk, user_email)
    VALUES('EugeneSel', 'anubis123', 'Admin', 'youdjin.sel15@gmail.com');
INSERT INTO "User"(user_login, user_password, role_name_fk, user_email)
    VALUES('JohnElton', 'iamthebest', 'Default', '');
INSERT INTO "User"(user_login, user_password, role_name_fk, user_email)
    VALUES('vadimkakhd', '321sibuna', 'Banned', ''); 
INSERT INTO "User"(user_login, user_password, role_name_fk, user_email)
    VALUES('tamerlan', 'rarestudent10', 'Default', 'okay@gmail.com'); 
INSERT INTO "User"(user_login, user_password, role_name_fk, user_email)
    VALUES('EugeneSel2', 'anubis1234', 'Default', 'youdjin.sel16@gmail.com'); 
    
INSERT INTO "Excel file"(excel_file_name, excel_file_size, excel_file_time, USER_LOGIN_FK)
    VALUES('C:\first', 132.0, TIMESTAMP'2018-11-04 00:12:42', 'EugeneSel'); 
INSERT INTO "Excel file"(excel_file_name, excel_file_size, excel_file_time, USER_LOGIN_FK)
    VALUES('\second', 122.0, TIMESTAMP'2018-11-05 00:12:42', 'JohnElton');  
INSERT INTO "Excel file"(excel_file_name, excel_file_size, excel_file_time, USER_LOGIN_FK)
    VALUES('C:\third', 142.0, TIMESTAMP'2018-11-06 00:12:42', 'tamerlan'); 
INSERT INTO "Excel file"(excel_file_name, excel_file_size, excel_file_time, USER_LOGIN_FK)
    VALUES('\first', 152.0, TIMESTAMP'2018-11-07 00:12:42', 'EugeneSel'); 
    
INSERT INTO Database(database_name, database_size, database_time, USER_LOGIN_FK)
    VALUES('E:\first', 152.0, TIMESTAMP'2018-11-04 00:12:42', 'EugeneSel'); 
INSERT INTO Database(database_name, database_size, database_time, USER_LOGIN_FK)
    VALUES('E:\second', 162.0, TIMESTAMP'2018-11-05 00:12:42', 'JohnElton'); 
INSERT INTO Database(database_name, database_size, database_time, USER_LOGIN_FK)
    VALUES('E:\third', 172.0, TIMESTAMP'2018-11-06 00:12:42', 'vadimkakhd'); 
INSERT INTO Database(database_name, database_size, database_time, USER_LOGIN_FK)
    VALUES('D:\first', 182.0, TIMESTAMP'2018-11-07 00:12:42', 'EugeneSel2'); 

INSERT INTO Rule(excel_file_name_fk, user_login_fk, rule_data_address, rule_data_content, rule_data_type)
    VALUES('C:\third', 'tamerlan', 'B4', '-175', 'Integer');
INSERT INTO Rule(excel_file_name_fk, user_login_fk, rule_data_address, rule_data_content, rule_data_type)
    VALUES('C:\first', 'EugeneSel', 'A1', '123.3','Float');
INSERT INTO Rule(excel_file_name_fk, user_login_fk, rule_data_address, rule_data_content, rule_data_type)
    VALUES('\second', 'JohnElton', 'C13', 'this cell is not empty', 'String');
INSERT INTO Rule(excel_file_name_fk,user_login_fk, rule_data_address, rule_data_content, rule_data_type)
    VALUES('\first', 'EugeneSel', 'E7', 'True', 'Boolean');
    
--INSERT INTO "Database generation"(excel_file_name_fk, user_login_fk, rule_data_address_fk, database_generation_time, new_database_name, database_name_fk)
--    VALUES('C:\first', 'EugeneSel', 'A1', TIMESTAMP'2018-11-04 00:12:42', 'D:\new_first', '');
--INSERT INTO "Database generation"(excel_file_name_fk, user_login_fk, rule_data_address_fk, database_generation_time, new_database_name, database_name_fk)
--    VALUES('\first', 'EugeneSel', 'E7', TIMESTAMP'2018-11-04 00:12:42', 'D:\new_second', '');
--INSERT INTO "Database generation"(excel_file_name_fk, user_login_fk, rule_data_address_fk, database_generation_time, new_database_name, database_name_fk)
--    VALUES('\second', 'JohnElton', 'C13', TIMESTAMP'2018-11-04 00:12:42', 'E:\new_second', '');
--INSERT INTO "Database generation"(excel_file_name_fk, user_login_fk, rule_data_address_fk, database_generation_time, new_database_name, database_name_fk)
--    VALUES('C:\third', 'tamerlan', 'B4', TIMESTAMP'2018-11-04 00:12:42', 'E:\third', 'E:\third');