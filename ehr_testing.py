"""EHR Testing"""

import pytest
import sqlite3

from ehr_analysis import (
    parse_patient_data,
    parse_lab_data,
    num_older_than,
    sick_patients,
    admission_age,
)


parse_patient_data("patient_test_data.txt")
parse_lab_data("lab_test_data.txt")


def test_num_older_than():
    """Test returning number of patients older than given year."""
    age1 = 0
    age2 = 150
    age3 = 52
    age4 = 60
    assert num_older_than(age1) == 3
    assert num_older_than(age2) == 0
    assert num_older_than(age3) == 2
    assert num_older_than(age4) == 1


def test_sick_patients():
    """Test returning unique list of sick patients."""
    lab1 = "CBC: MONOCYTES"
    lab2 = "CBC: HEMOGLOBIN"
    gt_lt1 = ">"
    gt_lt2 = "<"
    value1 = 0.2
    value2 = 18
    assert "79A7BA2A-D35A-4CB8-A835-6BAA13B0058C" in sick_patients(lab1, gt_lt1, value1)
    assert "56A35E74-90BE-44A0-B7BA-7743BB152133" in sick_patients(lab2, gt_lt2, value2)


def test_admission_age():
    """Test returning age at first admission of given patient."""
    patient1 = "DB92CDC6-FA9B-4492-BC2C-0C588AD78956"
    patient2 = "79A7BA2A-D35A-4CB8-A835-6BAA13B0058C"
    assert admission_age(patient1) == 15
    assert admission_age(patient2) == 27
