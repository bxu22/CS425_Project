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
name VARCHAR(100) NOT NULL,
blood_type VARCHAR(10) NOT NULL,
age INTEGER,
chronic_diseases VARCHAR(100),
drug_usage BOOLEAN,
last_tattoo_date DATE,
medication_history VARCHAR(100),
last_donation_time DATE,
phone_or_email VARCHAR(100),
city VARCHAR(100),
state VARCHAR(100),
organ_name VARCHAR(100) NOT NULL,
PRIMARY KEY (name, organ_name)
);
"""
#drop table Blood_Donor;
create_Blood_Donor_table="""
create table Blood_Donor (
name VARCHAR(100) NOT NULL,
blood_type VARCHAR(10) NOT NULL,
age INTEGER,
chronic_diseases VARCHAR(100),
drug_usage BOOLEAN,
last_tattoo_date DATE,
medication_history VARCHAR(100),
last_donation_time DATE,
phone_or_email VARCHAR(100),
city VARCHAR(100),
state VARCHAR(100),
PRIMARY KEY (name, blood_type)
);
"""

#drop table Patient;
create_Patient_table="""
create table Patient (
id SERIAL NOT NULL,
name VARCHAR(100) NOT NULL,
blood_type VARCHAR(10) NOT NULL,
age INTEGER,
need_organ VARCHAR(100),
need_blood VARCHAR(10),
pays INTEGER,
PRIMARY KEY (id)
);
"""

#drop table Organ;
create_Organ_table="""
create table Organ (
donor_name VARCHAR(100) NOT NULL,
organ_name VARCHAR(100) NOT NULL,
recipient INTEGER,
life INTEGER,
availability_date DATE,
PRIMARY KEY (donor_name, organ_name),
FOREIGN KEY (donor_name, organ_name) REFERENCES Organ_Donor(name, organ_name) ON DELETE CASCADE,
FOREIGN KEY (recipient) REFERENCES Patient(id)
);
"""

#drop table Hospital;
create_Hospital_table="""
create table Hospital (
id SERIAL NOT NULL,
name VARCHAR(100) NOT NULL,
city VARCHAR(100) NOT NULL,
state VARCHAR(100) NOT NULL,
hospitalization_cost INTEGER,
PRIMARY KEY (id)
);
"""

#drop table Doctor;
create_Doctor_table="""
create table Doctor (
id SERIAL NOT NULL,
name VARCHAR(100) NOT NULL,
specialization VARCHAR(100),
fee INTEGER,
PRIMARY KEY (id)
);
"""

#drop table Donor_Application;
create_Donor_Application_table="""
create table Donor_Application (
id SERIAL NOT NULL,
blood_type VARCHAR(10),
age INTEGER,
chronic_diseases VARCHAR(100),
drug_usage VARCHAR(100),
last_tattoo_date DATE,
medication_history VARCHAR(100),
last_donation_time DATE,
phone_or_email VARCHAR(100),
city VARCHAR(100),
state VARCHAR(100),
PRIMARY KEY (id)
);
"""
#drop table Works_At;
create_Works_At_table="""
create table Works_At (
doctor_id INTEGER NOT NULL,
hospital_id INTEGER NOT NULL,
PRIMARY KEY (doctor_id, hospital_id),
FOREIGN KEY (doctor_id) REFERENCES Doctor(id) ON DELETE CASCADE,
FOREIGN KEY (hospital_id) REFERENCES Hospital(id) ON DELETE CASCADE
);
"""

#drop table Patient_Need;
create_Patient_Need_table="""
create table Patient_Need (
patient_ID INTEGER NOT NULL,    
organ_name VARCHAR(100),
organ_donorr VARCHAR(100),
blood_type VARCHAR(10),
blood_donorr VARCHAR(100),
PRIMARY KEY (patient_ID),
FOREIGN KEY (patient_ID) REFERENCES Patient(id) ON DELETE CASCADE,
FOREIGN KEY (organ_donorr, organ_name) REFERENCES Organ_Donor(name, organ_name),
FOREIGN KEY (blood_donorr, blood_type) REFERENCES Blood_Donor(name, blood_type)
);
"""

#drop table Operates;
create_Operates_table="""
create table Operates (
doctor_id INTEGER NOT NULL,
patient_id INTEGER NOT NULL,
PRIMARY KEY (doctor_id, patient_id),
FOREIGN KEY (doctor_id) REFERENCES Doctor(id) ON DELETE CASCADE,
FOREIGN KEY (patient_id) REFERENCES Patient(id) ON DELETE CASCADE
);
"""

#drop table Pays;
create_Pays_table="""
create table Pays (
patient_id INTEGER NOT NULL,
hospital_id INTEGER NOT NULL,
PRIMARY KEY (patient_id),
FOREIGN KEY (patient_id) REFERENCES Patient(id) ON DELETE CASCADE,
FOREIGN KEY (hospital_id) REFERENCES Hospital(id) ON DELETE CASCADE
);
"""

#drop table In_;
create_In_table="""
create table in_ (
doctor_id INTEGER,
patient_id INTEGER,
hospital_id INTEGER NOT NULL,
PRIMARY KEY (hospital_id),
PRIMARY KEY (doctor_id),
PRIMARY KEY (patient_id),
FOREIGN KEY (patient_id) REFERENCES Patient(id),
FOREIGN KEY (doctor_id) REFERENCES Doctor(id),
FOREIGN KEY (hospital_id) REFERENCES Hospital(id) ON DELETE CASCADE
);
"""

#drop table Applies;
create_Applies_table="""
create table applies (
blood_type VARCHAR(10) NOT NULL,
organ_name VARCHAR(100) NOT NULL,
donor_id INTEGER NOT NULL,
hospital_id INTEGER NOT NULL,
PRIMARY KEY (donor_id, hospital_id),
FOREIGN KEY (donor_id) REFERENCES Donor_Application(id) ON DELETE CASCADE,
FOREIGN KEY (hospital_id) REFERENCES Hospital(id) ON DELETE CASCADE
);
"""

# BEING CHANGED AS QUERIES
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

# BEING CHANGED AS QUERIES
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
blood_donor_id VARCHAR(100),
organ_donor_id VARCHAR(100),
foreign key (blood_donor_id) references Blood_Donor_List(id),
foreign key (organ_donor_id) references Organ_Donor_List(id)
);
"""
create_Admin_role="""
CREATE ROLE admin WITH LOGIN ENCRYPTED PASSWORD '123456789';
GRANT ALL PRIVILEDGE on * TO admin;
"""
create_Doctor_User_role="""
CREATE ROLE doctor_user;
GRANT ALL PRIVILEDGE on Patient TO doctor_user;
GRANT ALL PRIVILEDGE on Organ_Donor TO doctor_user;
"""
create_Patient_User_role="""
CREATE ROLE patient_user;
GRANT INSERT PRIVILEDGE on Donor_Application TO patient_user;
"""

