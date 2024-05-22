
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


def Refill_of_container(
    concentration_of_ions: dict[str, float], 
    optimal_ion_concentrations: dict[str, float], 
    *args: float
) -> dict[str, float]:
    """
    Refill the container with ions that are below the optimal concentration.
    
    This function optionally checks if the concentration of ions in the solution is within an acceptable 
    range of the optimal concentration. If specified, it skips ions that are within the acceptable deviation 
    and refills only those that are below the optimal concentration.

    Parameters:
        concentration_of_ions (dict[str, float]): A dictionary containing the concentration of ions in the solution.
        optimal_ion_concentrations (dict[str, float]): A dictionary containing the optimal concentration of ions in the solution.
        *args (float): A list of acceptable maximum percentage deviations from the optimal concentration of ions in the solution.

    Returns:
        dict[str, float]: A dictionary containing the ions and the quantities to add to the solution.
    """
    # This part calculates the quantities of ions to add to the solution
    Ion_quantities_to_add={}
    for ion, concentration in concentration_of_ions.items():
            concentration_to_add=optimal_ion_concentrations[ion]-concentration_of_ions[ion]
            Ion_quantities_to_add[ion]= concentration_to_add
    return Ion_quantities_to_add

            
    