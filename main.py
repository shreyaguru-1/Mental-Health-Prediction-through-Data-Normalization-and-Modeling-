import databaseMethods as dm
import pandas as pd
import constants as c
import numpy as np

#Global variable 
normalized_database_filename = c.NORMALIZED_DATABASE_FILENAME
data_filename = c.DATA_FILENAME


# Create new database and  establish the connection
def createDatabase():
    return dm.create_connection(normalized_database_filename, True)

# Get Database connection
def getDatabaseConnection():
    return dm.create_connection(normalized_database_filename)

# Create Gender table
def createTable():
    create_gender_table()   
    create_country_table()
    create_country_state_table()
    create_employee_range()
    create_age_range()
    person_record_table()
    health_record_table()
    

def create_gender_table():
    # Read the data from the csv file and create a list of tuples 
    # Insert the data into the table
    df = pd.read_csv(data_filename)
    uniqueGender = df['Gender'].unique().tolist()

    genderList = [(x, c.Gender[x]) for x in uniqueGender]
    genderList = sorted(genderList, key = lambda x:x[0])
    conn_norm = getDatabaseConnection()
    dm.create_table(conn_norm, c.GENDER_CREATE_TABLE_SQL)
    dm.execute_many_sql_statement(c.GENDER_INSERT_TABLE,genderList,conn_norm)

def create_gender_to_genderCode_dictionary():
    gender_dictionary = {}
    conn_norm = getDatabaseConnection()
    gender_rows = dm.execute_sql_statement("SELECT * FROM Gender", conn_norm)
    for i in gender_rows:
        gender_dictionary[i[0]] = i[1]
    return gender_dictionary

def create_country_table():
    # Read the data from the csv file and create a list of tuples 
    # Insert the data into the table
    df = pd.read_csv(data_filename)
    uniqueCountry = df['Country'].unique().tolist()

    uniqueCountryTuple = [(x, ) for x in uniqueCountry]
    uniqueCountryTuple = sorted(uniqueCountryTuple, key = lambda x:x[0])
    conn_norm = getDatabaseConnection()
    dm.create_table(conn_norm, c.COUNTRY_CREATE_TABLE_SQL)
    dm.execute_many_sql_statement(c.COUNTRY_INSERT_TABLE,uniqueCountryTuple,conn_norm)

def create_country_to_countryid_dictionary():
    countryid_dictionary = {}
    conn_norm = getDatabaseConnection()
    country_rows = dm.execute_sql_statement("SELECT * FROM Country", conn_norm)
    for i in country_rows:
        countryid_dictionary[i[1]] = i[0]
    return countryid_dictionary

def create_country_state_table():
    # Read the data from the csv file and create a list of tuples 
    # Insert the data into the table
    df = pd.read_csv(data_filename)
    countryid_dictionary = create_country_to_countryid_dictionary()
    uniqueCountryState = df[['Country','state']].values.tolist()
    for i in uniqueCountryState:
        if str(i[1]) == 'nan':
            i[1] = None
    uniqueCountryStateTuple = list(set([(countryid_dictionary[x[0]], x[1]) for x in uniqueCountryState]))
    uniqueCountryStateTuple = sorted(uniqueCountryStateTuple, key = lambda x:x[0])
    conn_norm = getDatabaseConnection()
    dm.create_table(conn_norm, c.COUNTRY_STATE_CREATE_TABLE_SQL)
    dm.execute_many_sql_statement(c.COUNTRY_STATE__INSERT_TABLE,uniqueCountryStateTuple,conn_norm)

def create_employee_range():
    # Read the data from the csv file and create a list of tuples 
    # Insert the data into the table
    df = pd.read_csv(data_filename)
    emplyee_range = df[['no_employees']].values.tolist()

    dict = {
        '1-5' : 0,
        '6-25' : 1,
        '26-100' : 2,
        '100-500' : 3,
        '500-1000' : 4,
        'More than 1000' : 5
    }
    emplyee_range = list(set([x[0] for x in emplyee_range]))
    emplyee_range = sorted(emplyee_range,key = lambda x: dict.get(x))
    emplyee_rangeTuple = list([(x, dict[x]) for x in emplyee_range])
    conn_norm = getDatabaseConnection()
    dm.create_table(conn_norm, c.EMPLOYEE_RANGE_CREATE_TABLE_SQL)
    dm.execute_many_sql_statement(c.EMPLOYEE_RANGE_INSERT_TABLE,emplyee_rangeTuple,conn_norm)

def create_age_range():
    # Read the data from the csv file and create a list of tuples 
    # Insert the data into the table
    df = pd.read_csv(data_filename)

    dict_age = {
        '0-20' : 0,
        '21-30' : 1,
        '31-65' : 2,
        '66-100' : 3,
    }
    age_rangeTuple = list([(key, value) for key,value in dict_age.items()])
    conn_norm = getDatabaseConnection()
    dm.create_table(conn_norm, c.AGE_RANGE_CREATE_TABLE_SQL)
    dm.execute_many_sql_statement(c.AGE_RANGE_INSERT_TABLE,age_rangeTuple,conn_norm)


def person_record_table():
    df = pd.read_csv(data_filename)
    df = df[['Age','Gender','Country']]

    df['Age'].fillna(df['Age'].median(), inplace = True)
    s = pd.Series(df['Age'])
    s[s<18] = df['Age'].median()
    df['Age'] = s
    s = pd.Series(df['Age'])
    s[s>100] = df['Age'].median()
    df['Age'] = s
    personRecord = df.values.tolist()

    country_dict = create_country_to_countryid_dictionary()
    for person in personRecord:
        person[0] = int(person[0])
        person[2] = country_dict.get(person[2])
    conn_norm = getDatabaseConnection()
    dm.create_table(conn_norm, c.EMPLOYEE_CREATE_TABLE_SQL)
    dm.execute_many_sql_statement(c.EMPLOYEE_INSERT_TABLE,personRecord,conn_norm)

def health_record_table():
    # Read the data from the csv file and create a list of tuples 
    # Insert the data into the table
    df = pd.read_csv(data_filename)
    columns = ["self_employed","family_history","treatment","work_interfere","no_employees","remote_work","tech_company","benefits","care_options","wellness_program","seek_help","anonymity","leave","mental_health_consequence","phys_health_consequence","coworkers","supervisor","mental_health_interview","phys_health_interview","mental_vs_physical","obs_consequence"]
    survey_record =df[columns].values.tolist()
    conn_norm = getDatabaseConnection()
    dm.create_table(conn_norm, c.SURVEY_RECORD_RANGE_CREATE_TABLE_SQL)
    dm.execute_many_sql_statement(c.SURVEY_RECORD_RANGE_INSERT_TABLE,survey_record,conn_norm)


def fetchData():
    conn_norm = getDatabaseConnection()

       
    sql_query = pd.read_sql_query(c.FETCH_DATA_MODELLING, conn_norm)

    # Convert SQL to DataFrame
    df = pd.DataFrame(sql_query)

    return df

def main():
    conn_norm = createDatabase()
    createTable()
    conn_norm.close()

main()
    