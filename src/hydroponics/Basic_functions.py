"""
This file contains the most basic functions used in the project.
In particular, the file contains functions to:
- Import user data from an Excel file
- Calculate the molar mass of a salt
- Get the solubility product constant (Ksp) and solubility product (Q) of a salt
- Convert salt concentrations to ion concentrations
- Make a solution given the ion concentration wanted
"""

#Imports
import re
import os
import csv
import pandas as pd
from sympy import symbols, Eq, solve


# ----- Import User Data from Excel file -------------

def import_solution_data(solution_name: str) -> dict:
    """
    Import user data from the Excel file and returns it as a dictionary.

    Args:
        solution_name (str): Name of the column in the Excel file.

    Returns:
        dict: Dictionary containing the concentration of the ions [g/L] in the solution.
    """
    # Read the Excel file
    file_name = "data/UserData.xlsx"
    df = pd.read_excel(file_name, sheet_name="My Solution", skiprows=1)
    # Create a dictionary using zip and dictionary comprehension
    ion_solution_dict = dict(zip(df['Ions'], df[solution_name]))
    return ion_solution_dict

def predefined_solutions(plant:str ) -> dict:
    """
    Import user data from the Excel file and returns it as a dictionary.

    Args:
        plant (str): Name of the plant. Can either be 'Eggplant', 'Tomato' or 'Cucumber'.

    Returns:
        dict: Dictionary containing the concentration of the ions [g/L] in the solution.
    """
    available_plants = ['Eggplant', 'Tomato', 'Cucumber']
    if plant not in available_plants:
        raise ValueError(f"Plant {plant} not found. Available plants are {available_plants}.")
    else:
        # Read the Excel file
        file_name = "data/UserData.xlsx"
        df = pd.read_excel(file_name, sheet_name="Optimal Solution", skiprows=0)
        # Create a dictionary using zip and dictionary comprehension
        ion_solution_dict = dict(zip(df['Formula'], df['c [mol/L] '+plant]))
        return ion_solution_dict

def import_plant_data(plant_name:str) -> dict:
    """_summary_

    Args:
        plant (str): name of the column where the data is located
        
    Returns:
        dict: dictionary containing the needs of the plant for each ion [g] for a full growth cycle
    """
    # Read the Excel file
    file_name = "data/UserData.xlsx"
    df = pd.read_excel(file_name, sheet_name="My plant", skiprows=1)
    # Create a dictionary using zip and dictionary comprehension
    plant_dict = dict(zip(df['Ions'], df[plant_name]))
    return plant_dict


def load_from_data(file_name):
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # Construct the absolute path to the CSV file
    csv_path = os.path.join(current_dir, '..\\..\\data', file_name)
    return csv_path


# ----- Molar mass calculator ------------------------

