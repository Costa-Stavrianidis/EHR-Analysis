"""Computational Complexity/Data Structures."""

from datetime import datetime


def parse_data(filename: str) -> list[list[str]]:
    """Read and parses the data file."""
    with open(filename, "r", encoding="utf-8-sig") as file:  # O(1)
        lines = file.readlines()  # O(N)
        file_list = []  # O(1)
        for row in lines:  # O(N)
            row = row.split("\t")  # O(1)
            file_list.append(row)  # O(1)
    return file_list  # O(1)


# 1 + N + 1 + N * (1 + 1) + 1 -> 3(N) + 3 -> O(N)
# Opened file, created empty list which is constant time. Read through lines
# of file which is linear time, and iterated through lines which is linear time
# while splitting the rows (constant) and appending to a new list (constant).
# Finally, the list of lists was returned, which is constant, so the complexity
# overall is O(n).


def num_older_than(age: float, patient_data: list[list[str]]) -> int:
    """Take data and returns the number of patients older
    than a given age (in years).

    """
    # Header row must have the DOB column labeled exactly "PatientDateOfBirth"
    today = datetime.now()  # O(1)
    x = patient_data[0].index("PatientDateOfBirth")  # O(1)
    DOB = []  # O(1)
    older = 0  # O(1)
    for row in patient_data[1:]:  # O(N)
        DOB.append(datetime.strptime(row[x], "%Y-%m-%d %H:%M:%S.%f"))  # O(1)
    for i in DOB:  # O(N)
        if ((today - i) / 365.2425).days > age:  # O(1)
            older += 1  # O(1)
    return older  # O(1)


# 1 + 1 + 1 + N * 1 + N * (1 + 1) + 1 -> 3N + 4 -> O(N)
# Made a datetime variable, assigned a variable an integer, created an empty
# list, and set a variable to zero, all of which are constant time. Iterated
# through patient data which is linear time, and appended to empty list which
# is constant. Iterated through the appended list, which is linear time, and
# then made a Boolean statement which is constant, and added a constant to an
# integer, which is constant time. Finally, the integer was returned, which is
# constant time, so the overall complexity is O(N).


def sick_patients1(
    lab: str, gt_lt: str, value: float, lab_data: list[list[str]]
) -> list[str]:
    """Take data and returns a unique list of patients who have a given test
    with value above (">") or below ("<") a given level.

    """
    # Header row must have the patient ID column labeled exactly "PatientID"
    # Header row must have the given test column labeled exactly "LabName"
    # Header row must have the given test result labeled exactly "LabValue"
    x = lab_data[0].index("PatientID")  # O(N)
    y = lab_data[0].index("LabName")  # O(N)
    z = lab_data[0].index("LabValue")  # O(N)
    patients = []  # O(1)
    patients_sick = set()  # O(1)
    for row in lab_data[1:]:  # O(N)
        if row[y] == lab:  # O(1)
            patients.append(row)  # O(1)
    for rows in patients:  # O(N)
        rows[z] = float(rows[z])  # O(1)
        if gt_lt == ">":  # O(1)
            if rows[z] > value:  # O(1)
                patients_sick.add(rows[x])  # O(1)
        elif gt_lt == "<":  # O(1)
            if rows[z] < value:  # O(1)
                patients_sick.add(rows[x])  # O(1)
    patients_sick = list(patients_sick)  # O(1)
    return patients_sick  # O(1)


# N + N + N + 1 + 1 + N * (1 * 1) + N * (1 + 1 * 1 * 1 + 1 * 1 * 1) + 1 + 1
# -> 7N + 7 -> O(N)
# Assigned three variables as integers which is constant time, and made two
# empty lists which is also constant time. Iterated through lab data (linear)
# and added rows (constant). Iterated through the new set (linear) and checked
# to see if values were greater than or less than (linear). Finally, kept
# unique values and returned the final set, which is constant time. The overall
# complexity is O(N).
