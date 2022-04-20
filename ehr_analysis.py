"""EHR Analysis."""

from datetime import datetime
import sqlite3

con = sqlite3.connect("ehr.db")


def parse_patient_data(filename: str) -> None:
    """Read and parse the patient data file into a SQLite table."""
    # Header row must have variables named exactly as defined below
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Patient ([patient_id] TEXT PRIMARY KEY, [gender] TEXT, [DOB] TEXT, [race] TEXT)"
    )  # O(1)
    with open(filename, "r", encoding="utf-8-sig") as patient_file:  # O(1)
        patient_lines = patient_file.readlines()  # O(N)
        patient_file_list = []  # O(1)
        for row in patient_lines:  # O(N)
            row = row.split("\t")  # O(1)
            patient_file_list.append(row)  # O(1)
        patient_ID_col_index = patient_file_list[0].index("PatientID")  # O(N)
        patient_gender_col_index = patient_file_list[0].index("PatientGender")  # O(N)
        patient_DOB_col_index = patient_file_list[0].index("PatientDateOfBirth")  # O(N)
        patient_race_col_index = patient_file_list[0].index("PatientRace")  # O(N)
        for patients in patient_file_list[1:]:  # O(N)
            patient_list = [
                patients[patient_ID_col_index],
                patients[patient_gender_col_index],
                patients[patient_DOB_col_index],
                patients[patient_race_col_index],
            ]  # O(4)
            cur.execute(
                "INSERT or REPLACE INTO Patient VALUES (?, ?, ?, ?)", patient_list
            )  # O(1)


# 1 + 1 + N + 1 + N * (2) + N + N + N + N + N * (4) + 1 -> 11(N) + 4 -> O(N)


def parse_lab_data(filename: str) -> None:
    """Read and parse the lab data file into a SQLite table."""
    # Header row must have variables named exactly as defined below
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Lab ([patient_id] TEXT, [test] TEXT, [value] TEXT, [test_date] TEXT)"
    )  # O(1)
    with open(filename, "r", encoding="utf-8-sig") as lab_file:  # O(1)
        lab_lines = lab_file.readlines()  # O(M)
        lab_file_list = []  # O(1)
        for row in lab_lines:  # O(M)
            row = row.split("\t")  # O(1)
            lab_file_list.append(row)  # O(1)
        lab_ID_col_index = lab_file_list[0].index("PatientID")  # O(M)
        lab_test_col_index = lab_file_list[0].index("LabName")  # O(M)
        lab_value_col_index = lab_file_list[0].index("LabValue")  # O(M)
        lab_admission_col_index = lab_file_list[0].index("LabDateTime\n")  # O(M)
        for labs in lab_file_list[1:]:  # O(M)
            lab_list = [
                labs[lab_ID_col_index],
                labs[lab_test_col_index],
                labs[lab_value_col_index],
                labs[lab_admission_col_index],
            ]  # O(4)
            cur.execute(
                "INSERT or REPLACE INTO Lab VALUES (?, ?, ?, ?)", lab_list
            )  # O(1)


# 1 + 1 + M + 1 + M * (2) + M + M + M + M + M * (4) + 1 -> 11(M) + 4 -> O(M)

# These functions open the file and create a patient or lab table in the database "ehr.db".
# Every row in the Patient table is a patient from the original patient file with their
# information, and every row in the Lab table is a lab test for a  particular patient from
# the original lab file. The functions use the header row of the original data files to find
# which index of each row contains the variable named in the header row. The overall complexity
# is O(N) or O(M). Note that to add more columns of the original data files as table variables,
# simply add the variables in the SQLite CREATE TABLE command, store the index of the variable,
# and include it in the patient_list or lab_list object, depending on the function you are using.


class Patient:
    """Patient class with attributes and properties."""

    def __init__(self, cur, ID: str):
        """Initialize the patient class."""
        self.cur = cur
        self.ID = ID

    @property
    def gender(self) -> str:
        """Gender of patient."""
        gender = self.cur.execute(
            "SELECT gender FROM Patient WHERE patient_id = ?", (self.ID,)
        )
        return list(gender)[0][0]

    @property
    def DOB(self) -> str:
        """Date of birth of patient."""
        DOB = self.cur.execute(
            "SELECT DOB FROM Patient WHERE patient_id = ?", (self.ID,)
        )
        return list(DOB)[0][0]

    @property
    def race(self) -> str:
        """Race of patient."""
        race = self.cur.execute(
            "SELECT race FROM Patient WHERE patient_id = ?", (self.ID,)
        )
        return list(race)[0][0]

    @property
    def age(self) -> int:
        """Age of patient as of today."""
        today = datetime.now()
        dateofbirth = datetime.strptime(self.DOB, "%Y-%m-%d %H:%M:%S.%f")
        years = (today - dateofbirth) / 365.2425
        return years.days


