def units2num(unit:str) -> int : 
    idx = units_num
    return idx[unit]

def num2units(num:int) -> list :
    idx = units_num
    return reverse_index(idx, num).split('_')

def force2num(force_unit:str) -> int :
    idx = {
    'N' : 3, 
    'kN' : 4,  
    'kgf' : 5, 
    'tonf' : 6
    }   
    return idx[force_unit]

def length2num(length_unit:str) -> int:
    idx= {
        'mm' : 4, 
        'cm' : 5, 
        'm' : 6
    }
    return idx[length_unit]

def mtype2num(mat:str) -> int: 
    idx = {
        'steel' : 1,
        'concrete'  : 2,
        'none' : 3,
        'rebar' : 6
    }
    return idx[mat]

def loadpattern2number (load_type:str) -> int :
    idx = {
        'Dead' : 1,
        'Super Dead' : 2,
        'Live' : 3,
        'Reducible Live' : 4,
        'Seismic' : 5,
        'Wind' : 6,
        'Snow' : 7,
        'Other' : 8,
        'EV' : 8,
        'MASS' : 8,
        'ROOF Live' : 11,
        'Notional' : 12,
        'Seismic (Drift)' : 37,
        'QuakeDrift' : 61,
    }
    return loadpattern2number(load_type)

def reverse_index(data, value) :
    for i, j in data.items() :
        if j == value :
            return i
    return None

def units2num(units:str) -> int:
    units_num = {
        'kn_mm' : 5,
        'kn_m' : 6,
        'kgf_mm' : 7,
        'kgf_m' : 8,
        'n_mm' : 9,
        'n_m' : 10,
        'tonf_mm' : 11,
        'tonf_m' : 12,
        'kn_cm' : 13,
        'kgf_cm' : 14,
        'n_cm' : 15,
        'tonf_cm' : 16,
        
    }
    return units_num[units]