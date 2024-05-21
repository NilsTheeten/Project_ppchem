import matplotlib.pyplot as plt  # Importing matplotlib for plotting
import pandas as pd
from hydroponics.PH_Approximation_0 import pH_approximation
import os

pH_limit_of_plants = {
    "Eggplant": [6.2, 6.8],
    "Cucumber": [6.0, 7.0],
    "Bell pepper": [5.5, 6.5]
}

def generation_of_pH_list(concentrations_list:list, temperature:float, plant:str)->(tuple):
    """
    Generate pH values and identifies days where pH exceeded limits.

    Parameters:
        concentrations_list (list): list of dictionaries of concentrations throughout days, with the index of the 
        dictionary in the list being the day where the concentrations were derived.
        temperature (float): Temperature value.
        plant (str): Name of the plant.

    Returns:
        list: pH values for each concentration.
        list: Indices of days where pH exceeded limits.
    """
    pH_values = []  # List to store pH values
    Days_where_pH_was_exceeded = []  # List to store indices of days where pH exceeded limits

    # Loop through each concentration in the array
    for i in range(len(concentrations_list)):
        # Calculate pH value for the concentration
        pH_value = pH_approximation(concentrations_list[i], temperature)
        # Append pH value to the list
        pH_values.append(pH_value)
        
        # Check if the pH value is within specified limits for the plant
        if plant in pH_limit_of_plants:
            if pH_limit_of_plants[plant][0] < pH_value < pH_limit_of_plants[plant][1]:
                pass  # pH within limits, no action required
            else:
                # pH exceeds limits, add index to the list
                Days_where_pH_was_exceeded.append(i)
        else:
            if pH_value < pH_value < 7.0:
                pass  
            else:
                # pH exceeds limits, add index to the list
                Days_where_pH_was_exceeded.append(i)
    return pH_values, Days_where_pH_was_exceeded


def pH_graph(pH_values:list,Days_where_pH_was_exceeded:list,plant:str)->None:
    """"
    Generates a graph of pH values over time, with marked points where pH exceeded limits and a table of points of excess pH levels.
    Parameters:
        pH_values (tuple of lists of pH values over time)
        Days_where_pH_was_exceeded (list)
        plant (str)
    Returns:
        None

    """
    # Define acceptable pH range for a specific plant
    pH_range_min =pH_limit_of_plants[plant][0]
    pH_range_max =pH_limit_of_plants[plant][1]

    # Plot pH values
    plt.figure(figsize=(12, 6), dpi = 500)
    plt.plot(pH_values, marker='o', label='pH values')
    
    color = 'red'  # Color for the marked points

    for idx in Days_where_pH_was_exceeded:
        plt.plot(idx, pH_values[idx], marker='o', color=color)  # Plot each marked point with the specified color

    # Draw horizontal lines for acceptable pH range
    plt.axhline(y=pH_range_min, color='r', linestyle='--', label='Acceptable range (min)')
    plt.axhline(y=pH_range_max, color='g', linestyle='--', label='Acceptable range (max)')

    # Add legend
    plt.legend()

    # Add labels and title
    plt.xlabel('Days')
    plt.ylabel('pH')
    plt.title('pH Values Over Time')

    #Save Graph to the current directory
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_name = "graph_pH"
    file_path = os.path.join(current_dir, file_name)
    plt.savefig(file_path + ".png", format='png')  # Save as a PNG file for matplotlib

    # Initialize an empty list to hold dictionaries
    data_dict_list = []

    for i in Days_where_pH_was_exceeded:
        # Create a dictionary for each row
        row_dict = {
            'Day': i,
            'pH': pH_values[i]
        }
        # Append the dictionary to the list
        data_dict_list.append(row_dict)

    # Convert the list of dictionaries to a DataFrame
    table_of_points_of_excess = pd.DataFrame(data_dict_list)
        # Plot the table with a title
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=table_of_points_of_excess.values,
             colLabels=table_of_points_of_excess.columns,
             cellLoc='center', loc='upper center')
    plt.title("Points of Excess pH Levels")
    
    #Save Graph to the current directory
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_name = "Table_pH"
    file_path = os.path.join(current_dir, file_name)
    plt.savefig(file_path + ".png", format='png')  # Save as a PNG file for matplotlib
'''
# Example of values for testing pH graph
pH_values = [6.4, 6.5, 6.8, 6.2, 6.4, 6.4, 6.0, 5.8]
Days_where_pH_was_exceeded=[6,7]
pH_graph(pH_values,Days_where_pH_was_exceeded,"tomatoes")
'''

def pH_part_of_report_generation(concentrations_list:list, temperature:float, plant:str)->None:
    """"
    Generates a pH graph and a table of points of excess pH levels by calling the generation_of_pH _list function followed 
    by the pH_graph function and displaying the results.
    Parameters:
        concentrations_list (dict) 
        temperature (float)
        plant (str)
    Returns:
        None
    """
    pH_values, Days_where_pH_was_exceeded=generation_of_pH_list(concentrations_list, temperature, plant)
    pH_graph(pH_values,Days_where_pH_was_exceeded,plant)

    
    
