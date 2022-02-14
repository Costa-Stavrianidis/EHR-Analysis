"""EHR Testing"""

import pytest

from ehr_analysis import parse_data, num_older_than, sick_patients, admission_age


def test_parse_data():
    """Test parsing data."""
    filename1 = "PatientCorePopulatedTable.txt"
    filename2 = "LabsCorePopulatedTable.txt"
    assert parse_data(filename1)[0][3] == "PatientRace"
    assert parse_data(filename1)[1][0] == "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F"
    assert parse_data(filename1)[9][5] == "English"
    assert parse_data(filename2)[0][1] == "AdmissionID"
    assert parse_data(filename2)[1][0] == "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"
    assert parse_data(filename2)[9][4] == "k/cumm"


def test_num_older_than():
    """Test returning number of patients older than given year."""
    age1 = 0
    age2 = 150
    age3 = 54
    age4 = 67
    patient_data = parse_data("PatientCorePopulatedTable.txt")
    assert num_older_than(age1, patient_data) == 100
    assert num_older_than(age2, patient_data) == 0
    assert num_older_than(age3, patient_data) == 68
    assert num_older_than(age4, patient_data) == 42


def test_sick_patients():
    """Test returning unique list of sick patients."""
    lab1 = "URINALYSIS: RED BLOOD CELLS"
    lab2 = "CBC: LYMPHOCYTES"
    gt_lt1 = ">"
    gt_lt2 = "<"
    value1 = 1.5
    value2 = 2.5
    lab_data = parse_data("LabsCorePopulatedTable.txt")
    assert "1A8791E3-A61C-455A-8DEE-763EB90C9B2C" in sick_patients(
        lab1, gt_lt1, value1, lab_data
    )
    assert "1A8791E3-A61C-455A-8DEE-763EB90C9B2C" in sick_patients(
        lab2, gt_lt2, value2, lab_data
    )


def test_admission_age():
    """Test returning age at first admission of given patient."""
    patient1 = "1A8791E3-A61C-455A-8DEE-763EB90C9B2C"
    patient2 = "81C5B13B-F6B2-4E57-9593-6E7E4C13B2CE"
    patient_data = parse_data("PatientCorePopulatedTable.txt")
    lab_data = parse_data("LabsCorePopulatedTable.txt")
    assert admission_age(patient1, patient_data, lab_data) == 18
    assert admission_age(patient2, patient_data, lab_data) == 23
