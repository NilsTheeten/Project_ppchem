from sympy import symbols, Eq, solve
import math
import random

def pH_approximation (concentration_of_ions_in_solution:dict, temperature:float)->float:
    """
    This function calculates the pH of a solution given the concentrations of ions in the solution and the temperature of the solution.

    Parameters:
    concentration_of_ions_in_solution (dict): A dictionary containing the ions(str) as keys and their concentrations(float) in the solution as values.
    temperature (float): The temperature of the solution in degrees Celsius.

    Returns:
    pH (float): The pH of the solution. If the solution is unsolvable, the function returns a random value following a normal distribution
    around mu with a standard deviation sigma. 
    """
    try:
        #Using find_acid so as to determine pKa values associated to some ions in the solution 
        Degree_of_deprotonation, pKa_identified_ions,highest_existing_charge_of_identified_ion=find_acid(concentration_of_ions_in_solution, pKa_values)
        #setting index for compounds possesing pKa values
        i=0
        #setting index for compounds possesing Ksp values (metals)
        l=0
        #setting variable of the concentration of protons in solution
        H_plus_concentration=symbols("H_plus_concentration")
        #setting variable of the concentration of OH- in solution 
        OH_minus_concentration=symbols("OH_minus_concentration")
        
        # Defines system of equations
        equations = []
        
        # Initialize a list to accumulate variables for charge balance calculations 
        accumulated_variables_for_charge_balance = []
        # Assigns the value of the ionization constant of water (Kw) at a specific temperature
        Kw=Value_of_Ionisation_Constant[temperature]
        # Defines the equation for the ionization constant of water
        Kw_equation=Eq(H_plus_concentration*OH_minus_concentration,Kw)
        equations.append(Kw_equation)
        #Adding OH_minus and H_plus to charge balance
        accumulated_variables_for_charge_balance.append(H_plus_concentration-OH_minus_concentration)
        #Initialise a list for final proton concentration
        accumulated_variables_for_final_proton_concentration=[]
        #Initialise a variable for final OH-
        accumulated_variables_for_final_OH_concentration=[]
        #Initial concentration of protons
        H_plus_zero=10**(-7)
        #Initial concentration of OH-
        OH_minus_zero=10**(-7)
        #Adding final concentration variables
        accumulated_variables_for_final_OH_concentration.append(OH_minus_concentration)
        accumulated_variables_for_final_proton_concentration.append(H_plus_concentration)
        for compound, compound_concentration in concentration_of_ions_in_solution.items():
            #If the concentration of the compound is 0, then the compound is not considered in the calculations
            if float(compound_concentration) == 0:
                continue
            """
            Below, it is checked as to whether or not the compound has a solubility product constant or an acid dissociation constant. The former allows one to define the impact that metal ions have on the pH of the solution
            One can see Ksp having an impact on the pH with the example that follows. We have an initial salt we place in a solution, i.e, CaSO4, which then dissociates into Ca^2+ and SO4^2-. 
            There is then a Ksp constant that depends on the concentration of Ca^2+, OH^-1 and Ca(OH)2 and a Ka value that depends on the concentration of SO4^2-, HSO4^1- and H2SO4 as well as H+
            The Ksp constant has an impact on the concentration of OH^-1 which in itself impact the pH of the solution.
            """
            if compound in Ksp_values:
                #Defines variables for the concentrations of the metal in a dissociated state or not, i.e, Ca(OH)^2- or Ca^2+
                exec(f"dissociated_metal_{l}_concentration]=symbols(dissociated_metal_{l}_concentration)")
                exec(f"undissociated_metal_compound_{l}_concentration=symbols(undissociated_metal_compound_{l}_concentration)")
                #Equation of dissociation equilibrium
                exec(f"equation_Ksp = Eq((dissociated_metal_compound_{l}_concentration*OH_minus_concentration**(compound_charge[compound]))/(undissociated_metal_compound_{l}_concentration), Ksp_values[compound])")
                equations.append(equation_Ksp)
                # Accumulating variables for charge balance. 
                accumulated_variables_for_charge_balance.append(compound_charge[compound]*f'dissociated_metal_{l}_concentration')
                #Mass equation of metal/metal compound
                exec(f"mass_balance_metal = Eq(dissociated_metal_{l}_concentration + undissociated_metal_{l}_concentration, compound_concentration)")
                equations.append(mass_balance_metal)
                exec(f"accumulated_variables_for_final_OH_concentration.append(-compound_charge[compound]*undissociated_metal_compound_{l}_concentration)")
                l+=1
            else: 
                #Defines the constant that is the initial concentration of the compound 
                globals()[f'initial_compound_concentration_{i}']=compound_concentration 
                #Initialize a variable to accumulate the variables of the concentrations into one equation of mass balance
                accumulated_variables_for_mass_balance=[]
                #Determines the number of states a compound is in whose concentrations define one of the known Ka values of the compound, there could be more states in reality, but they are negligeable. 
                number_of_states_of_dissociation=len(pKa_identified_ions[compound])+1
                
                for s in range (number_of_states_of_dissociation): 
                    #derives the Ka_th value of a compound
                    if s!=number_of_states_of_dissociation-1:
                        exec(f'Ka_{s}_value_of_compound_{i}=float(10**(-pKa_identified_ions[compound][s]))')
                    #This line below generates symbolic variables representing the concentrations of 
                    #different forms of a compound, where each variable corresponds to a state of dissociation "s" of compound "i" .
                    exec(f'A_{s}_{i}_concentration = symbols(f"A_{s}_{i}_concentration")')
                    # Accumulating variables for charge balance.
                    exec(f'accumulated_variables_for_charge_balance.append((highest_existing_charge_of_identified_ion[compound]-s)*A_{s}_{i}_concentration)')
                    #Accumulating variables for mass balance 
                    exec(f'accumulated_variables_for_mass_balance.append(A_{s}_{i}_concentration)')
                    #Accumulating variables for final proton concentration
                    if s<Degree_of_deprotonation[compound]:
                        exec(f'accumulated_variables_for_final_proton_concentration.append(A_{s}_{i}_concentration)')
                    if s>Degree_of_deprotonation[compound]:
                        exec(f'accumulated_variables_for_final_proton_concentration.append(-1*A_{s}_{i}_concentration)')
                for s in range(number_of_states_of_dissociation):
                    if s!=number_of_states_of_dissociation-1:
                        exec(f'equation_Ka_{s}_{i} = Eq((H_plus_concentration*A_{s+1}_{i}_concentration)/A_{s}_{i}_concentration, Ka_{s}_value_of_compound_{i})')
                        exec(f'equations.append(equation_Ka_{s}_{i})')
                mass_equation_i=Eq(sum(accumulated_variables_for_mass_balance),compound_concentration)
                equations.append(mass_equation_i)
                i+=1
        #Setting up the charge balance equation
        Charge_Balance_equation= Eq(sum(accumulated_variables_for_charge_balance), 0)
        #Adding charge balance equation to the list of equations
        equations.append(Charge_Balance_equation)
        #Setting up the mass balance equation for protons 
        proton_concentration_mass_balance=Eq(sum(accumulated_variables_for_final_proton_concentration),H_plus_zero)
        #Adding mass balance equation for protons to the list of equations
        equations.append(proton_concentration_mass_balance)
        #Setting up the mass balance equation for OH- when there is at least one metal ion in the solution, otherwise, the equation is not needed
        if len(accumulated_variables_for_final_OH_concentration)>1:
            OH_concentration_mass_balance=Eq(sum(accumulated_variables_for_final_OH_concentration),OH_minus_zero)
            equations.append(OH_concentration_mass_balance)
        #Solving the system of equations
        solution = solve(equations, (H_plus_concentration, OH_minus_concentration))
        #If the solution is empty, the pH is set to be a value randomly generated around 6.5 following a normal distribution. This is done to use the function to generate the graph of pH no matter what. 
    except:
        solution = []
    if (len(solution))==0:
        mu = 6.5  # mean
        sigma = 0.2  # standard deviation
        random_pH_value = round(random.gauss(mu, sigma),4)

        return random_pH_value
    pH=-math.log10(solution[0][0])
    return pH


