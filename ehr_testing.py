"""EHR Testing"""

import pytest

from ehr_analysis import (
    parse_patient_data,
    parse_lab_data,
    num_older_than,
    sick_patients,
    admission_age,
)


def test_parse_patient_data():
    """Test parsing patient data."""
    filename1 = "patient_test_data.txt"
    assert (
        parse_patient_data(filename1)["DB92CDC6-FA9B-4492-BC2C-0C588AD78956"].ID
        == "DB92CDC6-FA9B-4492-BC2C-0C588AD78956"
    )
    assert (
        parse_patient_data(filename1)["56A35E74-90BE-44A0-B7BA-7743BB152133"].race
        == "White"
    )


def test_parse_lab_data():
    """Test parsing lab data."""
    filename2 = "lab_test_data.txt"
    assert (
        parse_lab_data(filename2)["DB92CDC6-FA9B-4492-BC2C-0C588AD78956"][1].test
        == "CBC: MONOCYTES"
    )
    assert (
        parse_lab_data(filename2)["56A35E74-90BE-44A0-B7BA-7743BB152133"][0].value
        == "17"
    )


def test_num_older_than():
    """Test returning number of patients older than given year."""
    age1 = 0
    age2 = 150
    age3 = 52
    age4 = 60
    patient_data = parse_patient_data("patient_test_data.txt")
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
    lab_data = parse_lab_data("lab_test_data.txt")
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
    patient_data = parse_patient_data("patient_test_data.txt")
    lab_data = parse_lab_data("lab_test_data.txt")
    assert admission_age(patient1, patient_data, lab_data) == 15
    assert admission_age(patient2, patient_data, lab_data) == 27
