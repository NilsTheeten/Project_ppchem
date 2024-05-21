"""
This file contains the functions needed in order to generate an automatic report.
"""

#Imports
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

from .Basic_functions import make_solution
from .Solutions_Solubility import plot_graph, data4graph
from .PH_Approximation_0 import *
from .pH_graph_0 import *

# Auxiliar functions
def merge_dicts(dict1, dict2, ions_of_interest = "all"):
    # Get the union of keys from both dictionaries
    all_ions = set(dict1.keys()) | set(dict2.keys())
    
    # Create lists to store ion names, values from dict1, and values from dict2
    ion_names = []
    values_dict1 = []
    values_dict2 = []
    
    # Iterate over ion names
    for ion in all_ions:
        # Append ion name to ion_names list
        if ion in ions_of_interest or ions_of_interest == "all":
            ion_names.append(ion)
        
        # Append value from dict1 or None if key does not exist
        if ion in dict1 and ion in ion_names:
            values_dict1.append(round(dict1[ion],4))
        elif ion in ion_names:
            values_dict1.append(0)
        
        # Append value from dict2 or None if key does not exist
        if ion in dict2 and ion in ion_names:
            values_dict2.append(round(dict2[ion],4))
        elif ion in ion_names:
            values_dict2.append(0)
    
    return [ion_names, values_dict1, values_dict2]

#---------- Main function ---------------------------------

