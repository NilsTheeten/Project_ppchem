"""This file contains tests for the functions in the Solutions_Solubility.py file."""

# Importing functions from Basic_functions.py file and Solutions_Solubility.py file
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from hydroponics.Basic_functions import *
from hydroponics.Solutions_Solubility import *


#-----------------Test Check_solubility function--------------------------------
 
def test_valid_solubility_salt_input_bool_output():
    # Test with soluble salts
    solution = {"MnCl2" : 0.0223, "KNO3" : 0.493, "Ca(NO3)2" : 0.945}
    assert check_solubility(solution, input_type="salt", output_type="bool") == True, "check_solubility: Test valid_solubility_salt_input_bool_output failed"

def test_valid_solubility_salt_input_analysis_output():
    # Test with soluble salts
    solution = {"MnCl2" : 0.0223, "KNO3" : 0.493, "Ca(NO3)2" : 0.945}
    assert check_solubility(solution, input_type="salt", output_type="analysis") == "all salts are soluble", "check_solubility: Test valid_solubility_salt_input_analysis_output failed"

def test_valid_solubility_ion_input_update_output():
    # Test with soluble salts
    solution = {"Mn": 0.05, "Cl": 0.05, "K": 0.03, "NO3": 0.02}
    assert check_solubility(solution, input_type="ion", output_type="update") == [], "check_solubility: Test valid_solubility_ion_input_update_output failed"

def test_insoluble_solution_salt_input_bool_output():
    # Test with insoluble salts
    solution = {"MnCl2" : 0.0223, "KNO3" : 493, "Ca(NO3)2" : 0.945}
    assert check_solubility(solution, input_type="salt", output_type="bool") == False, "check_solubility: Test insoluble_solution_salt_input_bool_output failed"
    
def test_insoluble_solution_salt_input_analysis_output():
    # Test with insoluble salts
    solution = {"MnCl2" : 0.0223, "KNO3" : 493, "Ca(NO3)2" : 0.945}
    assert check_solubility(solution, input_type="salt", output_type="analysis") == "The following salts precipitate: KNO3    ","check_solubility: Test insoluble_solution_salt_input_analysis_output failed"

def test_invalid_input_type():
    # Test with invalid input type
    solution = {"NaCl": 0.1, "KBr": 0.05}
    try:
        check_solubility(solution, input_type="invalid", output_type="bool")
    except ValueError as e:
        assert str(e) == "Invalid input type. Please choose either 'salt' or 'ion'.", "check_solubility: Test invalid_input_type failed"

def test_invalid_output_type():
    # Test with invalid output type
    solution = {"NaCl": 0.1, "KBr": 0.05}
    try:
        check_solubility(solution, input_type="salt", output_type="invalid")
    except ValueError as e:
        assert str(e) == "Invalid output type. Please choose either 'bool', 'analysis', or 'update'.", "check_solubility: Test invalid_output_type failed"
        
        
        
#-----------------Test analyse_nutriments function--------------------------------
def test_ion_input():
    """
    Test with ion input
    """
    solution = {"Na+": 0.1, "Cl-": 0.1, "K+": 0.05, "NO3(-)": 0.05}
    plant = {"Na+": 0.2, "Cl-": 0.2, "K+": 0.1, "NO3(-)": 0.1}
    growth_time = 10
    volume = 1
    assert analyse_nutriments(solution, plant, growth_time, volume, input_type_solution = "ion") == [False, 5, 'Na+'], "analyse_nutriments: Test ion_input failed"

def test_salt_input():
    solution = {"NaCl":0.1, "KNO3": 0.05}
    plant = {"Na+": 0.6, "Cl-": 0.9, "K+": 0.8, "NO3(-)": 0.7}
    growth_time = 100
    volume = 2
    assert analyse_nutriments(solution, plant, growth_time, volume) == [False, 12, 'K+'], "analyse_nutriments: Test salt_input failed"

def test_negative_volume():
    solution = {"NaCl":0.1, "KNO3": 0.05}
    plant = {"Na+": 0.2, "Cl-": 0.2, "K+": 0.1, "NO3(-)": 0.1}
    growth_time = 10
    volume = -1
    try:
        analyse_nutriments(solution, plant, growth_time, volume)
    except ValueError as e:
        assert str(e) == "Volume must be positive.", "analyse_nutriments: Test negative_volume failed"
        
#-----------------Test update_sol() function--------------------------------
def test_update_sol_basic():
    # Define a simple ions_solution and plant requirements
    ions_solution = {
        'Na': 5.0,
        'K': 2.0,
        'Ca': 1.0
    }
    plant = {
        'Na': 1.0,
        'K': 2.0,
        'Ca': 0.5
    }

    # Expected outcome after one day
    expected_solution = {
        'Na': 4.0,
        'K': 0.0,
        'Ca': 0.5
    }

    result = update_sol(ions_solution, plant)
    assert result == expected_solution, f"Test failed: {result} != {expected_solution}"
    print("test_update_sol_basic passed")

def test_update_sol_with_solubility():
    # Define a ions_solution and plant requirements
    ions_solution = {
        'Na': 5.0,
        'K': 3.0,
        'Ca': 4.0
    }
    plant = {
        'Na': 2.0,
        'K': 1.0,
        'Ca': 1.0
    }

    # Mock the check_solubility function
    def mock_check_solubility(solution, input_type="ion", output_type=None):
        if output_type == "update":
            return ['Ca']
        return False
    
    global check_solubility
    check_solubility = mock_check_solubility

    # Expected outcome after one day, considering Ca becomes unsoluble
    expected_solution = {
        'Na': 3.0,
        'K': 2.0,
        'Ca': 0.0
    }

    result = update_sol(ions_solution, plant)
    assert result == expected_solution, f"Test failed: {result} != {expected_solution}"


        
    
