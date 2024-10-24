# iedo_sandbox

This is a project repo for the IEDO Iron Electrowinning Project using GreenHEART.

How to run:

1. Install HOPP/GreenHEART from Jonathan Martin's fork, the "iedo_sandbox" branch

2. Test by running the example script run_example_plant.py

3. Test out different model inputs by changing values in example_plant/input/plant/greenheart_config.yaml,
    specifically iron: technology and iron: ore_type and re-running run_example_plant.py
    (These are just loading junk values for now, to test out the new iron.py technology module in GreenHEART)

To run NED-toolbox:

1. Switch to the "feature/ned" branch of HOPP/GreenHEART (on Jonathan Martin's fork still)

2. cd to NED-toolbox/

3. pip install -r requirements.txt

4. pip install -e .

5. Test by running the example script NED-toolbox/toolbox/verify-setup/00-verify_1site_api.py
    (Will take several minutes to run all the way through, can kill once you see "FLORIS is the system model")