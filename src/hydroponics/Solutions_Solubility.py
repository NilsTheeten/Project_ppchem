"""
This file contains the more advanced functions on solutions and solubility used in the project.
In particular, the file contains functions to:
- Check the solubility of a solution
- Analyse the nutriments in the solution
- Update the solution after 1 day of growth
- Plot the evolution of the solution
"""

#Imports
import pandas as pd
import math
import matplotlib.pyplot as plt
import os
import numpy as np
from .Basic_functions import get_molar_mass, get_Ksp, get_Q_solubility, salt2ions, dict_salts_trad

# ----------------- Analyse the solution -----------------

#Check the solubility of the solution
def check_solubility(salts_dict: dict, input_type: str = "salt", output_type: str = "bool") -> bool:
    """
    Check if the salts mixture is soluble.

    Args:
        salts_dict (dict): Dictionary with keys as salt names and values as concentrations [g/L].
        input_type (str): Type of input data, either "salt" or "ion".
        output_type (str): Type of output data, either "bool", "analysis", or "update".

    Returns:
        bool or str: True if salts are soluble (if output_type is "bool").
                     Analysis of precipitated salts or indication of solubility (if output_type is "analysis").
    """
    # Validate input and output types
    valid_input_types = {"salt", "ion"}
    valid_output_types = {"bool", "analysis", "update"}
    if input_type not in valid_input_types:
        raise ValueError("Invalid input type. Please choose either 'salt' or 'ion'.")
    if output_type not in valid_output_types:
        raise ValueError("Invalid output type. Please choose either 'bool', 'analysis', or 'update'.")
    
    #Handle type of input and convert to mol/L
    if input_type == "salt":
        salts_dict_molar= {salt: concentration / get_molar_mass(salt) for salt, concentration in salts_dict.items()}
        ions = salt2ions(salts_dict_molar, volume = 1)
    if input_type == "ion":
        ions = {ion: concentration / get_molar_mass(ion) for ion, concentration in salts_dict.items()}
        
    #Initialize variables
    soluble = True
    precipitate = []
    salts = dict_salts_trad.keys()
    
    #Compare Q and Ksp for each salt is the Ksp value is provided
    for salt in salts:
        try:
            Ksp = get_Ksp(salt)
            Q = get_Q_solubility(salt, ions)
            if Q > Ksp and set(dict_salts_trad[salt].keys()).issubset(set(ions.keys())):
                soluble = False
                precipitate.append(salt)
        except:
            pass
            
    
    #Handle type of output
    if output_type == "bool":
        return soluble
    elif output_type == "analysis":
        if soluble:
            return "all salts are soluble"
        else:
            text = f"The following salts precipitate: "
            for salt in precipitate:
                text+=str(salt)+"    "
            return text
    elif output_type == "update":
        return precipitate
    
#analyse the nutriments in the solution
def analyse_nutriments(solution: dict, plant: dict, growth_time: float, volume: float, input_type_solution: str= 'salt') -> list:
    """
    Returns the number of days a plant can grow with the given solution.

    Args:
        solution (dict): A dictionary containing salts or ions and their concentrations in the solution.
        input_type (str): Type of input data, either "salt" or "ion".
        plant (dict): A dictionary containing ions and their required quantity for plant growth.
        growth_time (float): Expected growth time of the plant [days].
        volume (float): Volume of the solution [L].
        *Note: the unit of solution and plant must be the same. (either mol/L or g/L)

    Returns:
        list: A list containing three elements:
            - bool: True if the solution contains enough nutriments for the plant, False otherwise.
            - int: Minimum days of growth achievable with the given solution.
            - str: Ion that limits the plant growth.

    Raises:
        ValueError: If the volume or growth time is non-positive.
    """
    #Check validity of Args
    if volume <= 0:
        raise ValueError("Volume must be positive.")
    if growth_time <= 0:
        raise ValueError("Growth time must be positive.")
    if input_type_solution not in {"salt", "ion"}:
        raise ValueError("Invalid input type. Please choose either 'salt' or 'ion'.")
    
    #Initialisation
    if input_type_solution == "salt":
        ions = salt2ions(solution, volume=volume)
    if input_type_solution == "ion":
        ions = {ion: solution[ion]*volume for ion in solution.keys()}
        
    daily_plant_need = {ion: plant[ion]/growth_time for ion in plant.keys()}
    limiting_ion = None
    growth_limit = growth_time
    
    #Determine limiting ion, minimum days of growth and if growth time exceeds the minimum days
    for ion in ions:
        if ion in daily_plant_need:
            days = math.floor(ions[ion] / daily_plant_need[ion])
            if days < growth_limit:
                growth_limit = days
                limiting_ion = ion
    if set(plant.keys()).issubset(set(ions.keys())):
        return [growth_limit == growth_time, growth_limit, limiting_ion]
    else:
        missing_ions = [ion for ion in plant.keys() if ion not in ions]
        return [False, 0, missing_ions]
   
#Check is enaugh nutriments are present in the solution
def check_supply_elements(ions_solution, plant) -> bool:
    for ion in plant.keys():
        if plant[ion] > ions_solution[ion]:
            return False
    return True



# ----------------- Evolution of the solution -----------------