#grant doctorUser TO Patient ;
#grant doctorUser to Organ_donor;

#Program runs here




while(True):
    print('Please login to the database.')
    host_n= input('Enter your host name: ')
    db_n= input('Enter your database name: ')
    user_n=input('Enter your user name: ') #admin, or other users.
    user_p = input('Enter your user password: ')

    try:
        connection = create_server_connection(host_n, db_n, user_n, user_p)
        print('Login successful')
        #will deal with user types later (maybe in try-excepts)
        while(True):
            print('What do you want to do? \n1: Add data to tables, 2: View tables & lists, 3: View reports, 4: Setup the database (only once)')
            main_ans = input()

            #add to a table
            if main_ans == 1:
                print('Tables: Donor, Organ')
                table_name = input('Which table do you want to add to: ')
                data_add = input('Enter the data: ')
                if (table_name == 'Donor' or table_name == 'Organ'):
                    data_add_q = 'INSERT INTO ' + table_name + ' VALUES ' + data_add        # I think this needs to be in two different if statements
                    try:                                                                    # since donor and organ have different attributes, also you have to specify the parameters
                        execute_query(connection, data_add_q)
                        print('added data to table')
                    except Error as err: #wrong data, or user cannot do this action.
                        print(f"Error: '{err}'")
                else:
                    print('Tried to reach a wrong table, go back to main menu')

            #view tables & lists
            elif main_ans == 2: # (!)update queries related to view like blood_donor_list
                view_q = '' #this is the query that is going to be run after the if-conditions.
                print('View: Donor, Organ, Patient, Blood_Donor_List, Organ_Donor_List, Donor_Match_List')
                view_name = input('Which view do you want: ')

                if(view_name == 'Donor' or view_name == 'Organ' or view_name == 'Patient'):
                    view_q = 'SELECT * FROM ' + view_name

                elif(view_name == 'Organ_Donor_List'):
                    do_search = input('Do you want to (1) view all or (2) search by sth:')
                    if (do_search == 1): #view all table
                        view_q = 'SELECT * FROM '+view_name

                    elif (do_search == 2): #search by sth
                        search_by = input('Search by region, organ, doctor')
                        search_val = input('Search value: ')
                        #write the query here
                        view_q = 'SELECT * FROM Organ_Donor WHERE ' + search_by + '=' + search_val

                elif(view_name == 'Blood_Donor_List'):
                    do_search = input('Do you want to (1) view all or (2) search by sth:')
                    if (do_search == 1): #view all table
                        view_q = 'SELECT * FROM ' + view_name

                    elif (do_search == 2): #search by sth
                        search_by = input('Search by region, blood_type, typeAvailability, age_group')
                        search_val = input('Search value: ')
                        #write the query here
                        view_q = 'SELECT * FROM Organ_Donor WHERE ' + search_by + '=' + search_val

                elif(view_name == 'Donor_Match_List'): #look further into
                    organ_or_blood = input('Do you want to look at (1) Organ matches or (2) Blood matches: ')
                    if(organ_or_blood == 1):
                        do_search = input('Do you want to (1) view all or (2) search by organ:')
                        if (do_search == 1): #view all table
                            view_q = Organ_Match_List
                        elif (do_search == 2):
                            organ_n = input('Which organ do you want to search for?: ')
                            view_q = Organ_Match_List + ' WHERE Organ_Donor.organ_name=' + organ_n

                    elif(organ_or_blood == 2):
                        do_search = input('Do you want to (1) view all or (2) search by blood:')
                        if (do_search == 1): #view all table
                            view_q = Blood_Match_List
                        elif (do_search == 2):
                            blood_type_n = input('Which blood type do you want to search for?: ')
                            view_q = Blood_Match_List + ' WHERE Blood_Donor.blood_type=' + blood_type_n

                #view_q is set according to the request.
                try:
                    results = read_query(connection, view_q)
                    for result in results:
                        print(result)
                except Error as err: #wrong data, or user cannot do this action.
                    print(f"Error: '{err}'")

            #view reports
            elif main_ans == 3:
                pass
            #create the database, should be run only once.
            elif main_ans == 4:
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
                print('Invalid request. input 1, 2, 3 or 4.') #return back to question
    except Error as err:
        print(f"Error: '{err}'")