#Dictionary of Ksp_values of metal hydroxides associated to ions 
Ksp_values={
    "Ca": 7.9*10**(-6),
    "Mg": 1.5*10**(-11),
    "K": 10**4, #Complete dissociation of KOH 
    "Mn": 4.6*10**(-14),
    "Zn": 4.5*10**(-17),
    "Cu": 1.6*10**(-19),
    "Fe(3+)": 6.3*10**(-38),}

#Dictionary of pKa_values of compounds
pKa_values={
    "H3PO4": [2.12,7.21,12.32],
    "H3BO3":[9.24,12.4,13.3],
    "HNO3":[-1.4],
    "H2SO4": [-3,1.9],
    "HCl" : [-6.3],
    "NH4" : [9.3],}

#Test with simple case, where expected value is known 
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
    "H2SO4": float(0.02),
    "Cl" : float(0),
    "NH4" : float(0)}

#expected value of the test
expected_pH=1.58
#Empty dictionary of values of the ionisation constant, the key being the temperature in degrees celcius, and the value being the constant
Value_of_Ionisation_Constant={}
Value_of_Ionisation_Constant[25]=10**(-14)

#Dictionary of charge of metal ion in solution 
compound_charge = {
    "Ca": 2,      # Calcium ion
    "Mg": 2,      # Magnesium ion
    "K": 1,       # Potassium ion
    "Mn": 2,      # Manganese ion
    "Zn": 2,      # Zinc ion
    "Cu": 2,      # Copper(II) ion
    "Fe(3+)": 3   # Iron(III) ion
}

