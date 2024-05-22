"""This file contains tests for the functions in the Basic_functions.py file."""

# Importing functions from Basic_functions.py file
import sys
import os
from pytest import approx
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from hydroponics import *

#--------------------------- Test get_molar_mass() ------------------------------
def test_molar_mass ():
    mol = ["Ca(NO3)2", "Ca(2+)(NO3)2(-)", "Ca++(NO3)2", "Ca(NO3)NO3"]
    for i in range(len(mol)):
        assert round(get_molar_mass(mol[i]),3) == 164.086, "Test molar mass failed: did not understand {mol[i]}"
           


#--------------------------- Test get_Ksp() ------------------------------
def test_get_Ksp():
    list = ['KNO3', 'KH2PO4', 'MnCl2', 'NaCl', 'KCl', 'KOH', 'K2SO4', 'K2CO3', 'KHCO3', 'CaCl2', 'MgCl2', 'FeCl3', 'AlCl3']
    Ksp_list = [
        9.76904463917891,
        2.758051364759525,
        810.1350827255483,
        37.716373801958376,
        21.04634685946477,
        398.49994656470716,
        1.0339299769044514,
        2072.3420181206798,
        11.330982570493006,
        1210.091270423005,
        754.4989632174183,
        0,
        3759.188606917454
    ]
    for i in range(len(list)):
        assert get_Ksp(list[i]) == approx(Ksp_list[i], rel=1e-3), f"Test_get_Ksp failed: Error for {list[i]}"
        
        

#----------------------------- Test get_Q() ----------------------------
def test_Get_Q():
    salt = "Ca(NO3)2"
    ions = {"Ca(2+)": 0.5, "NO3(-)": 0.5, "Cl-": 0.5}
    assert get_Q_solubility(salt, ions) == 0.125, "Test get_Q failed"
    
    
#----------------------------- Test salt2ions() ----------------------------
def test_mol_unit():
    solution_dict = {"NaCl": 0.1, "KBr": 0.05} # 0.1 mol/L NaCl, 0.05 mol/L KBr
    assert salt2ions(solution_dict, volume=2, unit='mol') == {'Na+': 0.2, 'Cl-': 0.2, 'K+': 0.1, 'Br-': 0.1}, "Salt2Ions: Test_mol_unit failed"
    
def test_g_unit():
    solution_dict = {"NaCl": 0.1, "KBr": 0.05} # 0.1 g/L NaCl, 0.05 g/L KBr
    assert salt2ions(solution_dict, volume=2, unit='g') == {'Na+': 4.597953856, 'Cl-': 7.090000000000001, 'K+': 3.9098300000000004, 'Br-': 7.9904}, "Salt2Ions: Test_g_unit failed"

def test_invalid_volume():
    solution_dict = {"NaCl": 0.1, "KBr": 0.05}
    try:
        salt2ions(solution_dict, volume=0)
    except ValueError as e:
        assert "{}".format(e) == "Volume must be positive.", "Salt2Ions: invalid volume failed"
        

#----------------------------- Test make_solution() ----------------------------
def test_make_solution():
    ions_in_solution = {"K+": 0.5, "Cl-": 0.6, "Br-": 0.1, "SO4(2-)": 0.5 }
    forbidden_ions = ['NO3(-)']
    volume = 10
    expected_result = {'KH2PO4': 15.6997161195170, 'MnCl2': 10.6491996897038, 'KBr': 1.48931592911494, 'MgSO4': 6.26514741400849}
    assert make_solution(ions_in_solution, forbidden_ions, volume) == approx(expected_result, 1e-3), "Test make_solution failed"
#----------------------------- Test find_acid() ----------------------------

