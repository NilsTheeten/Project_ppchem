import pandas as pd
#----------------------------User Input---------------------
def excel_to_dataframe(file_path, sheet = "Solution"):
    """
    Converts an Excel file into a Pandas DataFrame.
    
    Args:
    - file_path (str): The path to the Excel file.
    
    Returns:
    - df (DataFrame): The Pandas DataFrame containing the data from the Excel file.
    """
    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet, skiprows=0)
        return df
    except Exception as e:
        print("An error occurred while reading the Excel file:", e)
        return None
"""
# Example usage:
file_path = 'C:/Users/nilst/Documents/EPFL/BA_4/ppchem/Project/UserData.xlsx'
df = excel_to_dataframe(file_path)
print(df.head())
"""
def name2Ksp(df, salt_name):
    """
    Access the solubility product constant (Ksp) of a salt based on its name.
    
    Args:
    - df (DataFrame): The Pandas DataFrame containing the data.
    - salt_name (str): The name of the salt.
    
    Returns:
    - solubility (float): The solubility product constant (Ksp) of the salt.
    """
    try:
        # Access the solubility based on the name of the salt
        solubility = df.loc[df['Salt Name'] == salt_name, 'Ksp (20°C)'].values[0]
        return solubility
    except Exception as e:
        print("An error occurred while accessing the solubility:", e)
        return None
    
def formula2Ksp(df, formula):
    """
    Access the solubility product constant (Ksp) of a salt based on its name.
    
    Args:
    - df (DataFrame): The Pandas DataFrame containing the data.
    - salt_name (str): The name of the salt.
    
    Returns:
    - solubility (float): The solubility product constant (Ksp) of the salt.
    """
    try:
        # Access the solubility based on the name of the salt
        solubility = df.loc[df['Chemical formula'] == formula, 'Ksp (20°C)'].values[0]
        return solubility
    except Exception as e:
        print("An error occurred while accessing the solubility:", e)
        return None
"""   
# Example usage:  
salt_name = 'Potassium nitrate'
print(name2Ksp(df, salt_name))

solution_df = excel_to_dataframe(file_path, "Solution")
plant_df = excel_to_dataframe(file_path, "Plants")

solution_df
"""
def create_solutiondict(solution_df):
    solution_dict = {}
    for i in range(len(solution_df)):
        solution_dict[solution_df.iloc[i,1]] = solution_df.iloc[i,5]
    return solution_dict
"""
# Example usage:
file_path = 'C:/Users/nilst/Documents/EPFL/BA_4/ppchem/Project/UserData.xlsx'
solution_df = excel_to_dataframe(file_path, "Solution")
solution_dict = create_solutiondict(solution_df)
"""
#------------------------------------------------------------
