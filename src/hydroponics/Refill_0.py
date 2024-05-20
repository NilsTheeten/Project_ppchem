
import time

""""
Optional: Implement the following function that will be called by the main function that is provided below.

def Concentration_Checker(frequency:float)->None:
    print("Monitoring of Concentration started at:", time.time())

# Converts frequency in number of times per day to per second (e.g., 2 times per second)
frequency =frequency/(24*60*60) # calls per second

# Calculate the time interval between function calls
time_interval = 1 / frequency # seconds

while True:
    Refill_of_container(concentration_of_ions, acceptable_maximum_percentage_deviation_from_optimal, optimal_ion_concentrations)
    time.sleep(time_interval)    
"""


def Refill_of_container(concentration_of_ions:dict, optimal_ion_concentrations:dict,*args:float)->dict[str: float]:
    """
    This function (optionally) checks the concentration of ions in the solution, but otherwise refills the container with the ions that are below the optimal concentration.

    Parameters:
    concentration_of_ions: A dictionary containing the concentration of ions in the solution.
    optimal_ion_concentrations: A dictionary containing the optimal concentration of ions in the solution.
    *args: A list of acceptable maximum percentage deviation from optimal concentration of ions in the solution.

    Returns:
    A dictionary containing the ions and the quantities to add to the solution.
    """
    # This part checkS if the concentration of ions in the solution is within the acceptable range of the optimal concentration
    """"
    for arg in args:
        arg=acceptable_maximum_percentage_deviation_from_optimal=
    for ion, concentration in concentration_of_ions:
        if (concentration-optimal_ion_concentrations[ion])/optimal_ion_concentrations[ion]*100>acceptable_maximum_percentage_deviation_from_optimal:
            continue
        return "Concentrations within solution are optimal"
    """
    # This part calculates the quantities of ions to add to the solution
    Ion_quantities_to_add={}
    for ion, concentration in concentration_of_ions:
            concentration_to_add=optimal_ion_concentrations[ion]-concentration_of_ions[ion]
            Ion_quantities_to_add.update(ion, concentration_to_add)
    return Ion_quantities_to_add
            
    