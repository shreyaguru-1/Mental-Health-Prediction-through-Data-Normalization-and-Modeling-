NORMALIZED_DATABASE_FILENAME = 'normalized.db'
DATA_FILENAME = 'survey.csv'
DELEMETER = ','

GENDER_CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS [Gender] (
            [Gender] TEXT NOT NULL PRIMARY KEY,
            [GenderCode] INTEGER NOT NULL
        );
        """
GENDER_INSERT_TABLE = '''INSERT INTO Gender (Gender, GenderCode) VALUES(?,?)'''


COUNTRY_CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS [Country] (
            [CountryID] INTEGER NOT NULL PRIMARY KEY,
            [Country] TEXT NOT NULL
        );
        """
COUNTRY_INSERT_TABLE = '''INSERT INTO Country (Country) VALUES(?)'''

COUNTRY_STATE_CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS [CountryState] (
            [CountryStateID] INTEGER NOT NULL PRIMARY KEY,
            [CountryID] TEXT NOT NULL,
            [State] TEXT,
            FOREIGN KEY (CountryID) REFERENCES Country(CountryID)
        );
        """
COUNTRY_STATE__INSERT_TABLE = '''INSERT INTO CountryState (CountryID, State) VALUES(?,?)'''

EMPLOYEE_RANGE_CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS [EmpRange] (
            [EmpRange] TEXT NOT NULL PRIMARY KEY,
            [EmpRangeID] INTEGER NOT NULL
        );
        """
EMPLOYEE_RANGE_INSERT_TABLE = '''INSERT INTO EmpRange (EmpRange,EmpRangeID) VALUES(?,?)'''

AGE_RANGE_CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS [AgeRange] (
            [AgeRange] TEXT NOT NULL PRIMARY KEY,
            [AgeRangeID] INTEGER NOT NULL
        );
        """
AGE_RANGE_INSERT_TABLE = '''INSERT INTO AgeRange (AgeRange,AgeRangeID) VALUES(?,?)'''


EMPLOYEE_INSERT_TABLE = '''INSERT INTO Employee (Age, Gender, CountryID) VALUES(?,?,?)'''

EMPLOYEE_CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS [Employee] (
            [EmpID] INTEGER NOT NULL PRIMARY KEY,
            [Age] INTEGER NOT NULL,
            [Gender] TEXT NOT NULL,
            [CountryID] INTEGER NOT NULL,
            FOREIGN KEY (Gender) REFERENCES Gender(Gender),
            FOREIGN KEY (CountryID) REFERENCES Country(CountryID)
        );
        """

SURVEY_RECORD_RANGE_CREATE_TABLE_SQL = """CREATE TABLE IF NOT EXISTS [SurveyRecord] (
            [ID] INTEGER NOT NULL PRIMARY KEY,
            [SelfEmployed] TEXT,
            [FamilyHistory] TEXT,
            [Treatment] TEXT,
            [WorkInterfere] TEXT,
            [NoEmployees] TEXT,
            [RemoteWork] TEXT,
            [TechCompany] TEXT,
            [Benefits] TEXT,
            [CareOptions] TEXT,
            [WellnessProgram] TEXT,
            [SeekHelp] TEXT,
            [Anonymous] TEXT,
            [Leave] TEXT,
            [MentalHealthConsequences] TEXT,
            [PhysicalHealthConsequences] TEXT,
            [Coworkers] TEXT,
            [Supervisor] TEXT,
            [MentalHealthInterview] TEXT,
            [PhysicalHealthInterview] TEXT,
            [MentalVsPhysical] TEXT,
            [ObsConsequences] TEXT,
            FOREIGN KEY (ID) REFERENCES Employee(EmpID),
            FOREIGN KEY (NoEmployees) REFERENCES EmpRange(EmpRange)
            
        );
        """
SURVEY_RECORD_RANGE_INSERT_TABLE = '''INSERT INTO SurveyRecord(SelfEmployed,FamilyHistory,Treatment,WorkInterfere,
NoEmployees,RemoteWork,TechCompany,Benefits,CareOptions,WellnessProgram,SeekHelp,Anonymous,Leave,MentalHealthConsequences,
PhysicalHealthConsequences,Coworkers,Supervisor,MentalHealthInterview,PhysicalHealthInterview,MentalVsPhysical,
ObsConsequences) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''


FETCH_DATA_MODELLING = '''SELECT 
                        Employee.EmpID,
                        Employee.Age,
                        Gender.GenderCode,
                        CASE WHEN Employee.Age BETWEEN 0 AND 20 THEN 0
                            WHEN Employee.Age BETWEEN 21 AND 30 THEN 1
                            WHEN Employee.Age BETWEEN 31 AND 65 THEN 2
                            WHEN Employee.Age BETWEEN 66 AND 100 THEN 3
                        END AS AgeRange,
                        Employee.CountryID,
                        SurveyRecord.NoEmployees,
                        EmpRange.EmpRangeID as NoEmployeesRange,
                        SurveyRecord.SelfEmployed,
                        SurveyRecord.FamilyHistory,
                        SurveyRecord.Treatment,
                        SurveyRecord.WorkInterfere,
                        SurveyRecord.RemoteWork,
                        SurveyRecord.TechCompany,
                        SurveyRecord.Benefits,
                        SurveyRecord.CareOptions,
                        SurveyRecord.WellnessProgram,
                        SurveyRecord.SeekHelp,
                        SurveyRecord.Anonymous,
                        SurveyRecord.Leave,
                        SurveyRecord.MentalHealthConsequences,
                        SurveyRecord.PhysicalHealthConsequences,
                        SurveyRecord.Coworkers,
                        SurveyRecord.Supervisor,
                        SurveyRecord.MentalHealthInterview,
                        SurveyRecord.PhysicalHealthInterview,
                        SurveyRecord.MentalVsPhysical,
                        SurveyRecord.ObsConsequences
                        FROM SurveyRecord
                        INNER JOIN Employee
                            ON SurveyRecord.ID = Employee.EmpID
                        INNER JOIN Country
                            ON Employee.CountryID = Country.CountryID
                        INNER JOIN Gender
                            ON Employee.Gender = Gender.Gender
                        INNER JOIN EmpRange
                            ON SurveyRecord.NoEmployees = EmpRange.EmpRange
                        '''

Gender = {
    "A little about you":	2,
    "Agender":	2,
    "All":	2,
    "Androgyne":	2,
    "Cis Female":	1,
    "Cis Male":	0,
    "Cis Man":	0,
    "Enby":	2,
    "F":	1,
    "Femake":	1,
    "Female ":	1,
    "Female (cis)":	1,
    "Female (trans)":	1,
    "Female":	1,
    "Genderqueer":	2,
    "Guy (-ish) ^_^":	0,
    "M":	0,
    "Mail":	0,
    "Make":	0,
    "Mal":	0,
    "Male ":	0,
    "Male (CIS)":	0,
    "Male":	0,
    "Male-ish":	0,
    "Malr":	0,
    "Man":	0,
    "Nah":	2,
    "Neuter":	2,
    "Trans woman":	2,
    "Trans-female":	2,
    "Woman":	1,
    "cis male":	1,
    "cis-female/femme":	1,
    "f":	1,
    "femail":	1,
    "female":	1,
    "fluid":	1,
    "m":	0,
    "maile":	0,
    "male leaning androgynous":	2,
    "male":	0,
    "msle":	0,
    "non-binary":	2,
    "ostensibly male":	2,
    "p":	2,
    "queer":	2,
    "queer/she/they":	1,
    "something kinda male?":	2,
    "woman":	1,
    'ostensibly male, unsure what that really means':	2,
}
