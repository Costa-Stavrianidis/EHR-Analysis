"""Computational Complexity/Data Structures."""

from datetime import datetime


class Patient:
    """Patient class with instance attributes."""

    def __init__(self, ID: [str], gender: [str], DOB: [str], race: [str]):
        """Initialize the patient class."""
        self.ID = ID
        self.gender = gender
        self.DOB = DOB
        self.race = race

    @property
    def age(self) -> int:
        """Age of patient."""
        today = datetime.now()
        dateofbirth = datetime.strptime(self.DOB, "%Y-%m-%d %H:%M:%S.%f")
        years = (today - dateofbirth) / 365.2425
        return years.days


class Lab:
    """Lab class with instance attributes."""

    def __init__(self, ID: [str], test: [str], value: [str], admission: [str]):
        """Initialize the lab class."""
        self.ID = ID
        self.test = test
        self.value = value
        self.admission = admission


def parse_patient_data(filename: str) -> list[Patient]:
    """Read and parse the patient data file."""
    # Header row must have variables named exactly as defined below
    with open(filename, "r", encoding="utf-8-sig") as file:  # O(1)
        lines = file.readlines()  # O(N)
        file_list = []  # O(1)
        for row in lines:  # O(N)
            row = row.split("\t")  # O(1)
            file_list.append(row)  # O(1)
        patient_ID_col_index = file_list[0].index("PatientID")  # O(N)
        patient_gender_col_index = file_list[0].index("PatientGender")  # O(N)
        patient_DOB_col_index = file_list[0].index("PatientDateOfBirth")  # O(N)
        patient_race_col_index = file_list[0].index("PatientRace")  # O(N)
        patient_list = []  # O(1)
        for patients in file_list[1:]:  # O(N)
            patient_list.append(
                Patient(
                    patients[patient_ID_col_index],
                    patients[patient_gender_col_index],
                    patients[patient_DOB_col_index],
                    patients[patient_race_col_index],
                )
            )  # O(4)
    return patient_list  # O(1)


# 1 + N + 1 + N * (1 + 1) + N + N + N + N + 1 + N * (4) + 1 -> 11(N) + 4 -> O(N)


def parse_lab_data(filename: str) -> list[Lab]:
    """Read and parse the lab data file."""
    # Header row must have variables named exactly as defined below
    with open(filename, "r", encoding="utf-8-sig") as file:  # O(1)
        lines = file.readlines()  # O(N)
        file_list = []  # O(1)
        for row in lines:  # O(N)
            row = row.split("\t")  # O(1)
            file_list.append(row)  # O(1)
        lab_ID_col_index = file_list[0].index("PatientID")  # O(N)
        lab_test_col_index = file_list[0].index("LabName")  # O(N)
        lab_value_col_index = file_list[0].index("LabValue")  # O(N)
        lab_admission_col_index = file_list[0].index("LabDateTime\n")  # O(N)
        lab_list = []  # O(1)
        for labs in file_list[1:]:  # O(N)
            lab_list.append(
                Lab(
                    labs[lab_ID_col_index],
                    labs[lab_test_col_index],
                    labs[lab_value_col_index],
                    labs[lab_admission_col_index],
                )
            )  # O(4)
    return lab_list  # O(1)


# 1 + N + 1 + N * (1 + 1) + N + N + N + N + 1 + N * (4) + 1 -> 11(N) + 4 -> O(N)

# Both functions open the file and create a list, with every element of the list
# being a row in the data file. They then use the header row of the data file
# to find which index of each row contains the variable named in the header row.
# After finding the indexes for the variables, the functions iterate through the
# list of rows, taking the elements of the rows and defining the custom class
# (Patient or Lab) attributes as the elements of the rows that match the
# attributes. This will create a Patient or Lab object for each row in the dataset.
# The functions then return a list of Patient objects or a list of Lab objects. The
# overall complexity is O(N), which is linear time. Note that to add more columns
# of the data as attributes, simply add the attributes to the Patient or Lab class,
# define the index of the column in the function, and then add the attribute to
# the Patient or Lab class in the function using that index.


def num_older_than(age: float, patient_data: list[Patient]) -> int:
    """Take data and return the number of patients older
    than a given age (in years).

    """
    older = 0  # O(1)
    for patients in patient_data:  # O(N)
        if patients.age > age:  # O(1)
            older += 1  # O(1)
    return older  # O(1)


# 1 + N * (1 * 1) + 1 -> N + 3 -> O(N)

# This function takes the patient data in the form of a list of
# Patient objects. It will then iterate through this list and find
# how many patients have an age property (their age as of today in
# years) that is above the given input age in the function. The
# overall complexity is O(N), so linear time.


def sick_patients(
    lab: str, gt_lt: str, lab_value: float, lab_data: list[Lab]
) -> list[str]:
    """Take data and return a unique list of patients who have a given test
    with value above (">") or below ("<") a given level.

    """
    patients = []  # O(1)
    patients_sick = set()  # O(1)
    for labs in lab_data:  # O(N)
        if labs.test == lab:  # O(1)
            patients.append(labs)  # O(1)
    for rows in patients:  # O(N)
        rows.value = float(rows.value)  # O(1)
        if gt_lt == ">":  # O(1)
            if rows.value > lab_value:  # O(1)
                patients_sick.add(rows.ID)  # O(1)
        elif gt_lt == "<":  # O(1)
            if rows.value < lab_value:  # O(1)
                patients_sick.add(rows.ID)  # O(1)
    patients_sick = list(patients_sick)  # O(1)
    return patients_sick  # O(1)


# 1 + 1 + N * (1 * 1) + N * (1 + 1 * 1 * 1 + 1 * 1 * 1) + 1 + 1 -> 5N + 4 -> O(N)

# This function takes data in the form of a list of Lab objects. It
# will iterate through the list of of Lab objects and create a unique
# list of strings that are patient ID's of patients that have a certain
# lab test value above or below a given level. The overall complexity is O(N),
# which is linear time.


def admission_age(
    patient: str, patient_data: list[Patient], lab_data: list[Lab]
) -> int:
    """Take lab and patient data and return the age at first admission
    of any given patient.

    """
    for patients in patient_data:
        if patients.ID == patient:
            patient_DOB = datetime.strptime(patients.DOB, "%Y-%m-%d %H:%M:%S.%f")
    admissions = []
    for labs in lab_data:
        if labs.ID == patient:
            admissions.append(
                datetime.strptime(labs.admission[:23], "%Y-%m-%d %H:%M:%S.%f")
                - patient_DOB
            )
    age = int(min(admissions).days / 365.2425)
    return age
