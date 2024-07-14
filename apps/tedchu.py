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

    # What's beam will be reduced
    prefix = ['FB', 'SB']

    # Assign Non-Sway

    # Return

## Rules of Definition
def create_concrete_column(etabs, print_log, column_info) :
    obj = etabs.sapModel

    # Column Information
    # BxH, fc, fy, cover
    b = column_info['B']
    h = column_info['H']
    fc = column_info['fc']
    fy = column_info['fy']
    cover = column_info['cover']

    # Define Column Section

    # Return
    

def create_concrete_beam(etabs, print_log, beam_info, prefix) :
    obj = etabs.sapModel

    # Column Information
    # BxH, fc, fy, cover
    b = beam_info['B']
    h = beam_info['H']
    fc = beam_info['fc']
    fy = beam_info['fy']
    cover_top, cover_bot = beam_info['cover']


    # Define Column Section

    # Return

def change_story_material(etabs, print_log, story_material) :
    #################################
    #
    # story_material = {
    #   story:str : [fc:str, fy_c:str, fy_b:str, fy_sb:str, fy_fb:str]
    # }
    #
    #################################
    
    obj = etabs.sapModel

    
