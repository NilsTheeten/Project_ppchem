# Importing functions from Basic_functions.py file

import basic_functions as bf


#--------------------------- Test get_molar_mass() ------------------------------
def test_molar_mass ():
    mol = ["Ca(NO3)2", "Ca(2+)(NO3)2(-)", "Ca++(NO3)2", "Ca(NO3)NO3"]
    for i in range(len(mol)):
        assert round(bf.get_molar_mass(mol[i]),3) == 164.086, "Test failed: did not understand {mol[i]}"
        
    
test_molar_mass()


#--------------------------- Test get_Ksp() ------------------------------
def test_get_Ksp():
    list = ['KNO3', 'KH2PO4', 'MnCl2', 'NaCl', 'KCl', 'KOH', 'K2SO4', 'K2CO3', 'KHCO3', 'CaCl2', 'MgCl2', 'FeCl3', 'AlCl3', 'KBr']
    for i in range(len(list)):
        print(list[i])
        print(bf.get_Ksp(list[i]))

test_get_Ksp()
