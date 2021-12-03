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
# drop table Organ_Donor;
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
# drop table Blood_Donor;
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

# drop table Patient;
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

# drop table Organ;
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

# drop table Hospital;
create_Hospital_table = '''
CREATE TABLE Hospital (
id SERIAL NOT NULL,
name VARCHAR(100) NOT NULL,
region VARCHAR(100) NOT NULL,
hospitalization_cost INTEGER,
PRIMARY KEY (id)
);
'''

# drop table Doctor;
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

# drop table Donor_Application;
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

# drop table Works_At;
create_Works_At_table = '''
CREATE TABLE Works_At (
doctor_id INTEGER NOT NULL,
hospital_id INTEGER NOT NULL,
PRIMARY KEY (doctor_id, hospital_id),
FOREIGN KEY (doctor_id) REFERENCES Doctor(id) ON DELETE CASCADE,
FOREIGN KEY (hospital_id) REFERENCES Hospital(id) ON DELETE CASCADE
);
'''

# drop table Operates;
create_Operates_table = '''
CREATE TABLE Operates (
doctor_id INTEGER NOT NULL,
patient_id INTEGER NOT NULL,
PRIMARY KEY (doctor_id, patient_id),
FOREIGN KEY (doctor_id) REFERENCES Doctor(id) ON DELETE CASCADE,
FOREIGN KEY (patient_id) REFERENCES Patient(id) ON DELETE CASCADE
);
'''


# drop table Applies;
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
CREATE ROLE admin WITH LOGIN ENCRYPTED PASSWORD '123456789';
GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA public 
TO admin;
'''
create_Doctor_User_role = '''
CREATE ROLE doctor_user;
GRANT ALL PRIVILEGES ON TABLE Patient TO doctor_user;
GRANT ALL PRIVILEGES ON TABLE Organ_Donor TO doctor_user;
'''

create_Patient_User_role = '''
CREATE ROLE patient_user;
GRANT ALL PRIVILEGES ON TABLE Patient TO patient_user;
'''

random_data = '''
INSERT INTO Organ_Donor (name, blood_type, last_donation_time, organ_name)
VALUES ('Bob', 'A', '02/20/2000', 'liver'), ('Bob2', 'AB', '02/20/2001', 'liver'),
('Bob3', '0', '02/20/2000', 'liver');

INSERT INTO Blood_Donor (name, blood_type, last_donation_time, region)
VALUES ('Jack', 'B', '01/10/2010', 'Chicago','IL'), ('Jack2', 'B', '02/10/2010', 'Chicago','IL'),
('Jack3', 'B', '03/10/2010', 'Chicagoo','IL'), ('Jack4', 'B', '04/10/2010', 'Chicagoo','IL');

INSERT INTO Patient (name, blood_type)
VALUES ('patient1', 'A'), ('patient1', 'B'), ('patient1', 'AB'), ('patient4', '0');

INSERT INTO Hospital (name, region)
VALUES ('Charlie', 'Chicago, IL'), ('Bernie', 'Chicag, IL'),
('Smith', 'Chicago, IL'), ('GREATEST_HOSPITAL', 'Chica, IL');

INSERT INTO Doctor (name, number_of_operations)
VALUES ('doctor1', 2), ('doctor2', 0), ('doctor1', 1), ('doctor1', 2);

