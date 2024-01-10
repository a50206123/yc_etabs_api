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
        x -> float, 
        y -> float, 
        z -> float, 
        ) return unique -> int 
    + modify (
        unique -> str, 
        x -> float, 
        y -> float, 
        z -> float, 
        ) 
        