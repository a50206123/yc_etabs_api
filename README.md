# yc_ETABS_API 

## v0.0 Develping 

### Create Notes
----- 
### OUTLINE
+ ETABS : main class
    + get_version()
    + set_units(
        force_unit -> str,
        length_unit -> str
        )
    + save_edb()
    + export_e2k()
    + export_mdb()
    + import_e2k(
        filename -> str
        )
    + import_excel(
        filename -> str
        )

+ Table : Get & Set model database
    + read (
        key -> str, 
        col -> list = None  
        ) return table -> pandas.df 
    + write (
        key -> str, 
        df -> pandas.df 
        )

+ Point : For geometry of point
    + add (
        [x -> float, 
         y -> float, 
         z -> float]
        ) return unique -> int 
    + modify (
        unique -> str, 
        [x -> float, 
         y -> float, 
         z -> float]
        ) 
    + delete (
        unique -> int, 
        )
    + unique2label (
        unique -> int
        ) return label -> int
    + label2unique (
        label -> int,
        story -> str, 
        ) return unique -> int
+ Frame : For geometry of frame
    + add (
        [point1 -> int, 
         point2 -> int], 
        sect -> str, 
        ) return unique -> int 
    + modify (
        unique -> str, 
        [point1 -> int, 
         point2 -> int]
        ) 
    + delete (
        unique -> str, 
        ) 
    + unique2label (
        unique -> int
        ) return label -> int
    + label2unique (
        label -> int,
        story -> str, 
        ) return unique -> int
+ Shell : For geometry of shell
    + add (
        [points -> int], 
        sect -> str, 
        ) return unique -> int 
    + modify (
        unique -> str, 
        [points -> int]
        ) 
    + delete (
        unique -> str, 
        ) 
    + unique2label (
        unique -> int
        ) return label -> int
    + label2unique (
        label -> int,
        story -> str, 
        ) return unique -> int

+ Define : For Definition Setting
    + material_add (
        name -> str,
        props -> dict,
        material_type -> str,
        design_data -> dict
        )
    + material_modify (
        name -> str,
        props -> dict,
        material_type -> str,
        design_data -> dict
        )
    + frame_section_add (
        name -> str,
        props -> dict,
        design_data -> dict
        )
    + frame_section_modify (
        name -> str,
        props -> dict,
        design_data -> dict
        )
    + shell_section_add (
        name -> str,
        props -> dict,
        design_data -> dict
        )
    + shell_section_modify (
        name -> str,
        props -> dict,
        design_data -> dict
        )
    + spring_add (
        stype -> str,
        name -> str,
        stiff -> dict,
        linear -> int
        )
    + diaphragm_add (
        name -> str,
        is_semi_rigid -> bool = False
        )

+ Assign : For Assignments
    + frame_section (
        unique -> int,
        sect -> str
        )
    + frame_property_modifier(
        unique -> int,
        modifier -> dict,
        is_replace -> bool = True
        )
    + frame_rigid_zone (
        unique -> int,
        rigid_zone -> float
        )
    + frame_spring (
        unique -> int,
        spring_name -> str,
        spring_stiff -> float
        )
    + shell_section (
        stype -> str
        unique -> int,
        sect -> str
        )
    + shell_diaphragm (
        unique -> int,
        diaphragm_name -> str
        )
    + shell_automash (
        unique -> int,
        automash_setting -> dict
        )