class Lab:
    """Lab class with attributes and properties."""

    def __init__(self, cur, ID: str, test: str, admission: str):
        """Initialize the lab class."""
        self.cur = cur
        self.ID = ID
        self.test = test
        self.admission = admission

    @property
    def value(self) -> float:
        """Value of test result."""
        value = self.cur.execute(
            # f"SELECT value FROM Lab WHERE patient_id = '{self.ID}' AND test = '{self.test}' AND test_date = '{self.admission}'"
            "SELECT value FROM Lab WHERE patient_id = ? AND test = ? AND test_date = ?",
            (
                self.ID,
                self.test,
                self.admission,
            ),
        )
        Value = float(list(value)[0][0])
        return Value

    @property
    def admission_date(self) -> datetime:
        """Admission date for test in datetime format."""
        admission_date = self.cur.execute(
            # f"SELECT test_date FROM Lab WHERE patient_id = '{self.ID}' AND test = '{self.test}' AND test_date = '{self.admission}'"
            "SELECT test_date FROM Lab WHERE patient_id = ? AND test = ? AND test_date = ?",
            (
                self.ID,
                self.test,
                self.admission,
            ),
        )
        Admission_date = datetime.strptime(
            list(admission_date)[0][0][:23], "%Y-%m-%d %H:%M:%S.%f"
        )
        return Admission_date


def num_older_than(age: float) -> int:
    """Take data and return the number of patients older
    than a given age (in years).

    """
    cur = con.cursor()
    older = 0  # O(1)
    patient_list = []  # O(1)
    cur.execute("SELECT * FROM Patient")  # O(1)
    patients_table = cur.fetchall()  # O(1)
    for patients in patients_table:  # O(N)
        patient_list.append(Patient(cur, patients[0]))  # O(2)
    for patient in patient_list:  # O(N)
        if patient.age > age:  # O(1)
            older += 1  # O(1)
    return older  # O(1)


# 1 + 1 + 1 + 1 + N * (2) + N * (1 + 1) + 1 -> 4N + 5 -> O(N)

# This function takes the patient data from the Patient table in the ehr.db
# SQLite database and creates a list of Patient objects from all of the rows
# in the table. It then iterates through this list and find how many patients have an
# age property that is above the given input age in the function. The overall complexity
# is O(N), so linear time.


def sick_patients(test: str, gt_lt: str, lab_value: float) -> set[str]:
    """Take data and return a unique list of patients who have a given test
    with value above (">") or below ("<") a given level.

    """
    cur = con.cursor()
    lab_list = []  # O(1)
    patients_sick = set()  # O(1)
    cur.execute("SELECT * FROM Lab")  # O(1)
    labs_table = cur.fetchall()  # O(1)
    for labs in labs_table:  # O(M)
        lab_list.append(Lab(cur, labs[0], labs[1], labs[3]))  # O(4)
    for rows in lab_list:  # O(M)
        if gt_lt == ">":  # O(1)
            if rows.value > lab_value and rows.test == test:  # O(2)
                patients_sick.add(rows.ID)  # O(1)
        elif gt_lt == "<":  # O(1)
            if rows.value < lab_value and rows.test == test:  # O(2)
                patients_sick.add(rows.ID)  # O(1)
    return patients_sick  # O(1)


# 1 + 1 + 1 + 1 + M * (4) + M * (8) + 1 -> 12M + 5 -> O(M)

# This function takes data the lab data from the Lab table in the ehr.db SQLite
# database and creates a list of Lab objects from all of the rows in the table.
# It then iterates through the list of of Lab objects and create a unique
# list of strings that are patient ID's of patients that have a certain
# lab test value above or below a given level. The overall complexity is O(M).


def admission_age(patient: str) -> int:
    """Take patient and lab data and return the age at first admission
    of any given patient.

    """
    cur = con.cursor()
    patient_labs = []  # O(1)
    cur.execute("SELECT * FROM Lab")  # O(1)
    lab_table = cur.fetchall()  # O(1)
    for labs in lab_table:  # O(M)
        if labs[0] == patient:  # O(1)
            patient_labs.append(Lab(cur, labs[0], labs[1], labs[3]))  # O(4)
    patient_object = None  # O(1)
    cur.execute("SELECT * FROM Patient")  # O(1)
    patient_table = cur.fetchall()  # O(1)
    for patients in patient_table:  # O(N)
        if patients[0] == patient:  # O(1)
            patient_object = Patient(cur, patients[0])  # O(2)
    patient_DOB = datetime.strptime(patient_object.DOB, "%Y-%m-%d %H:%M:%S.%f")  # O(1)
    admission_ages = []  # O(1)
    for lab_objects in patient_labs:  # O(M)
        admission_ages.append(lab_objects.admission_date - patient_DOB)  # O(1)
    age = int(min(admission_ages).days / 365.2425)  # O(1)
    return age  # O(1)


# 1 + 1 + 1 + M * (4 + 1) + 1 + 1 + 1 + N * (1 + 2) + 1 + 1 + M * 1 + 1 + 1
# -> 6M + 3N + 10 -> O(N) + O(M)

# This function takes data from the Lab table in the ehr.db SQLite database and
# creates a list of lab objects from all the rows in the table that have a matching
# patient ID to the one inputted in the function. It then takes data from the Patient
# table in the ehr.db database and stores a patient object for the row in the table
# that has a matching patient ID to the one inputted into the function. It then takes
# the DOB property from the patient object and makes a list of all the lab objects
# admission dates subtracted by the patient's DOB (in datetime format). It then takes
# the minimum of the list, which would be the patient's first lab admission date, and
# calculates how old they were at that time. The overall complexity is O(N) + O(M).
