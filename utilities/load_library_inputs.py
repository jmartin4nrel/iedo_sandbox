import os
import pandas as pd

'''
Loads iron electrowinning cost inputs from library files into config object
'''

def load_ore_cost(config, filepath):
    
    # Read cost csv into dataframe
    ore_df = pd.read_csv(filepath,index_col=0)
    ore_type = config.greenheart_config['iron']['ore_type']
    ore_cost = ore_df.loc[ore_type,'Price [$/tonne]']
    
    # Inflate with CPI
    cd = str(os.path.abspath(os.path.dirname(__file__)))
    cpi_df = pd.read_csv(cd+"/cpi.csv",index_col=0)
    dollar_year = ore_df.loc[ore_type,'$ year']
    cost_year = config.greenheart_config['project_parameters']['cost_year']
    ratio = cpi_df.loc[cost_year,'CPI']/cpi_df.loc[dollar_year,'CPI']
    config.greenheart_config['iron']['costs']['feedstocks']['iron_ore_pellet_unitcost'] = ore_cost*ratio


    return config

def load_tech_capex(config, filepath):

    # Read csv into dataframe and write to config
    capex_df = pd.read_csv(filepath,index_col=0)
    tech = config.greenheart_config['iron']['technology']
    tech_capex = capex_df.loc[tech,'CAPEX [$/MTPY]']

    # Inflate with CEPCI
    cd = str(os.path.abspath(os.path.dirname(__file__)))
    cepci_df = pd.read_csv(cd+"/cepci.csv",index_col=0)
    dollar_year = capex_df.loc[tech,'$ year']
    cost_year = config.greenheart_config['project_parameters']['cost_year']
    ratio = cepci_df.loc[cost_year,'CEPCI']/cepci_df.loc[dollar_year,'CEPCI']
    config.greenheart_config['iron']['costs']['capex_misc'] = tech_capex*ratio

    return config