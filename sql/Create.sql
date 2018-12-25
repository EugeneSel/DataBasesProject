/*==============================================================*/
/* DBMS name:      ORACLE Version 11g                           */
/* Created on:     18.11.2018 20:29:27                          */
/*==============================================================*/


alter table Database
   drop constraint FK_DATABASE_USER;

alter table "Database generation"
   drop constraint FK_DB_GENERATION_DB;

alter table "Database generation"
   drop constraint FK_DB_GENERATION_RULE;

alter table "Excel file"
   drop constraint FK_EXCEL_FILE_USER;

alter table Rule
   drop constraint FK_RULE_EXCEL_FILE;

alter table "User"
   drop constraint FK_USER_ROLE;

drop index "User works with Database_FK";

drop table Database cascade constraints;

drop index "Generated Database_FK";

drop index "Rule of Data Transfer_FK";

drop table "Database generation" cascade constraints;

drop index "User works with Excel file_FK";

drop table "Excel file" cascade constraints;

drop table Role cascade constraints;

drop index "Excel file data Rule_FK";

drop table Rule cascade constraints;

drop index "User has Role_FK";

drop table "User" cascade constraints;

/*==============================================================*/
/* Table: Database                                              */
/*==============================================================*/
create table Database 
(
   database_name        VARCHAR2(200)        not null,
   user_login_fk        VARCHAR2(30)         not null,
   database_size        INTEGER              not null,
   database_time        DATE                 not null,
   deleted              DATE,
   constraint PK_DATABASE primary key (database_name)
);

/*==============================================================*/
/* Index: "User works with Database_FK"                         */
/*==============================================================*/
create index "User works with Database_FK" on Database (
   user_login_fk ASC
);

/*==============================================================*/
/* Table: "Database generation"                                 */
/*==============================================================*/
create table "Database generation" 
(
   database_generation_time DATE                 not null,
   new_database_name    VARCHAR2(200)        not null,
   excel_file_name_fk   VARCHAR2(200),
   user_login_fk        VARCHAR2(30)         not null,
   rule_data_address_fk VARCHAR2(50),
   database_name_fk     VARCHAR2(200),
   constraint "PK_DATABASE GENERATION" primary key (database_generation_time, new_database_name, excel_file_name_fk, user_login_fk, rule_data_address_fk)
);

/*==============================================================*/
/* Index: "Rule of Data Transfer_FK"                            */
/*==============================================================*/
create index "Rule of Data Transfer_FK" on "Database generation" (
   excel_file_name_fk ASC,
   user_login_fk ASC,
   rule_data_address_fk ASC
);

/*==============================================================*/
/* Index: "Generated Database_FK"                               */
/*==============================================================*/
create index "Generated Database_FK" on "Database generation" (
   database_name_fk ASC
);

/*==============================================================*/
/* Table: "Excel file"                                          */
/*==============================================================*/
create table "Excel file" 
(
   excel_file_name      VARCHAR2(200)        not null,
   user_login_fk        VARCHAR2(30)         not null,
   excel_file_size      INTEGER              not null,
   excel_file_time      DATE                 not null,
   deleted              DATE,
   constraint "PK_EXCEL FILE" primary key (excel_file_name, user_login_fk)
);

/*==============================================================*/
/* Index: "User works with Excel file_FK"                       */
/*==============================================================*/
create index "User works with Excel file_FK" on "Excel file" (
   user_login_fk ASC
);

/*==============================================================*/
/* Table: Role                                                  */
/*==============================================================*/
create table Role 
(
   role_name            VARCHAR2(30)         not null,
   constraint PK_ROLE primary key (role_name)
);

/*==============================================================*/
/* Table: Rule                                                  */
/*==============================================================*/
create table Rule 
(
   excel_file_name_fk   VARCHAR2(200),
   user_login_fk        VARCHAR2(30)         not null,
   rule_data_address    VARCHAR2(50)         not null,
   rule_data_content    VARCHAR2(1000),
   rule_data_type       VARCHAR2(30)         not null,
   deleted              DATE,
   constraint PK_RULE primary key (excel_file_name_fk, user_login_fk, rule_data_address)
);

