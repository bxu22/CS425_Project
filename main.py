# Authors:
# Ali Guzelyel
# Brian Xu

import psycopg2

def read_query(connection, query):
    cursor=connection.cursor()
    result=None
    try:
        cursor.execute(query)
        result=cursor.fetchall()
        return result
    except:
        print('Error')

# QUERIES
create_Organ_Donor_table = '''
CREATE TABLE Organ_Donor (
name VARCHAR(100) NOT NULL,
blood_type VARCHAR(10) NOT NULL,
age INTEGER,
chronic_diseases VARCHAR(100),
drug_usage BOOLEAN,
last_tattoo_date DATE,
medication_history VARCHAR(100),
last_donation_time DATE NOT NULL,
phone_or_email VARCHAR(100),
region VARCHAR(100),
organ_name VARCHAR(100) NOT NULL,
PRIMARY KEY (name, organ_name)
);
'''

create_Blood_Donor_table = '''
CREATE TABLE Blood_Donor (
name VARCHAR(100) NOT NULL,
blood_type VARCHAR(10) NOT NULL,
age INTEGER,
chronic_diseases VARCHAR(100),
drug_usage BOOLEAN,
last_tattoo_date DATE,
medication_history VARCHAR(100),
last_donation_time DATE NOT NULL,
phone_or_email VARCHAR(100),
region VARCHAR(100) NOT NULL,
PRIMARY KEY (name, blood_type)
);
'''

create_Patient_table = '''
CREATE TABLE Patient (
id SERIAL NOT NULL,
name VARCHAR(100) NOT NULL,
blood_type VARCHAR(10) NOT NULL,
age INTEGER,
need_organ VARCHAR(100),
need_blood VARCHAR(10),
pays INTEGER,
PRIMARY KEY (id)
);
'''

create_Organ_table = '''
CREATE TABLE Organ (
donor_name VARCHAR(100) NOT NULL,
organ_name VARCHAR(100) NOT NULL,
recipient INTEGER,
life INTEGER,
availability_date DATE,
PRIMARY KEY (donor_name, organ_name),
FOREIGN KEY (donor_name, organ_name) REFERENCES Organ_Donor(name, organ_name) ON DELETE CASCADE,
FOREIGN KEY (recipient) REFERENCES Patient(id)
);
'''

create_Hospital_table = '''
CREATE TABLE Hospital (
id SERIAL NOT NULL,
name VARCHAR(100) NOT NULL,
region VARCHAR(100) NOT NULL,
hospitalization_cost INTEGER,
PRIMARY KEY (id)
);
'''

create_Doctor_table = '''
CREATE TABLE Doctor (
id SERIAL NOT NULL,
name VARCHAR(100) NOT NULL,
specialization VARCHAR(100),
fee INTEGER,
number_of_operations INTEGER DEFAULT 0,
PRIMARY KEY (id)
);
'''

create_Donor_Application_table = '''
CREATE TABLE Donor_Application (
id SERIAL NOT NULL,
blood_type VARCHAR(10),
age INTEGER,
chronic_diseases VARCHAR(100),
drug_usage VARCHAR(100),
last_tattoo_date DATE,
medication_history VARCHAR(100),
last_donation_time DATE NOT NULL,
phone_or_email VARCHAR(100),
region VARCHAR(100),
PRIMARY KEY (id)
);
'''

create_Works_At_table = '''
CREATE TABLE Works_At (
doctor_id INTEGER NOT NULL,
hospital_id INTEGER NOT NULL,
PRIMARY KEY (doctor_id, hospital_id),
FOREIGN KEY (doctor_id) REFERENCES Doctor(id) ON DELETE CASCADE,
FOREIGN KEY (hospital_id) REFERENCES Hospital(id) ON DELETE CASCADE
);
'''

create_Operates_table = '''
CREATE TABLE Operates (
doctor_id INTEGER NOT NULL,
patient_id INTEGER NOT NULL,
PRIMARY KEY (doctor_id, patient_id),
FOREIGN KEY (doctor_id) REFERENCES Doctor(id) ON DELETE CASCADE,
FOREIGN KEY (patient_id) REFERENCES Patient(id) ON DELETE CASCADE
);
'''

create_Applies_table = '''
CREATE TABLE applies (
blood_type VARCHAR(10) NOT NULL,
organ_name VARCHAR(100) NOT NULL,
donor_id INTEGER NOT NULL,
hospital_id INTEGER NOT NULL,
PRIMARY KEY (donor_id, hospital_id),
FOREIGN KEY (donor_id) REFERENCES Donor_Application(id) ON DELETE CASCADE,
FOREIGN KEY (hospital_id) REFERENCES Hospital(id) ON DELETE CASCADE
);
'''