def get_atom_mass(atom_name: str) -> float:
    """
    Gets the atomic mass of the atom from a CVS file

    Args:
        atom_name (str): Name of the atom, i.e. 'H', 'O', 'C', etc.

    Returns:
        float: atomic mass of the atom in g/mol
    """
    # Define the name of the CSV file
    data_file = load_from_data("molar_mass.csv") #Check path to CSV file
    with open(data_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Atom'] == atom_name:
                return float(row['Molar mass [g/mol]'])

def get_molar_mass(salt: str) -> float:
    """
    Returns the molar mass of a salt in g/mol.
    
    Args:
    - salt (str): The chemical formula of the salt.
        Handels chemical formulas of type "Ca(NO3)2", "Ca(2+)(NO3-)2", "Ca2(NO3)2", "Ca(NO3)2(2+)"
    """
    #Check for special characters
    def contains_special_characters(input_string:str):
        # Define a regular expression pattern to match special characters
        pattern = re.compile(r'[!@#$%^&*_=\[\]{};\'\\:"|,.<>\/?]')
        # Use search method to find if any special characters exist in the input string
        if pattern.search(input_string):
            return True
        else:
            return False

    def molar(molecule:str):
        
        if contains_special_characters(molecule):
            raise ValueError("Invalid input. The formula of the molcule can only contain letters,numbers, parentheses and '+' or '-' signs.")
        
        current_count = ""
        current_element = ""
        i=0
        molar_mass = 0
        #Test for charges and numbers
        while molecule[-1] == "+" or molecule[-1] == "-":
            molecule = molecule[:-1]
            if len(molecule) == 0:
                break
        if molecule.isnumeric():
            return 0   
    
        while i < len(molecule):
            if i<len(molecule)-3:
                if molecule[i].isupper() and molecule[i+1].islower() and molecule[i+2].isnumeric() and molecule[i+3].isnumeric():
                    current_element = molecule[i]+molecule[i+1]
                    current_count = molecule[i+2]+molecule[i+3]
                    i+=4
                    molar_mass += get_atom_mass(current_element)*int(current_count)
                    continue
                
            if i<len(molecule)-2:
                if molecule[i].isupper() and molecule[i+1].islower() and molecule[i+2].isnumeric():
                    current_element = molecule[i]+molecule[i+1]
                    current_count = molecule[i+2]
                    i+=3
                    molar_mass += get_atom_mass(current_element)*int(current_count)
                    continue
                    
                if molecule[i].isupper() and molecule[i+1].islower() and molecule[i+2].isalpha():
                    current_element = molecule[i]+molecule[i+1]
                    current_count = 1
                    i+=2
                    molar_mass += get_atom_mass(current_element)*int(current_count)
                    continue
                
                if molecule[i].isupper() and molecule[i+1].isnumeric() and molecule[i+2].isnumeric():
                    current_element = molecule[i]
                    current_count = molecule[i+1]+molecule[i+2]
                    i+=2
                    molar_mass += get_atom_mass(current_element)*int(current_count)
                    continue
            if i<len(molecule)-1:
                if molecule[i].isupper() and molecule[i+1].isnumeric():
                    current_element = molecule[i]
                    current_count = molecule[i+1]
                    i+=2
                    molar_mass += get_atom_mass(current_element)*int(current_count)
                    continue
                elif molecule[i].isupper() and molecule[i+1].isupper():
                    current_element = molecule[i]
                    current_count = 1
                    i+=1
                    molar_mass += get_atom_mass(current_element)*int(current_count)
                    continue
            
            if i == len(molecule)-2:
                if molecule[i].isupper() and molecule[i+1].islower():
                    current_element = molecule[i]+molecule[i+1]
                    current_count = 1
                    i+=2
                    molar_mass += get_atom_mass(current_element)*int(current_count)
                    continue
                if molecule[i].isupper() and molecule[i+1].isupper():
                    current_element = molecule[i]
                    current_count = 1
                    i+=1
                    molar_mass += get_atom_mass(current_element)*int(current_count)
                    continue
                if molecule[i].isupper() and molecule[i+1].isnumeric():
                    current_element = molecule[i]
                    current_count = molecule[i+1]
                    i+=2
                    molar_mass += get_atom_mass(current_element)*int(current_count)
                    continue  
            if i == len(molecule)-1:
                current_element = molecule[i]
                current_count = 1
                i+=1
                molar_mass += get_atom_mass(current_element)*int(current_count)
                continue
            if molar_mass >=100000:
                break

        return molar_mass
    
    #Take care of brakets
    M = 0    
    while "(" in salt:
        left = salt.index("(")
        right = salt.index(")")
        substing = salt[left+1:right]

        if right != len(salt)-1:
            if salt[right+1].isnumeric():
                M += int(salt[right+1])*molar(substing)
                salt = salt[:left] + salt[right+2:]
            else:
                M += molar(substing)
                salt = salt[:left] + salt[right+1:]
        else:
            M += molar(substing)
            salt = salt[:left] + salt[right+1:]
            
    total_molar_mass = M + molar(salt)
    return total_molar_mass



#------ Basic Solubility functions -----------------------------
#Dictionaries used to handle salts with multiple ions, extend dictionaries if needed
salt2nbIons = {
    "Ca(NO3)2": [1,2],
    "MgSO4": [1,1],
    "KNO3": [1,1],
    "KH2PO4": [1,1],
    "H3BO3": [1],
    "MnCl2": [1,2],
    "ZnSO4": [1,1],
    "CuSO4": [1,1],
    "(NH4)6Mo7O24": [6,1],
    "C10H12FeN2NaO8": [1,1],
    "(NH4)H2PO4" : [1,1],
    "NaCl": [1,],
    "NaOH": [1,1],
    "Na2CO3": [2,1],
    "Na2SO4": [2,1],
    "NaHCO3": [1,1],
    "Na2S": [2,1],
    "KCl": [1,1],
    "KOH": [1,1],
    "K2SO4": [2,1],
    "K2CO3": [2,1],
    "KHCO3": [1,1],
    "CaCl2": [1,2],
    "Ca(OH)2": [1,2],
    "CaCO3": [1,1],
    "MgCl2": [1,2],
    "Mg(OH)2": [1,2],
    "MgCO3": [1,1],
    "FeSO4": [1,1],
    "FeCl3": [1,3],
    "AlCl3": [1,3],
    "KBr" : [1,1]

    
}
dict_salts_trad = {
    "Ca(NO3)2": {"Ca(2+)": 1, "NO3(-)": 2},
    "MgSO4": {"Mg(2+)": 1, "SO4": 1},
    "KNO3": {"K+": 1, "NO3(-)": 1},
    "KH2PO4": {"K+": 1, "H2PO4": 1},
    "H3BO3": {"B": 1},
    "MnCl2": {"Mn(2+)": 1, "Cl-": 2},
    "ZnSO4": {"Zn(2+)": 1, "SO4": 1},
    "CuSO4": {"Cu(2+)": 1, "SO4": 1},
    "(NH4)6Mo7O24": {"NH(4+)" : 6, "Mo7O24": 1},
    "Fe(III)EDTANa": {"Fe(3+)": 1, "Na+": 1, "EDTA": 1},
    "(NH4)H2PO4" : {"NH4+": 1, "H2PO4": 1},
    "NaCl": {"Na+": 1, "Cl-": 1},
    "NaOH": {"Na+": 1, "OH-": 1},
    "Na2CO3": {"Na+": 2, "CO3": 1},
    "Na2SO4": {"Na+": 2, "SO4": 1},
    "NaHCO3": {"Na+": 1, "HCO3": 1},
    "Na2S": {"Na+": 2, "S(2-)": 1},
    "KCl": {"K+": 1, "Cl-": 1},
    "KOH": {"K+": 1, "OH-": 1},
    "K2SO4": {"K+": 2, "SO4": 1},
    "K2CO3": {"K+": 2, "CO3": 1},
    "KHCO3": {"K+": 1, "HCO3": 1},
    "CaCl2": {"Ca(2+)": 1, "Cl-": 2},
    "Ca(OH)2": {"Ca(2+)": 1, "OH-": 2},
    "CaCO3": {"Ca(2+)": 1, "CO3": 1},
    "MgCl2": {"Mg(2+)": 1, "Cl-": 2},
    "Mg(OH)2": {"Mg(2+)": 1, "OH-": 2},
    "MgCO3": {"Mg(2+)": 1, "CO3": 1},
    "FeSO4": {"Fe(2+)": 1, "SO4": 1},
    "FeCl3": {"Fe(3+)": 1, "Cl-": 3},
    "AlCl3": {"Al(3+)": 1, "Cl-": 3},
    "KBr" : {"K+": 1, "Br-": 1}

    
}


# Get the solubility constant Ksp of a salt
def get_Ksp(salt_name: str) -> float:
    """
    Access the solubility product constant (Ksp) of a salt based on its name. 
        Uses a salt2nbIons dictionary to find the number of ions in a salt.

    Args:
        salt_name (str): The name of the salt. 

    Returns:
        float: The solubility product constant (Ksp) of the salt.
    """
    solubility_file = load_from_data("solubility.csv")
    df_solubility = pd.read_csv(solubility_file)
    
    row = df_solubility.loc[df_solubility["Formula"] == salt_name].values.tolist() # [[name, formula, value]]
    Ksp = 0
    if row:
        solubility = float(row[0][2]) *10 #go from g/100mL to g/L
        mol_sol = solubility/get_molar_mass(salt_name) #mol/L
        
        #Ksp = n^n * m^m * mol_sol^(n+m) for salt of type nXmY
        ions = salt2nbIons[salt_name]
        if len(ions) <=1:
            Ksp = mol_sol
        else: 
            n = ions[0]
            m = ions[1]
            Ksp = (n**n)*(m**m)*(mol_sol**(n+m))
    return Ksp 

# Get the solubility product Q of a salt
def get_Q_solubility(salt_name: str, ions_in_solution: dict) -> float:
    '''
    Returns the solubility product of a salt
    
    Args:
        salt_name (str): name of the salt
        ions_in_solution (dict): dictionary with keys as ions and values as the concentration in mol/L
    
    Returns:
        float: solubility product Q
    '''
    Q = 1
    i=0
    for ion in dict_salts_trad[salt_name]:
        if ion in ions_in_solution:
            Q *= ions_in_solution[ion]**salt2nbIons[salt_name][i]
            i+=1
    return Q




#-----------Basic ion-salt functions----------------------------

# Convert salt concentrations to ion concentrations
def salt2ions(solution: dict, volume: float = 1, unit: str = "g") -> dict:
    """
    Convert salts to ions based on their concentrations and volume. Concentrations are in g/L by default 
        but can also be given in mol/L by specifying 'unit' as 'mol'.
        A 'dict_salts_trad' dictionary is used to convert salt names to ions.

    Args:
        solution (dict): A dictionary containing salt names as keys and concentrations as values.
        volume (float, optional): Volume of the solution. Defaults to 1.
        unit (str, optional): Unit of concentration. Defaults to "g". Options are "g" or "mol".

    Returns:
        dict: A dictionary containing ions and their concentrations [g/L] in the solution (volume =1), their quantity [g] if volume > 1

    Raises:
        ValueError: If the volume is non-positive.
    """
    if volume <= 0:
        raise ValueError("Volume must be positive.")
    if unit == "mol":
        ions = {}
        for salt in solution:
            if salt in dict_salts_trad:
                for ion in dict_salts_trad[salt].keys():
                    if ion in ions:
                        ions[ion] += dict_salts_trad[salt][ion] * solution[salt]
                    else:
                        ions[ion] = dict_salts_trad[salt][ion] * solution[salt]
            else:
                raise ValueError(f"Salt {salt} not found in the 'dict_salts_trad' dictionary.")
            
        ions_in_solution = {n: volume * ions[n] for n in ions.keys()}    
        return ions_in_solution
    
    elif unit == "g":
        salts = {salt: mass/get_molar_mass(salt) for salt, mass in solution.items()}
        ions = {}
        for salt in salts:
            if salt in dict_salts_trad:
                for ion in dict_salts_trad[salt].keys():
                    if ion in ions:
                        ions[ion] += dict_salts_trad[salt][ion] * solution[salt]
                    else:
                        ions[ion] = dict_salts_trad[salt][ion] * solution[salt]
            else:
                raise ValueError(f"Salt {salt} not found in the 'dict_salts_trad' dictionary.")
        ions_in_solution = {ion: float(get_molar_mass(ion)) * float(volume) * ions[ion] for ion in ions.keys()}
        return ions_in_solution
    else:
        raise ValueError("'Unit' must be 'g' or 'mol'.")

#Make a solution given the ion concentration wanted
def make_solution (ions_in_solution :dict, forbidden_ions:list, volume:float, )->dict:
    '''
    Returns how much of each salt [g] to add to a solution of certain volume [L]
    to obtain a certain concentration of ions [g/L]
    
    Args:
        ions_in_solution (dict): dictionary with keys as ions and values as the concentration in g/L
        forbidden_ions (list): list of ions that cannot be in the solution
        volume (float): volume of the solution in L
    
    Returns:
        dict: dictionary with keys as salt names and values as the amount of salt needed in g
    '''
    
    if set(ions_in_solution.keys()).intersection(forbidden_ions) != set() :
        raise ValueError("Forbidden ions are in the solution")
    
    molar_ions = {ion: ions_in_solution[ion]/get_molar_mass(ion) for ion in ions_in_solution}
    # Define variables
    possible_salts = []
    for salt in dict_salts_trad.keys():
        for ion in dict_salts_trad[salt]:
            if (ion in molar_ions) and (salt not in possible_salts) and (len(set(dict_salts_trad[salt].keys()).intersection(forbidden_ions)) == 0):
                possible_salts.append(salt)
    
    for salt in possible_salts[:]:
        if get_Ksp(salt) <= get_Q_solubility(salt, molar_ions):
            possible_salts.remove(salt)
    
    #NB variables == NB equations
    final_salts = []
    nb_eq = len(molar_ions.keys())
    for ion in molar_ions.keys():
        for salt in possible_salts:
            if ion in dict_salts_trad[salt] and salt not in final_salts:
                final_salts.append(salt)
                break
                
    variables = symbols(final_salts)
        
    #Set up equations
    equations = []
    for ion in molar_ions.keys():
        lhs = 0
        rhs = molar_ions[ion] * volume
        for salt in final_salts:
            if ion in dict_salts_trad[salt]:
                lhs += dict_salts_trad[salt][ion] * symbols(salt)
        equation = Eq(lhs, rhs)
        equations.append(equation)     
    
    #Solve equations
    solution = solve(equations, variables)
    mass_salts = {salt: solution[symbols(salt)]*get_molar_mass(salt) for salt in final_salts}
        
    return mass_salts  

