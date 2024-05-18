"""This file contains tests for the functions in the Basic_functions.py file."""

# Importing functions from Basic_functions.py file
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from hydroponics import *

#--------------------------- Test get_molar_mass() ------------------------------
def test_molar_mass ():
    mol = ["Ca(NO3)2", "Ca(2+)(NO3)2(-)", "Ca++(NO3)2", "Ca(NO3)NO3"]
    for i in range(len(mol)):
        assert round(get_molar_mass(mol[i]),3) == 164.086, "Test molar mass failed: did not understand {mol[i]}"
           


#--------------------------- Test get_Ksp() ------------------------------
def test_get_Ksp():
    list = ['KNO3', 'KH2PO4', 'MnCl2', 'NaCl', 'KCl', 'KOH', 'K2SO4', 'K2CO3', 'KHCO3', 'CaCl2', 'MgCl2', 'FeCl3', 'AlCl3', 'KBr']
    Ksp_list = [9.76904463917891, 2.758051364759525, 810.1350827255483, 6.141365792880145, 21.04634685946477, 398.49994656470716, 1.0339299769044514, 2072.3420181206798, 11.330982570493006, 1210.091270423005, 754.4989632174183, 0, 3759.188606917454, 30.110339484562]
    for i in range(len(list)-1):
        assert get_Ksp(list[i]) == Ksp_list[i], f"Test_get_Ksp failed: Error for {list[i]}"
        
        

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
    ions_in_solution = {"K+": 0.5, "Cl-": 0.6, "Br-": 0.1, "SO4": 0.5 }
    forbidden_ions = ['NO3(-)']
    volume = 10
    expected_result = {'KH2PO4': 15.6997161195170, 'MnCl2': 10.6491996897038, 'KBr': 1.48931592911494, 'MgSO4': 6.26514741400849}
    assert make_solution(ions_in_solution, forbidden_ions, volume) == expected_result
    
    
    

    


    