Donor_Organ_Match_List = '''
SELECT * FROM Organ_Donor
JOIN Patient
ON Organ_Donor.blood_type=Patient.blood_type
AND Organ_Donor.organ_name=Patient.need_organ;
'''

Donor_Blood_Match_List = '''
SELECT * FROM Blood_Donor
JOIN Patient
ON Blood_Donor.blood_type=Patient.blood_type
OR (SELECT blood_type FROM Organ_Donor WHERE blood_type='O')=Patient.blood
OR Organ_Donor.blood_type=(SELECT blood_type FROM Patient WHERE blood_type='AB')
'''

Income_Report = '''
SELECT SUM(fee)
FROM Doctor
'''

Operations_Report = '''
SELECT COUNT(number_of_operations), region, name
FROM Doctor 
GROUP BY region
ORDER BY COUNT(number_of_operations) DESC;
'''

create_Blood_Donor_index = '''
CREATE INDEX Blood_Donor_index ON Blood_Donor(blood_type);
'''

create_Organ_Donor_index = '''
CREATE INDEX Organ_Donor_index ON Organ(organ_name);
'''

create_Hospital_Region_index = '''
CREATE INDEX Hospital_Region_index ON Hospital(region);
'''

create_Doctor_Specialization_index = '''
CREATE INDEX Doctor_Specialization_index ON Doctor(specialization);
'''

create_Admin_role = '''
CREATE ROLE admin LOGIN SUPERUSER;
GRANT ALL PRIVILEGES ON TABLE Organ_Donor TO admin;
GRANT ALL PRIVILEGES ON TABLE Blood_Donor TO admin;
GRANT ALL PRIVILEGES ON TABLE Patient TO admin;
GRANT ALL PRIVILEGES ON TABLE Organ TO admin;
GRANT ALL PRIVILEGES ON TABLE Hospital TO admin;
GRANT ALL PRIVILEGES ON TABLE Doctor TO admin;
GRANT ALL PRIVILEGES ON TABLE Donor_Application TO admin;
GRANT ALL PRIVILEGES ON TABLE Works_At TO admin;
GRANT ALL PRIVILEGES ON TABLE Operates TO admin;
GRANT ALL PRIVILEGES ON TABLE Applies TO admin;
GRANT ALL PRIVILEGES ON SEQUENCE doctor_id_seq TO admin;
GRANT ALL PRIVILEGES ON SEQUENCE donor_application_id_seq TO admin;
GRANT ALL PRIVILEGES ON SEQUENCE hospital_id_seq TO admin;
GRANT ALL PRIVILEGES ON SEQUENCE patient_id_seq TO admin;
'''

create_Doctor_User_role = '''
CREATE ROLE doctor_user LOGIN NOINHERIT;
GRANT ALL PRIVILEGES ON TABLE Patient TO doctor_user;
GRANT ALL PRIVILEGES ON TABLE Organ_Donor TO doctor_user;
'''

create_Patient_User_role = '''
CREATE ROLE patient_user LOGIN NOINHERIT;
GRANT ALL PRIVILEGES ON TABLE Patient TO patient_user;
'''

# Drop Tables
drop_Organ_Donor_table = '''
DROP TABLE Organ_Donor CASCADE;
'''

drop_Blood_Donor_table = '''
DROP TABLE Blood_Donor CASCADE;
'''

drop_Patient_table = '''
DROP TABLE Patient CASCADE;
'''

drop_Organ_table = '''
DROP TABLE Organ CASCADE;
'''

drop_Hospital_table = '''
DROP TABLE Hospital CASCADE;
'''

drop_Doctor_table = '''
DROP TABLE Doctor CASCADE;
'''

drop_Donor_Application = '''
DROP TABLE Donor_Application CASCADE;
'''

drop_Works_At = '''
DROP TABLE Works_At CASCADE;
'''

drop_Operates_table = '''
DROP TABLE Operates CASCADE;
'''

drop_Applies_table = '''
DROP TABLE applies CASCADE;
'''

drop_Admin_role = '''
DROP ROLE IF EXISTS admin;
'''

drop_Doctor_User_role = '''
DROP ROLE IF EXISTS doctor_user;
'''

drop_Patient_User_role = '''
DROP ROLE IF EXISTS patient_user;
'''

