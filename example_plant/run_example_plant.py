# general imports
import os
import json
import pickle

# # yaml imports
import yaml
from pathlib import Path

# HOPP imports
from greenheart.simulation.greenheart_simulation import (
    run_simulation,
    GreenHeartSimulationConfig,
)
from greenheart.simulation.greenheart_simulation import run_simulation as run_greenheart
from greenheart.tools.optimization.gc_run_greenheart import run_greenheart as run_greenheart_with_om
from greenheart.tools.optimization.fileIO import save_data, load_data
import openmdao.api as om

from utilities.load_library_inputs import load_ore_cost, load_tech_capex

'''
Simulates an example iron plant in GreenHEART - copied from 01-onshore-steel-mn in dev/refactor and
altered to fit the IEDO Iron Electrowinning project
'''

if __name__ == "__main__":

    # Decide if running a new simulation or loading a previously run simulation
    run_new = True
    filename = "example_plant"

    # Decide if running OpenMDAO problem or straight GreenHEART simulation (True for OpenMDAO)
    run_om = False
    
    # Decide if analyzing or optimizing (True for analysis, False for optimization)
    run_analysis = True

    # Load inputs as needed
    filepath = str(os.path.abspath(os.path.dirname(__file__)))
    input_filepath = filepath + "/input/"
    output_filepath = filepath + "/output/"
    turbine_model = "lbw_6MW"
    filename_turbine_config = input_filepath+"turbines/"+turbine_model+".yaml"
    filename_floris_config = input_filepath+"floris/floris_input_lbw_6MW.yaml"
    filename_hopp_config =  input_filepath+"plant/hopp_config_mn.yaml"
    filename_greenheart_config =  input_filepath+"plant/greenheart_config_onshore_mn.yaml"

    # Set cost filepaths
    ore_cost_filepath = input_filepath + "cost_library/ore_cost.csv"
    tech_capex_filepath = input_filepath  + "cost_library/tech_capex.csv"

    # Set up GreenHEART configuration
    if run_new:
        config = GreenHeartSimulationConfig(
            filename_hopp_config,
            filename_greenheart_config,
            filename_turbine_config,
            filename_floris_config,
            verbose=False,
            show_plots=False,
            save_plots=False,
            use_profast=True,
            post_processing=False,
            incentive_option=1,
            plant_design_scenario=9,
            output_level=7,
        )

        # Load ore- and tech- specific costs
        config = load_ore_cost(config,ore_cost_filepath)
        config = load_tech_capex(config,tech_capex_filepath)

    # Run/load GreenHEART simulation
    if run_om:
        
        # Run using OpenMDAO
        if True: #run_new: #TODO - Make load_data actually work?
            prob, config = run_greenheart_with_om(config, run_only=run_analysis)

            # Save GreenHEART data (OpenMDAO inputs/outputs)
            save_data(output_filepath+filename+"_om", prob)

        else:

            # Load GreenHEART data (OpenMDAO inputs/outputs) - doesn't work...
            om_problem = om.Problem()
            prob = load_data(filename, om_problem)
    
        lcoe = prob.get_val("lcoe", units="USD/(MW*h)")
        lcoh = prob.get_val("lcoh", units="USD/kg")
        lcoi = prob.get_val("lcoi", units="USD/t")

    else:
        
        # Run not using OpenMDAO
        if run_new:
            lcoe, lcoh, iron_finance, ammonia_finance = run_greenheart(config)
            lcoi = iron_finance.sol['price']
            
            # Save GreenHEART data (lcoe, lcoh, and IronCostModelOutputs)
            output = open(output_filepath+filename+"_lcoe.txt", 'w')
            output.write(str(lcoe))
            output = open(output_filepath+filename+"_lcoh.txt", 'w')
            output.write(str(lcoh))
            output = open(output_filepath+filename+"_sf.pkl", 'wb')
            pickle.dump(iron_finance, output)

        # Load from saved files
        else:
            input = open(output_filepath+filename+"_lcoe.txt")
            lcoe = float(input.read())
            input = open(output_filepath+filename+"_lcoh.txt")
            lcoh = float(input.read())
            input = open(output_filepath+filename+"_sf.pkl", 'rb')
            iron_finance = pickle.load(input)
            lcoi = iron_finance.sol['price']


    print("LCOE: ", lcoe, "[$/MWh]")
    print("LCOH: ", lcoh, "[$/kg]")
    print("LCOI: ", lcoi, "[$/metric-tonne]")