def generate_report(
    plant_name: str,
    required_nutriments: dict,
    growth_time: float,
    ions_of_interest: list,
    solution_composition: dict,
    solution_volume: float,
    forbidden_ions: list = [],

) -> None:
    """
    Generates a simulation report in PDF format based on the provided parameters.

    Args:
        plant_name (str): The name of the plant for which the hydroponic solution simulation is conducted.
        required_nutriments (dict): A dictionary containing the required nutriments (ions) for the specified plant for a full growth [g].
        solution_composition (dict): A dictionary representing the composition of the hydroponic solution [g/L] for each ion.
        solution_volume (float): The volume of the hydroponic solution [L].
        ions_of_interest (list): A list of ions for which the concentration is of interest.
        growth_time (float): The duration of the growth of the plant [days].
        forbidden_ions (list, default): A list of ions that are forbidden in the solution.

    Returns:
        None: a pdf is created in the folder of this file
    """
    print("Generating report...")
    # PageTemplate of the document
    doc = SimpleDocTemplate("hydroponic_report.pdf", pagesize=letter)
    story = []
    interest_ions = ", ".join(ions_of_interest)
    nono_ions = ", ".join(forbidden_ions)
    
    # Title
    title_style = getSampleStyleSheet()["Title"]
    title = Paragraph("Hydroponic Farming Simulation Report", title_style)
    story.append(title)
    story.append(Spacer(1, 12))

    # 1 .Simulation conditions ---------------------------------------------------------
    subtitle_style = getSampleStyleSheet()['Heading2']
    subtitle = Paragraph(" 1. Simulation Conditions", subtitle_style)
    story.append(subtitle)
    story.append(Spacer(1, 6))
    
    paragraph_style = getSampleStyleSheet()["Normal"]
    conditions_text = f"This report summarizes the simulation of the growth of a {plant_name} in a hydroponic solution.<br/>"\
    f"The volume of the solution used in the simulation is {solution_volume} L. "\
    f"The simulation was done for a duration of {growth_time} days and the followig ions were analysed: {interest_ions}.<br/> <br/>"\
    f"The following assumptions were made for the simulation:<br/>"\
        f" - The plant consumes a constant amount of nutriments each day <br/>"\
        f" - The temperature is assumed to be constant at 25 °C and the pressure at 1 atm. <br/>"\
        f" - The effect of the sun exposure and light conditions was neglected. <br/> <br/>"\
    f"The following elements were simulated and analysed:<br/>"\
        f" - The amount of salts to add to the solution. <br/>"\
        f" - The evolution of the concentration of the ions of interest in the solution. <br/>"\
        f" - The pH of the solution. <br/>"\
    f"<br/> <br/>"\
    f" The table below shows the provided optimal concentrations of the ions in the hydroponic solution and "\
    f"the nutritional needs of the {plant_name} plant (fully grown):"
    story.append(Paragraph(conditions_text, paragraph_style))
    story.append(Spacer(1, 12))
    
    #Table 
    data = merge_dicts(solution_composition, required_nutriments, ions_of_interest)
    headers = ["Ions",'Hydroponic solution [g/L]', f'{plant_name} nutriments requirements[g]']
    table_data = [[elem] + sublist for elem, sublist in zip(headers, data)] 
    # Transpose the data (swap rows and columns)
    table_data = list(map(list, zip(*table_data)))
    table = Table(table_data)
    table.setStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12)])
    # Calculate required size for the table
    table.wrap(doc.width, doc.height)
    
    # Add the table to the story
    story.append(table)
    story.append(Spacer(1, 12))
    print("Collecting the data ...")
    # 2. Preparation of the solution ---------------------------------------------------------
    subtitle = Paragraph(" 2. Preparation of the solution", subtitle_style)
    story.append(subtitle)
    story.append(Spacer(1, 6))
    
    preparation_text = f"The table below shows the mass of salts to add the the {solution_volume} L solution" \
        f" to obtain the desired concentrations of the ions for the {plant_name} plant.<br/>"\
        f" The following restrictions were given for the preparation of the solution:<br/>"\
        f" - Forbidden ions: {nono_ions} <br/>"\
        f" - All the salts must be soluble. <br/>"\
        f" - The salts come from a list of commercially available salts. <br/>"
        
    story.append(Paragraph(preparation_text, paragraph_style))
    story.append(Spacer(1, 12))
    
    #Add table: "salts to add in the solution"
    salt_composition = make_solution(solution_composition, forbidden_ions ,solution_volume)
    headers = ["Salts"]+list(salt_composition.keys())
    data = list(salt_composition.values())
    data = [round(float(elem), 4) for elem in data]
    data = [f"Mass [g] for {solution_volume} L solution"]+data
    table_data = [[elem] + [sublist] for elem, sublist in zip(headers, data)]
    table = Table(table_data)
    table.setStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12)])
    # Calculate required size for the table
    table.wrap(doc.width, doc.height)
    story.append(table)
    story.append(Spacer(1, 12))
    
    
    # 3. Ion concentration elvolution ---------------------------------------------------------
    subtitle = Paragraph(" 3. Evolution of the concentration of ions", subtitle_style)
    story.append(subtitle)
    story.append(Spacer(1, 6))
    
    ion_figure_text = f"The Figure below shows the concentration of the ions of interest ({interest_ions}) " \
        f"as a function of the days of growth of the plant."
    story.append(Paragraph(ion_figure_text, paragraph_style))
    story.append(Spacer(1, 12))
    
    # Make the graph
    plot_graph(solution_composition, "ion", required_nutriments, growth_time, solution_volume, ions_of_interest)
    
    # Get the path of the graph
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_name = "graph_"
    for ion in ions_of_interest:
        file_name += str(ion) + "_"
    file_name += ".png"
    file_path = os.path.join(current_dir, file_name)

    # Add the image to the story and center it
    image = Image(file_path, width=600, height=300)
    image.hAlign = 'CENTER'
    story.append(image)
    story.append(Spacer(1, 12))
    
    print("Simulating the plant growth...")
    # 4. pH of the solution ---------------------------------------------------------
    subtitle = Paragraph(" 4. pH of the solution", subtitle_style)
    story.append(subtitle)
    story.append(Spacer(1, 6))
    
    pH_text = f"The Figure below shows the pH of the solution as a function of the growth of the plant."\
        f"The pH limits are shown in the graph."
    
    story.append(Paragraph(pH_text, paragraph_style))
    story.append(Spacer(1, 12))
    
    #Generate the data
    solution_pH = data4graph(solution_composition,solution_volume,required_nutriments,growth_time)[1]
    temp = int(25)
    pH_part_of_report_generation(solution_pH, temp, plant_name) #create images
    
    # Get the path of the pH_graph
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_name = "graph_pH.png"
    file_path = os.path.join(current_dir, file_name)
    # Add the image to the story and center it
    image = Image(file_path, width=600, height=300)
    image.hAlign = 'CENTER'
    story.append(image)
    story.append(Spacer(1, 12))
    
    # Get the path of the pH_table
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_name = "Table_pH.png"
    file_path = os.path.join(current_dir, file_name)
    # Add the image to the story and center it
    image = Image(file_path, width=300, height=300)
    image.hAlign = 'CENTER'
    story.append(image)
    story.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(story)
    print("Report generated successfully!")
    