# Program runs here
while(True):
    # print('Please login to the database. Recommended to login as postgres to setup database.')
    # host_n = input('Enter your host name: ')
    # db_n = input('Enter your database name: ')
    # user_n = input('Enter your user name: ')
    # user_p = input('Enter your user password: ')

    try:
        connection = psycopg2.connect(host = 'localhost', database = 'postgres', user = 'postgres', password = '1234', port = '5432') # Comment this line after you are done with postgres(admin) setting up database
        # connection = psycopg2.connect(host = host_n, database = db_n, user = user_n, password = user_p, port = '5432') # Uncomment this line and the lines above for different user login
        print('Login successful as ')# + user_n)
        cursor = connection.cursor()
        while(True):
            print('What do you want to do?\n1: Add data to tables\n2: View lists & reports\n3: Setup database/create roles (only once)\n4: Drop database/roles (only after database was created)\n5: Create user\n6: Grant\Revoke role to user (Postgres Admin only)\n7: Exit')
            main_ans = input('Input: ')

            #add to a table
            if main_ans == '1':
                print('Tables:\n1: Blood_Donor\n2: Organ_Donor\n3: Organ\n4: Patient\n5: Doctor\n6: Hospital')
                table_name = input('Which table do you want to add to: ')
                if table_name == '1': # Blood Donor
                    name = input('Name (String): ')
                    blood_type = input('Blood Type (String): ')
                    age = input('Age (Integer): ')
                    chronic_diseases = input('Chronic Diseases (String): ')
                    drug_usage = input('On any drugs (Boolean): ')
                    last_tattoo_date = input('Last Tattoo Date (YYYY-MM-DD): ')
                    medication_history = input('Medication History (String): ')
                    last_donation_time = input('Last Donation Date (YYYY-MM-DD): ')
                    phone_or_email = input('Provide Phone or Email Address (String): ')
                    region = input('Region (City, State) (String): ')
                    data = (name, blood_type, age, chronic_diseases, drug_usage, last_tattoo_date, medication_history, last_donation_time, phone_or_email, region)
                    data_add_q = 'INSERT INTO blood_donor (name, blood_type, age, chronic_diseases, drug_usage, last_tattoo_date, medication_history, last_donation_time, phone_or_email, region) VALUES (' + ', '.join(data) + ')'
                    cursor.execute(data_add_q)
                    connection.commit()
                    connection.close()
                    print('Data has been added')
                    break

                elif table_name == '2': # Organ Donor
                    name = input('Name (String): ')
                    blood_type = input('Blood Type (String): ')
                    age = input('Age (Integer): ')
                    chronic_diseases = input('Chronic Diseases (String): ')
                    drug_usage = input('On any drugs (Boolean): ')
                    last_tattoo_date = input('Last Tattoo Date (YYYY-MM-DD): ')
                    medication_history = input('Medication History (String): ')
                    last_donation_time = input('Last Donation Date (YYYY-MM-DD): ')
                    phone_or_email = input('Provide Phone or Email Address (String): ')
                    region = input('Region (City, State) (String): ')
                    organ_name = input('Organ Name (String): ')
                    data = (name, blood_type, age, chronic_diseases, drug_usage, last_tattoo_date, medication_history, last_donation_time, phone_or_email, region, organ_name)
                    data_add_q = 'INSERT INTO organ_donor (name, blood_type, age, chronic_diseases, drug_usage, last_tattoo_date, medication_history, last_donation_time, phone_or_email, region, organ_name) VALUES (' + ', '.join(data) + ')'
                    cursor.execute(data_add_q)
                    connection.commit()
                    connection.close()
                    print('Data has been added')
                    break

                elif table_name == '3': # Organ
                    donor_name = input('Donor Name (String): ')
                    organ_name = input('Organ Name (String): ')
                    life = input('Life number of days (Integer): ')
                    availability_date = input('Available Date (Date): ')
                    data = (donor_name, organ_name, life, availability_date)
                    data_add_q = 'INSERT INTO organ (donor_name, organ_name, life, availability_date) VALUES (' + ', '.join(data) + ')'
                    cursor.execute(data_add_q)
                    connection.commit()
                    connection.close()
                    print('Data has been added')
                    break

                elif table_name == '4': # Patient
                    name = input('Name (String): ')
                    blood_type = input('Blood Type (String): ')
                    age = input('Age (Integer): ')
                    need_organ = input('Need Organ (String): ')
                    need_blood = input('Need Blood (String): ')
                    pays = input('Payment cost (Integer): ')
                    data = (name, blood_type, age, need_organ, need_blood, pays)
                    data_add_q = 'INSERT INTO patient (name, blood_type, age, need_organ, need_blood, pays) VALUES (' + ', '.join(data) + ')'
                    cursor.execute(data_add_q)
                    connection.commit()
                    connection.close()
                    print('Data has been added')
                    break

                elif table_name == '5': # Doctor
                    name = input('Name (String): ')
                    specialization = input('Specialization (String): ')
                    fee = input('Fee (Integer): ')
                    number_of_operations = input('Number of Operations (Integer): ')
                    data = (name, specialization, fee, number_of_operations)
                    data_add_q = 'INSERT INTO doctor (name, specialization, fee, number_of_operations) VALUES (' + ', '.join(data) + ')'
                    cursor.execute(data_add_q)
                    connection.commit()
                    connection.close()
                    print('Data has been added')
                    break

                elif table_name == '6': # Hospital
                    name = input('Hospital Name (String): ')
                    region = input('Region (City, State) (String): ')
                    hospitalization_cost = input('Hospitalization Cost (Integer): ')
                    data = (name, region, hospitalization_cost)
                    data_add_q = 'INSERT INTO hospital (name, region, hospitalization_cost) VALUES (' + ', '.join(data) + ')'
                    cursor.execute(data_add_q)
                    connection.commit()
                    connection.close()
                    print('Data has been added')
                    break

                else:
                    print('Tried to reach a wrong table, go back to main menu')

            #view tables & lists
            elif main_ans == '2': # (!)update queries related to view like blood_donor_list
                view_q = '' #this is the query that is going to be run after the if-conditions.
                print('View: Organ_Donor_List, Blood_Donor_List, Donor_Match_List, OperationDonor, Organ, Patient')
                view_name = input('Which view do you want: ')
                if view_name == 'Donor' or view_name == 'Organ' or view_name == 'Patient':
                    view_q = 'SELECT * FROM ' + view_name
                    cursor.execute(view_q)
                    datas = cursor.fetchall()
                    for data in datas:
                        print(data)
                        break

                elif view_name == 'Organ_Donor_List':
                    do_search = input('Do you want to (1) view all or (2) search by sth:')
                    if do_search == '1': #view all table
                        view_q = 'SELECT * FROM '+ view_name
                        cursor.execute(view_q)
                        datas = cursor.fetchall()
                        for data in datas:
                            print(data)
                        break

                    elif do_search == '2': #search by sth
                        search_by = input('Search by region, organ, doctor')
                        search_val = input('Search value: ')
                        #write the query here
                        view_q = 'SELECT * FROM Organ_Donor WHERE ' + search_by + '=' + search_val
                        cursor.execute(view_q)
                        datas = cursor.fetchall()
                        for data in datas:
                            print(data)
                        break

                elif view_name == 'Blood_Donor_List':
                    do_search = input('Do you want to (1) view all or (2) search by sth:')
                    if (do_search == '1'): #view all table
                        view_q = 'SELECT * FROM ' + view_name
                        cursor.execute(view_q)
                        datas = cursor.fetchall()
                        for data in datas:
                            print(data)
                        break

                    elif do_search == '2': #search by sth
                        search_by = input('Search by region, blood_type, typeAvailability, age_group (=, <, <=, >, >=)')
                        search_val = input('Search value: ')
                        if search_by == 'region':
                            view_q = 'SELECT * FROM Blood_Donor WHERE region = ' + search_val
                            cursor.execute(view_q)
                            datas = cursor.fetchall()
                            for data in datas:
                                print(data)
                            break

                        elif search_by == 'blood_type':
                            view_q = 'SELECT * FROM Blood_Donor WHERE blood_type = ' + search_val
                            cursor.execute(view_q)
                            datas = cursor.fetchall()
                            for data in datas:
                                print(data)
                            break

                        elif search_by == 'typeAvailability':
                            view_q = 'SELECT * FROM Blood_Donor WHERE last_donation_time = ' + search_val
                            cursor.execute(view_q)
                            datas = cursor.fetchall()
                            for data in datas:
                                print(data)
                            break

                        elif search_by == 'age_group':
                            view_q = 'SELECT * FROM Blood_Donor WHERE age ' + search_val
                            cursor.execute(view_q)
                            datas = cursor.fetchall()
                            for data in datas:
                                print(data)
                            break

                elif view_name == 'Donor_Match_List': #look further into
                    organ_or_blood = input('Do you want to look at (1) Organ matches or (2) Blood matches: ')
                    if(organ_or_blood == '1'):
                        do_search = input('Do you want to (1) view all or (2) search by organ:')
                        if (do_search == '1'): #view all table
                            cursor.execute(Donor_Organ_Match_List)
                            datas = cursor.fetchall()
                            for data in datas:
                                print(data)
                            break

                        elif do_search == '2':
                            organ_n = input('Which organ do you want to search for?: ')
                            view_q = Donor_Organ_Match_List + ' WHERE Organ_Donor.organ_name=' + organ_n
                            cursor.execute(view_q)
                            datas = cursor.fetchall()
                            for data in datas:
                                print(data)
                            break

                    elif organ_or_blood == '2':
                        do_search = input('Do you want to (1) view all or (2) search by blood:')
                        if do_search == '1': #view all table
                            cursor.execute(Donor_Blood_Match_List)
                            datas = cursor.fetchall()
                            for data in datas:
                                print(data)
                            break

                        elif do_search == '2':
                            blood_type_n = input('Which blood type do you want to search for?: ')
                            view_q = Donor_Blood_Match_List + ' WHERE Blood_Donor.blood_type=' + blood_type_n
                            cursor.execute(view_q)
                            for data in datas:
                                print(data)
                            break
                
                elif view_name == 'Income Report':
                    cursor.execute(Income_Report)
                    datas = cursor.fetchall()
                    for data in datas:
                        print(data)
                    break

                elif view_name == 'Operations Report':
                    cursor.execute(Operations_Report)
                    datas = cursor.fetchall()
                    for data in datas:
                        print(data)
                    break

                else: 
                    print('Error not a view.')

            #create the database, should be run only once.
            elif main_ans == '3':
                try:
                    # Tables
                    cursor.execute(create_Organ_Donor_table)
                    cursor.execute(create_Blood_Donor_table)
                    cursor.execute(create_Patient_table)
                    cursor.execute(create_Organ_table)
                    cursor.execute(create_Hospital_table)
                    cursor.execute(create_Doctor_table)
                    cursor.execute(create_Donor_Application_table)
                    cursor.execute(create_Works_At_table)
                    cursor.execute(create_Operates_table)
                    cursor.execute(create_Applies_table)

                    # Indices
                    cursor.execute(create_Blood_Donor_index)
                    cursor.execute(create_Organ_Donor_index)
                    cursor.execute(create_Hospital_Region_index)
                    cursor.execute(create_Doctor_Specialization_index)
                    connection.commit()
                    print('Tables are created.')
                    
                    # Roles
                    cursor.execute(create_Admin_role)
                    cursor.execute(create_Doctor_User_role)
                    cursor.execute(create_Patient_User_role)
                    connection.commit()
                    print('Roles are created.')
                    
                    connection.close()
                except:
                    print('Error: Any error has occurred.')
                break

            # delete database, only run once after database is created
            elif main_ans == '4':
                try:
                    cursor.execute(drop_Applies_table)
                    cursor.execute(drop_Blood_Donor_table)
                    cursor.execute(drop_Donor_Application)
                    cursor.execute(drop_Operates_table)
                    cursor.execute(drop_Organ_table)
                    cursor.execute(drop_Works_At)
                    connection.commit()

                    cursor.execute(drop_Doctor_table)
                    cursor.execute(drop_Hospital_table)
                    cursor.execute(drop_Organ_Donor_table)
                    cursor.execute(drop_Patient_table)
                    connection.commit()
                    print('Tables are dropped.')

                    cursor.execute(drop_Admin_role)
                    cursor.execute(drop_Doctor_User_role)
                    cursor.execute(drop_Patient_User_role)
                    print('Roles are dropped.')

                    connection.commit()
                    connection.close()
                except:
                    print('Error: Any error has occurred.')
                break
            elif main_ans == '5':
                username = input('Input a username: ')
                password = input('Input a password: ')
                view_q = 'CREATE USER ' + username + ' WITH ENCRYPTED PASSWORD ' + password
                cursor.execute(view_q)
                connection.commit()
                connection.close()
                print('User created')
                break
            elif main_ans == '6':
                sec_ans = input('1: Grant\n2: Revoke\nInput: ')
                if sec_ans == '1':
                    username = input('Input a username: ')
                    role = input('Input a role: ')
                    view_q = 'GRANT ' + role + ' TO ' + username
                    cursor.execute(view_q)
                    connection.commit()
                    connection.close()
                    print('Role granted.')
                    break

                elif sec_ans == '2':
                    username = input('Input a username: ')
                    role = input('Input a role: ')
                    view_q = 'REVOKE ' + role + ' FROM ' + username
                    cursor.execute(view_q)
                    connection.commit()
                    connection.close()
                    print('Role revoked.')
                    break

                else:
                    print('Invalid request. Input 1 or 2.')
            elif main_ans == '7':
                break
            else:
                print('Invalid request. Input 1, 2, 3, 4, 5, 6, or 7') # return back to question
    except:
        print('Error')
    break