/*==============================================================*/
/* Index: "Excel file data Rule_FK"                             */
/*==============================================================*/
create index "Excel file data Rule_FK" on Rule (
   excel_file_name_fk ASC,
   user_login_fk ASC
);

/*==============================================================*/
/* Table: "User"                                                */
/*==============================================================*/
create table "User" 
(
   user_login           VARCHAR2(30)         not null,
   role_name_fk         VARCHAR2(30)         not null,
   user_password        VARCHAR2(30)         not null,
   user_email           VARCHAR2(30),
   constraint PK_USER primary key (user_login)
);

/*==============================================================*/
/* Index: "User has Role_FK"                                    */
/*==============================================================*/
create index "User has Role_FK" on "User" (
   role_name_fk ASC
);

alter table Database
   add constraint FK_DATABASE_USER foreign key (user_login_fk)
      references "User" (user_login);

alter table "Database generation"
   add constraint FK_DB_GENERATION_DB foreign key (database_name_fk)
      references Database (database_name);

alter table "Database generation"
   add constraint FK_DB_GENERATION_RULE foreign key (excel_file_name_fk, user_login_fk, rule_data_address_fk)
      references Rule (excel_file_name_fk, user_login_fk, rule_data_address);

alter table "Excel file"
   add constraint FK_EXCEL_FILE_USER foreign key (user_login_fk)
      references "User" (user_login);

alter table Rule
   add constraint FK_RULE_EXCEL_FILE foreign key (excel_file_name_fk, user_login_fk)
      references "Excel file" (excel_file_name, user_login_fk);

alter table "User"
   add constraint FK_USER_ROLE foreign key (role_name_fk)
      references Role (role_name);

alter table "User"
    add constraint user_password_unique unique (user_password);
    
alter table "User"
    add constraint user_password_length check (length(user_password) >= 8);
    
alter table "User"
    add constraint user_email_unique UNIQUE (user_email);
    
alter table "Excel file"
    add constraint excel_file_size_positive check (excel_file_size >= 0);
    
alter table Database
    add constraint database_size_positive check (database_size >= 0);
    
alter table "User"
    add constraint user_login_length check (length(user_login) >= 4);

alter table "User"
    add constraint user_login_content check (Regexp_like(user_login, '[A-Za-z0-9_]'));
    
alter table "User"
    add constraint user_password_content check (Regexp_like(user_password, '[A-Za-z0-9]'));
    
alter table "User"
    add constraint user_email_content check (Regexp_like(user_email, '[a-z0-9.@]'));
    
alter table Role
    add constraint role_name_values check (role_name in ('Banned', 'Admin', 'Default'));
    
alter table Rule
    add constraint data_type_values check (rule_data_type in ('Integer', 'Float', 'Boolean', 'Date', 'Time', 'String'));
    
alter table "Excel file"
    add constraint excel_file_name_content check (Regexp_like(excel_file_name, '([A-Za-z]:\\|\\){1}([A-Za-z0-9-_]{1,}\\|[A-Za-z0-9-_]{1,}){1,}'));
    
alter table "Excel file"
    add constraint excel_file_name_length check (length(excel_file_name) <= 30);
    
alter table Database
    add constraint database_name_content check (Regexp_like(database_name, '([A-Za-z]:\\|\\){1}([A-Za-z0-9-_]{1,}\\|[A-Za-z0-9-_]{1,}){1,}'));
    
alter table Database
    add constraint database_name_length check (length(database_name) <= 30);
    
alter table "Database generation"
    add constraint new_database_name_content check (Regexp_like(new_database_name, '([A-Za-z]:\\|\\){1}([A-Za-z0-9-_]{1,}\\|[A-Za-z0-9-_]{1,}){1,}'));
    
alter table "Database generation"
    add constraint new_database_name_length check (length(new_database_name) <= 30);
    
alter table Rule
    add constraint rule_data_address_content check (Regexp_like(rule_data_address, '[A-Z]{1,4}[0-9]{1,4}'));
    
alter table Rule
    add constraint rule_data_address_length check (length(rule_data_address) >= 2 and length(rule_data_address) <= 8);
    
alter table Rule
    add constraint rule_data_content_length check (length(rule_data_content) <= 50);