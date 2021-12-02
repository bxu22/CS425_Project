import psycopg2
import pandas as pd

def create_server_connection(host_name, database_name, user_name, user_password):
    connection=None
    try:
        connection = psycopg2.connect(
        host=host_name,
        database=database_name,
        user=user_name,
        password=user_password)
        )
        print("Connection to database is successful")
    except Error as err:
        print(f"Error: '{err}'")

#if we need to create another database
# def create_database(connection, query):
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         print("Database created successfully")
#     except Error as err:
#         print(f"Error: '{err}'")

def execute_query(connection, query):
    cursor=connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor=connection.cursor()
    result=None
    try:
        cursor.execute(query)
        result=cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

#QUERIES
#drop table Organ_Donor;
create_Organ_Donor_table="""
create table Organ_Donor (
name VARCHAR(100) not null,
blood_type VARCHAR(100),
age integer,
chronic_diseases VARCHAR(100),
drug_usage boolean,
last_tattoo_date date,
medication_history varchar(100),
last_donation_time date,
phone_or_email VARCHAR(100),
city VARCHAR(100),
state VARCHAR(100),
organ_name VARCHAR(100) not null,
primary key (name, organ_name) ---on delete cascade how?
);
"""
#drop table Blood_Donor;
create_Blood_Donor_table="""
create table Blood_Donor(
name VARCHAR(100) not null,
blood_type VARCHAR(100) not null,
age integer,
chronic_diseases VARCHAR(100),
drug_usage boolean,
last_tattoo_date date,
medication_history varchar(100),
last_donation_time date,
phone_or_email VARCHAR(100),
city VARCHAR(100),
state VARCHAR(100),
primary key (name, blood_type)
);
"""

#drop table Patient;
create_Patient_table="""
create table Patient (
name VARCHAR(100) not null,
blood_type VARCHAR(100),
age integer,
need_organ VARCHAR(100),
need_blood VARCHAR(100),
pays integer,
primary key (name)
);
"""

#drop table organ;
create_Organ_table="""
create table organ(
organ_name VARCHAR(100) not null,
donor_name VARCHAR(100) not null,
recipient VARCHAR(100),
life integer,
availability_date date,
primary key (organ_name, donor_name),
foreign key (organ_name, donor_name) references Organ_donor on delete cascade,
foreign key (recipient) references Patient
);
"""

#drop table Hospital;
create_Hospital_table="""
create table Hospital (
name VARCHAR(100) not null,
city VARCHAR(100),
state VARCHAR(100),
hospitalization_cost integer,
primary key (name)
);
"""

#drop table Doctor;
create_Doctor_table="""
create table Doctor (
name VARCHAR(100) not null,
specialization VARCHAR(100),
fee integer,
primary key (name)
);
"""

#drop table donor_application;
create_Donor_Application_table="""
create table Donor_Application (
donorID integer not null,
blood_type VARCHAR(100),
age integer,
chronic_diseases VARCHAR(100),
drug_usage VARCHAR(100),
last_tattoo_date date,
medication_history VARCHAR(100),
last_donation_time date,
phone_or_email VARCHAR(100),
city VARCHAR(100),
state VARCHAR(100),
primary key (donorID)
);
"""
#drop table works_at;
create_Works_At_table="""
create table works_at (
hospital_name VARCHAR (100) not null,
doctor_name VARCHAR (100) not null,
primary key (doctor_name, hospital_name),
foreign key (doctor_name) references Doctor(name) on delete cascade,
foreign key (hospital_name) references Hospital(name) on delete cascade
);
"""

#drop table patient_need;
create_Patient_Need_table="""
create table patient_need (
patient_ID VARCHAR(100) not null,
organ_name varchar(100),
organ_donorr varchar(100),
blood_type varchar(100),
blood_donorr varchar(100),
primary key (patient_ID),
foreign key (patient_ID) references Patient(name) on delete cascade,
foreign key (organ_donorr, organ_name) references Organ_Donor(name, organ_name) ,
foreign key (blood_donorr, blood_type) references Blood_Donor(name, blood_type)
);
"""

#drop table operates;
create_Operates_table="""
create table operates (
Doctor_name VARCHAR (100) not null,
Patient_name VARCHAR(100) not null,
Primary key (doctor_name, patient_name),
foreign key (doctor_name) references doctor(name) on delete cascade,
foreign key (patient_name) references patient(name) on delete cascade
);
"""