#Update the solution after 1 day of growth
def update_sol(ions_solution: dict, plant: dict, volume: float) -> dict:
    """
    updates the salts in solutions after 1 day of growth and checks the solubility of the new solution
    
    Args:
        ions_solution: dictionary with keys as ions and values as the amount of ions in the solution [g/L]
        plant: dictionary with keys as ions and values as the amount of ions needed for 1 day for the plant [g]
        
    Returns:
        dictionary: updated ions_solution after 1 day of growth and checking the solubility
    """
    volume_plant = {ion: plant[ion]/volume for ion in plant.keys()}
    for ion in volume_plant:
        if ions_solution[ion] <= volume_plant[ion]:  
            ions_solution[ion] = 0
        else:      
            ions_solution[ion] -= volume_plant[ion]
    
    if check_solubility(ions_solution, input_type="ion"):
        return ions_solution  
    else: 
        unsoluble_ions = check_solubility(ions_solution, input_type ="ion", output_type = "update")
        for ion in unsoluble_ions:
            ions_solution[ion] = 0
        return ions_solution
    
# Evolution of the concentration as the plant grows (internal function)
def data4graph(solution: dict, volume: float, plant: dict, growth_time: float) -> list:
    """
    Creates a dictionary with the data needed to plot the graph
    
    Args:
        solution (dict): Initial concentration [g/L] of the ions in the solution.
        volume (float): Volume of the solution [L].
        plant (dict): Dictionary containing required amount of ions for the plant growth.
        growth_time (float): Expected growth time of the plant [days].
    
    Returns:
        list: A list containing two elements:
            - list: A list of days. [0,1,2,3,4,5,6,...]
            - list: A list of dictionaries with the concentration of ions in the solution for each day.
    
    """
    #Initialisation:
    daily_need_plant = {ion: plant[ion]/growth_time for ion in plant.keys()}
    data = [[],[]] #data = [[0,1,2,3,4,5,6,...],[{"Na",0.1,"K",0.2,...}, {"Na": 0.05, "K": 0.1,...},...]]
    i=0
    data[0].append(i)
    data[1].append(solution.copy())
    
    #Loop trough further values
    for i in range(1,growth_time+1):
            if check_supply_elements(solution, daily_need_plant):
                solution = update_sol(solution, daily_need_plant, volume)
                data[0].append(i)
                data[1].append(solution.copy())
            else:
                data[0].append(i)
                data[1].append(solution.copy())
        
    return data
    
#List of colors for the graph
python_colors = ['b', 'g', 'c', 'm', 'y', 'k',
                 'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan',
                 'mediumblue', 'darkorange', 'limegreen', 'indianred', 'violet', 'sienna', 'deepskyblue', 'peru', 'gold']

#Plot the evolution of the solution
def plot_graph(solution: dict, input_type:str, plant:dict, growth_time:float, volume:float = 1, ions_of_interest: list = "all"):
    """
    Creates graph of salts in hydroponic solution

    Args:
        salts (dict): Initial concentration [g/L] of the ions in the solution.
        input_type (str): Type of input data, either "salt" or "ion".
        plant (dict): the plant requirements to fully grow [g].
        growth_time (float): Expected growth time of the plant [days].
        volume (float, optional): Volume of the solution [L]. Defaults to 1.
        ions_of_interest (list, optional): list of ions to plot. Defaults to "all". 
            Elements must be part of the keys of solution.
    
    Returns:
        None, saves the graph as a .png file in the download folder.
    """
    
    #Initialise the figure and aesthetics
    plt.figure(figsize=(12, 6), dpi = 500)
    plt.title('Evolution of the Salts in hydroponic solution', fontsize=16, weight='bold')
    plt.xlabel(f'Time [days]', fontsize=14)
    plt.ylabel('Concentration of the salt [g/L]', fontsize=14)
    plt.grid(False)
    plt.gca().set_facecolor('#f9f9f9')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    # Setting y-axis to log scale
    #plt.yscale('log')
    
    
    #xlength = analyse_nutriments(solution, plant, growth_time, volume, input_type_solution = 'ion')[1]
    
    #Handle Input type
    if input_type == "salt":
        initial_ion_solution = salt2ions(solution, volume)
    else:
        initial_ion_solution = solution.copy()
        
    #add the growth limit
    analysis = analyse_nutriments(initial_ion_solution, plant, growth_time, volume, input_type_solution = 'ion')
    if analysis[1] != growth_time:
        plt.axvline(x=analysis[1], color='r', linestyle='--', label=f'Growth limit: insufficient {analysis[2]}')
        
    #Plot the data for the ions of interest
    i = 0 #handle the colors    
    data = data4graph(initial_ion_solution, volume, plant, growth_time)
    for ion in initial_ion_solution.keys():
        if ion in ions_of_interest or ions_of_interest == "all":
            x = data[0]
            y = []
            for j in range(len(x)):
                y.append(data[1][j][ion])
            plt.plot(x, y, label = ion, color = python_colors[i],alpha=0.8, linewidth=1.5, linestyle='-', marker='o', markersize=3)
            i+=1
            
    
    plt.legend(loc='best')
    
    #Save Graph to the current directory
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_name = "graph_"
    for ion in ions_of_interest:
        file_name += str(ion) + "_"
    file_path = os.path.join(current_dir, file_name)
    plt.savefig(file_path + ".png", format='png')  # Save as a PNG file for matplotlib
    
 