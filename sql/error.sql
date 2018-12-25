create or replace view excel_file as
    Select *
    From "Excel file";
/

create or replace view databases as
    Select *
    From Database;
/

create or replace view rules as
    Select *
    From Rule;
/

create or replace trigger trg_delete_excel_file
    instead of delete on excel_file
    REFERENCING OLD AS deleted_row
    FOR EACH ROW
    begin
        :deleted_row.deleted := CURRENT_TIMESTAMP;
    END;
/  

create or replace trigger trg_delete_database
    instead of delete on databases
    REFERENCING OLD AS deleted_row
    FOR EACH ROW
    begin
        :deleted_row.deleted := CURRENT_TIMESTAMP;
    END;
/  
  
create or replace trigger trg_delete_rule
    instead of delete on rules
    REFERENCING OLD AS deleted_row
    FOR EACH ROW
    begin
        deleted_row.deleted := CURRENT_TIMESTAMP;
    END;
/  