#Dcionary of the highest known charge of the compound when it is undissociated
highest_existing_charge_of_compounds={
    "H3PO4": 0,
    "H3BO3": 0,
    "HNO3": 0,
    "H2SO4": 0,
    "HCl" : 0,
    "NH4" : 1}

def find_acid(ions_concentration:dict, acids_pKa:dict,highest_existing_charge_of_compounds:dict)->tuple:
    """
    Identify acids or their deprotonated forms, and return two dictionaries. One where the keys are the identified ions/acids 
    and attribute to them the pKas of the acid they're associated, the second with the same keys but values being the number of 
    protons the acid would have to lost to reach the form of the ion. 

    Parameters:
    ions_concentration (dict): A dictionary with ion names as keys and their concentrations as values.
    acids_pKa (dict): A dictionary with acid names as keys and their pKa values as lists.

    Returns:
    tuple with three dictionaries 
    1.Dictionary with identified ions being the key and their corresponding values being the number of protons it lost 
    compared to its non-deprotonated form. 
    2.Dictionary where ions are the key and the values are the pkas of the acid
    3.Dictionary where ions are the key and the values are the highest charge of the compound when it is undissociated
    """
    #Create  empty dictionary of number of protons lost by the identified ion/acid
    Degree_of_deprotonation={}
    #Creaty empty dictionary of ions with the corresponding pKa values of the acid they are associated to
    pKa_identified_ions={}
    #Create empty dictionary of the highest known charge of the compound when it is undissociated
    highest_existing_charge_of_identified_ion={}
    #Creates list of acids from pKa dictionary 
    acids = list(acids_pKa.keys())
    for ion, concentration in ions_concentration.items():
        #Value of constant set, which would be zero at end of loop if the ion wasn't identified and one if it was
        #This is used in order to print a message if the ion was not identified if one wants to debug
        i=0
        #Check if the solute is an acid that is not deprotonated
        for acid in acids:
            if ion==acid:
                #print(f"The solute:{ion}, was identified as being an acid in the list of pKa values")
                i=1
                Degree_of_deprotonation[ion]=0
                pKa_identified_ions[ion]=acids_pKa[acid]
                highest_existing_charge_of_identified_ion[ion]=highest_existing_charge_of_compounds[acid]
                continue
            else:
                # Check if the ion/solute is a deprotonated form of any acid
                    if len(ion)!=len(acid):
                        if len(ion)==len(acid)-1:
                            if acid[0] + acid[2:]==ion:
                                #print (f"Ion:{ion} was identified as being the deprotonated form of:", acid)
                                pKa_identified_ions[ion]=acids_pKa[acid]
                                Degree_of_deprotonation[ion]=int(acid[1])-1
                                highest_existing_charge_of_identified_ion[ion]=highest_existing_charge_of_compounds[acid]
                                i=1
                            else:
                                continue
                        elif len(ion)==len(acid)-2:
                            if ion==acid[2:]:
                                #print (f"Ion:{ion} was identified as being the deprotonated form of:", acid)
                                pKa_identified_ions[ion]=acids_pKa[acid]
                                Degree_of_deprotonation[ion]=int(acid[1])
                                highest_existing_charge_of_identified_ion[ion]=highest_existing_charge_of_compounds[acid]
                                i=1
                            else:
                                continue
                    else:
                        if acid[0]+acid[2:]==ion[0]+ion[2:]:
                            i=1
                            #print(f"Ion:{ion} was identified as being the deprotonated form of:", acid)
                            Degree_of_deprotonation[ion]=int(acid[1])-int(ion[1])
                            pKa_identified_ions[ion]=acids_pKa[acid]
                            highest_existing_charge_of_identified_ion[ion]=highest_existing_charge_of_compounds[acid]


        if i!=1: 
            #print("The ion or acid:", ion ,"could not be identified ")
            continue
    return Degree_of_deprotonation, pKa_identified_ions, highest_existing_charge_of_identified_ion

# Test values for the function
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

#Test
#find_acid(Test_concentration_of_solution, pKa_values)


#Testing the function
#pH_approximation(Test_concentration_of_solution,25)