INSERT INTO Donor_Application (blood_type, age, last_donation_time)
VALUES ('A', 25, '10/20/2015'), ('B', 24, '10/20/2016'),
('AB', 20, '10/20/2010'), ('0', 29, '10/20/2011');
'''


# Program runs here
while(True):
    print('Please login to the database. Recommended to login as postgres to setup database.')
    host_n = input('Enter your host name: ')
    db_n = input('Enter your database name: ')
    user_n = input('Enter your user name: ') #admin, or other users.
    user_p = input('Enter your user password: ')

    try:
        connection = psycopg2.connect(host = host_n, database = db_n, user = user_n, password = user_p, port = '5432')
        print('Login successful as ' + user_n)
        cursor = connection.cursor()
        while(True):
            print('What do you want to do? \n1: Add data to tables\n2: View tables & lists\n3: View reports\n4: Setup the database (only once),')
            main_ans = input()

            #add to a table
            if main_ans == '1':
                print('Tables: Donor(Blood or Organ), Organ, Patient, Doctor, Hospital')
                table_name = input('Which table do you want to add to: ')
                data_add = input('Enter the data: ')
                if table_name == 'Donor':
                    table_name = input('Blood or Organ: ')
                    if table_name == 'Blood': 
                        data_add_q = 'INSERT INTO Blood_Donor (name, blood_type, last_donation_time, region) VALUES ' + data_add
                        cursor.execute(data_add_q)
                        connection.commit()
                    elif table_name == 'Organ':
                        data_add_q = 'INSERT INTO Organ_Donor  VALUES ' + data_add
                        cursor.execute(data_add_q)
                        connection.commit()
                    else:
                        print('Blood or Organ only!')
                elif table_name == 'Organ':
                    data_add_q = 'INSERT INTO Organ (donor_name, organ_name) VALUES ' + data_add
                    cursor.execute(data_add_q)
                    connection.commit()
                elif table_name == 'Patient':
                    data_add_q = 'INSERT INTO Patient (name, blood_type) VALUES ' + data_add
                    cursor.execute(data_add_q)
                    connection.commit()
                elif table_name == 'Doctor':
                    data_add_q = 'INSERT INTO Doctor (name, number_of_operations) VALUES ' + data_add
                    cursor.execute(data_add_q)
                    connection.commit()
                elif table_name == 'Hospital':
                    data_add_q = 'INSERT INTO Hospital (name, region) VALUES ' + data_add
                    cursor.execute(data_add_q)
                    connection.commit()
                else:
                    print('Tried to reach a wrong table, go back to main menu')

            #view tables & lists
            elif main_ans == '2': # (!)update queries related to view like blood_donor_list
                view_q = '' #this is the query that is going to be run after the if-conditions.
                print('View: Donor, Organ, Patient, Blood_Donor_List, Organ_Donor_List, Donor_Match_List')
                view_name = input('Which view do you want: ')

                if view_name == 'Donor' or view_name == 'Organ' or view_name == 'Patient':
                    view_q = 'SELECT * FROM ' + view_name
                    cursor.execute(view_q)
                    datas = cursor.fetchall()
                    for data in datas:
                        print(data)

                elif view_name == 'Organ_Donor_List':
                    do_search = input('Do you want to (1) view all or (2) search by sth:')
                    if do_search == '1': #view all table
                        view_q = 'SELECT * FROM '+ view_name
                        cursor.execute(view_q)
                        datas = cursor.fetchall()
                        for data in datas:
                            print(data)

                    elif do_search == '2': #search by sth
                        search_by = input('Search by region, organ, doctor')
                        search_val = input('Search value: ')
                        #write the query here
                        view_q = 'SELECT * FROM Organ_Donor WHERE ' + search_by + '=' + search_val
                        cursor.execute(view_q)
                        datas = cursor.fetchall()
                        for data in datas:
                            print(data)

                elif view_name == 'Blood_Donor_List':
                    do_search = input('Do you want to (1) view all or (2) search by sth:')
                    if (do_search == '1'): #view all table
                        view_q = 'SELECT * FROM ' + view_name
                        cursor.execute(view_q)
                        datas = cursor.fetchall()
                        for data in datas:
                            print(data)

                    elif do_search == '2': #search by sth
                        search_by = input('Search by region, blood_type, typeAvailability, age_group (=, <, <=, >, >=)')
                        search_val = input('Search value: ')
                        if search_by == 'region':
                            view_q = 'SELECT * FROM Blood_Donor WHERE region = ' + search_val
                            cursor.execute(view_q)
                            datas = cursor.fetchall()
                            for data in datas:
                                print(data)
                        elif search_by == 'blood_type':
                            view_q = 'SELECT * FROM Blood_Donor WHERE blood_type = ' + search_val
                            cursor.execute(view_q)
                            datas = cursor.fetchall()
                            for data in datas:
                                print(data)
                        elif search_by == 'typeAvailability':
                            view_q = 'SELECT * FROM Blood_Donor WHERE last_donation_time = ' + search_val
                            cursor.execute(view_q)
                            datas = cursor.fetchall()
                            for data in datas:
                                print(data)
                        elif search_by == 'age_group':
                            view_q = 'SELECT * FROM Blood_Donor WHERE age ' + search_val
                            cursor.execute(view_q)
                            datas = cursor.fetchall()
                            for data in datas:
                                print(data)

                elif view_name == 'Donor_Match_List': #look further into
                    organ_or_blood = input('Do you want to look at (1) Organ matches or (2) Blood matches: ')
                    if(organ_or_blood == '1'):
                        do_search = input('Do you want to (1) view all or (2) search by organ:')
                        if (do_search == '1'): #view all table
                            cursor.execute(Donor_Organ_Match_List)
                            datas = cursor.fetchall()
                            for data in datas:
                                print(data)

                        elif do_search == '2':
                            organ_n = input('Which organ do you want to search for?: ')
                            view_q = Donor_Organ_Match_List + ' WHERE Organ_Donor.organ_name=' + organ_n

                    elif organ_or_blood == '2':
                        do_search = input('Do you want to (1) view all or (2) search by blood:')
                        if do_search == '1': #view all table
                            cursor.execute(Donor_Blood_Match_List)
                            datas = cursor.fetchall()
                            for data in datas:
                                print(data)
                        elif do_search == '2':
                            blood_type_n = input('Which blood type do you want to search for?: ')
                            view_q = Donor_Blood_Match_List + ' WHERE Blood_Donor.blood_type=' + blood_type_n
                
                elif view_name == 'Income Report':
                    cursor.execute(Income_Report)
                    datas = cursor.fetchall()
                    for data in datas:
                        print(data)
                elif view_name == 'Operations Report':
                    cursor.execute(Operations_Report)
                    datas = cursor.fetchall()
                    for data in datas:
                        print(data)
                else: 
                    print('')
            #view reports
            elif main_ans == '3':
                pass
            #create the database, should be run only once.
            elif main_ans == '4':
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

                    # Roles
                    cursor.execute(create_Admin_role)
                    cursor.execute(create_Doctor_User_role)
                    cursor.execute(create_Patient_User_role)

                    print('Tables are created.')

                    # random data
                    cursor.execute(random_data)

                    connection.commit()
                except:
                    print('Error: Already have existing tables')
            else:
                print('Invalid request. Input 1, 2, 3, or 4.') # return back to question
    except:
        print('Error')
        break
