######## TEDCHU ########
# It's functions for operating ETABS in TEDCHU

#### Constant Zone ####
fc_enum = {
    'A' : 210, 'B' : 245, 'C' : 280, 
    'D' : 315, 'E' : 350, 'F' : 385, 
    'G' : 420, 'F' : 490, 'H' : 560
}
fy_enum = {
    'J' : 4200, 'Q' : 5000, 'K' : 5600
}


#### Function Zone ####
## Common Operations
def torsion_reduction(etabs, print_log) :
    obj = etabs.sapModel

    # What's beam will be reduced
    prefix = ['B', 'SB']

    # Assign Torsion Reduction

    # Return

def set_nonsway(etabs, print_log) :
    obj = etabs.sapModel


## Rules of Definition
def create_concrete_column(etabs, print_log) :
    obj = etabs.sapModel

def create_concrete_beam(etabs, print_log) :
    obj = etabs.sapModel

def change_story_material(etabs, print_log) :
    obj = etabs.sapModel

