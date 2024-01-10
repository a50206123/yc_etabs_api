# yc_ETABS_API 

## v0.0 Develping 

### Create Notes 
+ ETABS 

+ Table
    + read (
        key -> str, 
        col -> list = None  
        ) return table -> pandas.df 
    + write (
        key -> str, 
        df -> pandas.df 
        )

+ Point 
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
+ Frame 
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
+ Shell 
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

+ Define
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
        stype -> int,
        name -> str,
        stiff -> dict,
        linear -> int
        )
    + diaphragm_add (
        name -> str,
        is_semi_rigid -> bool = False
        )

+ Assign
    + frame_section (
        unique -> int,
        sect -> str
        )