def test_find_acid():
    pKa_values={
    "H3PO4": [2.12,7.21,12.32],
    "H3BO3":[9.24,12.4,13.3],
    "HNO3":[-1.4],
    "H2SO4": [-3,1.9],
    "HCl" : [-6.3],
    "NH4" : [9.3],}

    Test_concentration_of_solution = {
        "Ca": float(0),
        "Mg": float(0),
        "K": float(0),
        "PO4": float(0),
        "BO3":float(0),
        "Mn": float(0),
        "Zn": float(0),
        "Cu": float(0),
        "Fe(3+)": float(0),
        "NO3": float(0),
        "HSO4": float(0.02),
        "Cl" : float(0),
        "NH4" : float(0)}
    
    highest_existing_charge_of_compounds = {'H3PO4': 0, 'H3BO3': 0, 'H2SO4': 0, 'NH4': 1}
    
    expected_dict=({'PO4': 3, 'BO3': 3, 'HSO4': 1, 'NH4': 0},
    {'PO4': [2.12, 7.21, 12.32],
    'BO3': [9.24, 12.4, 13.3],
    'HSO4': [-3, 1.9],
    'NH4': [9.3]},{'PO4': 0, 'BO3': 0, 'HSO4': 0, 'NH4': 1})
    assert find_acid(Test_concentration_of_solution,pKa_values,highest_existing_charge_of_compounds) == expected_dict

#----------------------------- Test pH_approximation() ----------------------------
def test_pH_approximation():
    pKa_values={
    "H3PO4": [2.12,7.21,12.32],
    "H3BO3":[9.24,12.4,13.3],
    "HNO3":[-1.4],
    "H2SO4": [-3,1.9],
    "HCl" : [-6.3],
    "NH4" : [9.3],}
    
    Test_concentration_of_solution = {
        "Ca": float(0),
        "Mg": float(0),
        "K": float(0),
        "PO4": float(0),
        "BO3":float(0),
        "Mn": float(0),
        "Zn": float(0),
        "Cu": float(0),
        "Fe(3+)": float(0),
        "NO3": float(0),
        "HSO4": float(0.02),
        "Cl" : float(0),
        "NH4" : float(0)}
    
    result = pH_approximation(Test_concentration_of_solution,25)
    lower_bound = 6
    upper_bound = 7.5
    assert lower_bound <= result <= upper_bound, f"Test failed: {result} is not within the range {lower_bound} to {upper_bound}"

#----------------------------- Test Refill_of_container() ----------------------------
def test_Refill_of_container():
    concentration_of_ions = {"Na+": 0.1, "Cl-": 0.1, "K+": 0.05, "NO3(-)": 0.05}
    optimal_ion_concentrations = {"Na+": 0.2, "Cl-": 0.2, "K+": 0.1, "NO3(-)": 0.1}
    assert Refill_of_container(concentration_of_ions, optimal_ion_concentrations, 5) == {'Na+': 0.1, 'Cl-': 0.1, 'K+': 0.05, 'NO3(-)': 0.05}, "Refill_of_container: Test failed"

#----------------------------- Test generation_of_pH_list() ----------------------------
def test_generation_of_pH_list():
      Test_concentrations_list_of_solution =[{
          "Ca": float(0),
          "Mg": float(0),
          "K": float(0),
          "PO4": float(0),
          "BO3":float(0),
          "Mn": float(0),
          "Zn": float(0),
          "Cu": float(0),
          "Fe(3+)": float(0),
          "NO3": float(0),
          "HSO4": float(0.02),
          "Cl" : float(0),
          "NH4" : float(0)},{
          "Ca": float(0),
          "Mg": float(0),
          "K": float(0),
          "PO4": float(0),
          "BO3":float(0),
          "Mn": float(0),
          "Zn": float(0),
          "Cu": float(0),
          "Fe(3+)": float(0),
          "NO3": float(0),
          "HSO4": float(0.02),
          "Cl" : float(0),
          "NH4" : float(0)}]
      temperature = 25
      plant = "Eggplant"
      list_of_pH,exceeded_days_list=generation_of_pH_list(Test_concentrations_list_of_solution,temperature,plant)
      for i in range (len(list_of_pH)):
          assert 6.0<=list_of_pH[i]<= 8.0, "generation_of_pH_list: Test failed"
      assert type(exceeded_days_list) == list, "generation_of_pH_list: Test failed"