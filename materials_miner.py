#Materials Modelling Group, The Technical University of Kenya
#A python script for downloading material properties from the Materials Project Database.
'''
Prerequisites
1. Have Pymatgen installed in your system. 
2. Have an API key from the materials project website
'''
##Note: The script is open to more modifications depending on the need. 
from pymatgen import MPRester
import pandas as pd
m = MPRester('FImzw6RhEAMS1TVx')
def materials_class():
    '''
    This function allows one to define the family of materials that they are interested in and subsequently collect their material IDs and formulas. 
    perovskites, anti-perovskites, transition metal nitrides and transition metal carbides have been provided for starters, 
    More families can be added as one desires. 
    '''

    perovskites = m.query(criteria={'formula_anonymous':"ABC3", 'elements':{'$in':['Ba', 'Sr', 'Ca'], "$all":['Ti', 'O']}}, properties = ['task_id', 'pretty_formula'])
    anti_perovskites = m.query(criteria={'formula_anonymous':'A3BC', 'elements':{'$in':['Ba', 'Sr', 'Ca'], "$all":['Sn', 'O']}}, properties=['task_id', 'pretty_formula'])
    tmns = m.query(criteria = {'formula_anonymous':'AB', 'elements':{'$in':['Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rb', 'Pd', 'Ag', 'Cd'], "$all":['N']}}, properties=['task_id', 'pretty_formula'])
    tmcs = m.query(criteria={'formula_anonymous':'AB', 'elements':{'$in':['Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rb', 'Pd', 'Ag', 'Cd'], "$all":['C']}}, properties=['task_id', 'pretty_formula'])
    perovskites_df, anti_perovskites_df, tmns_df, tmcs_df = pd.DataFrame(perovskites), pd.DataFrame(anti_perovskites), pd.DataFrame(tmns), pd.DataFrame(tmcs)
    return perovskites_df, anti_perovskites_df, tmns_df, tmcs_df
def get_properties(family):
    '''
    This function takes in a family of perovskites from the data frames created in the materialsclass function. 
    It then iterates through every id in the dataframe and obtains the final energy, the bandgap, density, energy and possion ratio
    It finally returns the dataframe of the specific family selected with the updated entries. 
    '''
    family_ids = family.iloc[:, 0].values
    fenergy=[];  gap=[]; density=[] ; energy_p=[] ;  ratio=[]
    for num, i in enumerate(family_ids):

        properties = m.query(criteria={'task_id': i}, properties=['final_energy', 'band_gap', 'density', 'energy_per_atom', 'poisson_ratio'])
        fenergy.append(properties[0]['final_energy'])
        bgap.append(properties[0]['band_gap'])
        density.append(properties[0]['density'])
        energy_p.append(properties[0]['energy_per_atom'])
        ratio.append(properties[0]['poisson_ratio'])

        #properties = pd.DataFrame(properties)
    family['final_energy'] = fenergy
    family['band_gap'] = bgap
    family['density'] = density
    family['energy'] = energy_p
    family['poisson_ratio'] = ratio
    return perovskites_df

def save_to_csv(family_properties):
    '''
    This function simply takes the dataframe created from the get_properties function and saves it as a csv file for any further use
    '''
    csv_file = family_properties.to_csv('family'.csv)# this will be edited depending on the material family being used
    return csv_file

