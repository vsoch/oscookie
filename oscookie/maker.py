'''

maker.py: Supplementary functions to help with toy analysis


'''

import sys

def generate_random_spec(spec_type=None):
    '''generate_random_spec is the main function to generate a random
    spec file. Depending on the file, a different command (eg package
    manager) will be run to download software.
    '''
    # Collect inputs for number to generate
    if spec_type == None:
        spec_type = "Singularity"

    if spec_type != "Singularity":
        print("Currently only supported spec type is Singularity, sorry.")
        sys.exit(1)

    
    # For each
    # select random operating system
    # Select random number for install and remove
    # Install and remove packages
    # If have sublanguage (eg, node, python, R) install random set
    # Write commands into Singularity spec
    print('Vanessa needs to write me!')



def select_software(baseos,minN=10,maxN=50):
    '''select software will select a random set of software
    to install based on a particular os.
    '''
    # Read in OS
    # Select random N
    print('Vanessa needs to write me!')



