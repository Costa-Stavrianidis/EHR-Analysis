"""EHR Testing"""

import pytest

from ehr_analysis import parse_data, num_older_than, sick_patients, admission_age


def test_parse_data():
    """Test parsing data."""
    filename1 = "patient_test_data.txt"
    filename2 = "lab_test_data.txt"
    assert parse_data(filename1)[0][3] == "PatientRace"
    assert parse_data(filename1)[1][0] == "DB92CDC6-FA9B-4492-BC2C-0C588AD78956"
    assert parse_data(filename1)[3][5] == "English"
    assert parse_data(filename2)[0][1] == "AdmissionID"
    assert parse_data(filename2)[1][0] == "DB92CDC6-FA9B-4492-BC2C-0C588AD78956"
    assert parse_data(filename2)[2][4] == "k/cumm"


def test_num_older_than():
    """Test returning number of patients older than given year."""
    age1 = 0
    age2 = 150
    age3 = 52
    age4 = 60
    patient_data = parse_data("patient_test_data.txt")
    assert num_older_than(age1, patient_data) == 3
    assert num_older_than(age2, patient_data) == 0
    assert num_older_than(age3, patient_data) == 2
    assert num_older_than(age4, patient_data) == 1


def test_sick_patients():
    """Test returning unique list of sick patients."""
    lab1 = "CBC: MONOCYTES"
    lab2 = "CBC: HEMOGLOBIN"
    gt_lt1 = ">"
    gt_lt2 = "<"
    value1 = 0.2
    value2 = 18
    lab_data = parse_data("lab_test_data.txt")
    assert "79A7BA2A-D35A-4CB8-A835-6BAA13B0058C" in sick_patients(
        lab1, gt_lt1, value1, lab_data
    )
    assert "56A35E74-90BE-44A0-B7BA-7743BB152133" in sick_patients(
        lab2, gt_lt2, value2, lab_data
    )


def test_admission_age():
    """Test returning age at first admission of given patient."""
    patient1 = "DB92CDC6-FA9B-4492-BC2C-0C588AD78956"
    patient2 = "79A7BA2A-D35A-4CB8-A835-6BAA13B0058C"
    patient_data = parse_data("patient_test_data.txt")
    lab_data = parse_data("lab_test_data.txt")
    assert admission_age(patient1, patient_data, lab_data) == 15
    assert admission_age(patient2, patient_data, lab_data) == 27