#drop table pays;
create_Pays_table="""
create table pays (
patient_name VARCHAR(100) not null,
hospital_name varchar(100),
primary key (patient_name),
Foreign key (patient_name) references patient(name) on delete cascade,
foreign key (hospital_name) references hospital(name) on delete cascade
);
"""

#drop table in_;
create_In_table="""
create table in_ (
doctor_name VARCHAR(100),
patient_name VARCHAR(100) not null,
hospital_name VARCHAR(100),
primary key (hospital_name),
foreign key (doctor_name) references doctor(name),
foreign key (patient_name) references patient(name),
foreign key (hospital_name) references hospital(name) on delete cascade
);
"""

#drop table applies;
create_Applies_table="""
create table applies (
blood_type VARCHAR(100),
organ_name VARCHAR(100),
donorID integer not null,
hospital_name VARCHAR(100) not null,
Primary key (DonorID, hospital_name),
Foreign key (DonorID) references donor_application(donorID) on delete cascade,
foreign key (hospital_name) references hospital(name) on delete cascade
);
"""

#CHANGE THIS
#drop table Blood_donor_list;
#Should be search
# create_Blood_Donor_List_table="""
# create table Blood_Donor_List (
# ID VARCHAR(100) not null,
# region VARCHAR(100),
# typeAvailability VARCHAR(100),
# age_group INTEGER,
# primary key(ID)
# );
# """

#CHANGE THIS
#drop table organ_donor_list;
#Should be search
# create_Organ_Donor_List_table="""
# create table Organ_Donor_List (
# ID VARCHAR(100) not null,
# organ VARCHAR(100),
# speacialized_doctor VARCHAR(100),
# primary key(ID)
# );
# """

Blood_Match_List="""
SELECT * FROM Blood_Donor
JOIN Patient
ON Blood_Donor.blood_type=Patient.blood_type
"""

Organ_Match_List="""
SELECT * FROM Organ_Donor
JOIN Patient
ON Organ_Donor.blood_type=Patient.blood_type
AND Organ_Donor.organ_name=Patient.need_organ
JOIN Organ ON Organ.recipient=Patient.name
"""

create_Blood_Donor_List_index="""
create index Blood_Donor_List_index on Blood_Donor_List(ID);
"""
create_Organ_Donor_List_index="""
create index Organ_Donor_List_index on Organ_Donor_List(ID);
"""

#CHANGE THIS
#drop table all_donors;
#Should be search
create_All_Donors_table="""
create table all_donors (
blood_donor_ID VARCHAR(100),
organ_donor_ID VARCHAR(100),
foreign key (blood_donor_ID) references Blood_Donor_List,
foreign key (organ_donor_ID) references Organ_Donor_List
);
"""
create_Admin_role="""
CREATE ROLE admin WITH LOGIN ENCRYPTED PASSWORD '123456789';
GRANT ALL PRIVILEDGE on * TO admin;
"""
create_Doctor_User_role="""
CREATE ROLE doctor_user;
GRANT ALL PRIVILEDGE on Patient TO doctor_user;
GRANT ALL PRIVILEDGE on Organ_donor TO doctor_user;
"""
create_Patient_User_role="""
CREATE ROLE patient_user;
GRANT INSERT PRIVILEDGE on Donor_Application TO patient_user;
"""

#create type Blood_Donor_List as table Donor_List [not null];
#create type Organ_Donor_List is table of Donor_List [not null];
#create role doctorUser;
#grant doctorUser TO Patient ;
#grant doctorUser to Organ_donor;

#Program runs here




while(True):
    print("Please login to the database.")
    host_n= input("Enter your host name: ")
    db_n= input("Enter your database name: ")
    user_n=input("Enter your user name: ") #admin, or other users.
    user_p = input("Enter your user password: ")

    try:
        connection = create_server_connection(host_n, db_n, user_n, user_p)
        print("Login successfull")
        #will deal with user types later (maybe in try-excepts)
        while(True):
            print("What do you want to do? \n1: Add data to tables, 2: View tables & lists, 3: View reports, 4: Setup the database (only once) ")
            main_ans = input()

            #add to a table
            if main_ans = 1:
                print("Tables: Donor, Organ")
                table_name = input("Which table do you want to add to: ")
                data_add = input("Enter the data: ")
                if (table_name == "Donor" or table_name=="Organ"):
                    data_add_q="INSERT INTO "+table_name+" VALUES "+data_add
                    try:
                        execute_query(connection, data_add_string)
                        print("added data to table")
                    except Error as err: #wrong data, or user cannot do this action.
                        print(f"Error: '{err}'")
                else:
                    print("Tried to reach a wrong table, go back to main menu")

            #view tables & lists
            elif main_ans = 2: # (!)update queries related to view like blood_donor_list
                view_q="" #this is the query that is going to be run after the if-conditions.
                print("View: Donor, Organ, Patient, Blood_Donor_List, Organ_Donor_List, Donor_Match_List")
                view_name = input("Which view do you want: ")

                if(view_name=="Donor" or view_name=="Organ" or view_name=="Patient"):
                    view_q = "SELECT * FROM "+view_name

                elif(view_name=="Organ_Donor_List"):
                    do_search = input("Do you want to (1) view all or (2) search by sth:")
                    if (do_search==1): #view all table
                        view_q = "SELECT * FROM "+view_name

                    elif (do_search==2): #search by sth
                        search_by = input("Search by region, organ, doctor")
                        search_val = input("Search value: ")
                        #write the query here
                        view_q = "SELECT * FROM Organ_Donor WHERE "+ search_by+"="+search_val

                elif(view_name=="Blood_Donor_List"):
                    do_search = input("Do you want to (1) view all or (2) search by sth:")
                    if (do_search==1): #view all table
                        view_q = "SELECT * FROM "+view_name

                    elif (do_search==2): #search by sth
                        search_by = input("Search by region, blood_type, typeAvailability, age_group")
                        search_val = input("Search value: ")
                        #write the query here
                        view_q = "SELECT * FROM Organ_Donor WHERE "+ search_by+"="+search_val

                elif(view_name=="Donor_Match_List"): #look further into
                    organ_or_blood = input("Do you want to look at (1) Organ matches or (2) Blood matches: ")
                    if(organ_or_blood==1):
                        do_search = input("Do you want to (1) view all or (2) search by organ:")
                        if (do_search==1): #view all table
                            view_q = Organ_Match_List
                        elif (do_search==2):
                            organ_n = input("which organ do you want to search for?: ")
                            view_q = Organ_Match_List+" WHERE Organ_Donor.organ_name="+organ_n

                    elif(organ_or_blood==2):
                        do_search = input("Do you want to (1) view all or (2) search by blood:")
                        if (do_search==1): #view all table
                            view_q = Blood_Match_List
                        elif (do_search==2):
                            blood_type_n = input("which blood type do you want to search for?: ")
                            view_q = Blood_Match_List+" WHERE Blood_Donor.blood_type="+blood_type_n

                #view_q is set according to the request.
                try:
                    results = read_query(connection, view_q)
                    for result in results:
                        print(result)
                except Error as err: #wrong data, or user cannot do this action.
                    print(f"Error: '{err}'")

            #view reports
            elif main_ans = 3:
                pass
            #create the database, should be run only once.
            elif main_ans = 4:
                try:
                    execute_query(connection, create_Organ_Donor_table)
                    execute_query(connection, create_Blood_Donor_table)
                    execute_query(connection, create_Patient_table)
                    execute_query(connection, create_Organ_table)
                    execute_query(connection, create_Hospital_table)
                    execute_query(connection, create_Donor_Application_table)
                    execute_query(connection, create_Works_At_table)
                    execute_query(connection, create_Patient_Need_table)
                    execute_query(connection, create_Organ_table)
                    execute_query(connection, create_Operates_table)
                    execute_query(connection, create_Pays_table)
                    execute_query(connection, create_In_table)
                    execute_query(connection, create_Applies_table)
                    execute_query(connection, create_All_Donors_table)
                    execute_query(connection, create_Admin_role)
                    execute_query(connection, create_Doctor_User_role)
                    execute_query(connection, create_Patient_User_role)
                    #ADD DUMMY DATA TOO
                except Error as err:
                    print(f"Error: '{err}'")
            else:
                print("Invalid request. input 1, 2, 3 or 4.") #return back to question
    except Error as err:
        print(f"Error: '{err}'")
