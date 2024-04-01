import pandas as pd
import os
import re

class ChangeSection :
    def __init__(self, etabs, excel_filename = None) -> None:
        self.etabs = etabs
        self.excel_filename = excel_filename
        
        self.read_info()
        self.get_story_suffix()

        self.reg_sect = re.compile(r"(\D+)(\d+\.*\d*\.*\d*)(\D+)")

    def read_info(self) :
        excel_filename = self.excel_filename
        etabs = self.etabs

        if excel_filename == None :
            excel_filename = 'Auto_Info'

            for name in os.listdir(etabs.EDB_path) :
                if excel_filename in name :
                    print('found')
                    df = pd.read_excel(f'{etabs.EDB_path}\\{name}', sheet_name='- 樓層置換資訊')
                    break
                else : 
                    if name == os.listdir(etabs.EDB_path)[-1] :
                        print(f'No EXCEL to Read !! {etabs.EDB_path}')

        else :
            df = pd.read_excel(etabs.EDB_path+name, sheet_name='- 樓層置換資訊')

        self.df = df
    
    def get_story_suffix(self) :
        df = self.df
        
        story_suffix = {}

        story = df['Story']
        conc = df['Conc']
        col = df['Column']
        bm = df['Beam']
        sb = df['SBeam']
        fb = df['FBeam']

        for i in range(len(df)) :
            story_suffix[story[i]] = {
                'C' : conc[i]+col[i],
                'B' : conc[i]+bm[i],
                'SB' : conc[i]+sb[i],
                'FB' : conc[i]+fb[i],
            }
        
        self.story_suffix = story_suffix

    def run(self) :
        etabs = self.etabs
        story_suffix = self.story_suffix

        frames = etabs.Frames.get_name_list()

        for frame in frames :
            label, story = etabs.Frames.unique2label(frame)
            sect = etabs.Frames.get_section(frame)

            if etabs.Define.Material.get(etabs.Define.FrameSect.get(etabs.Frames.get_section(frame),shape='rect')['mat'])['mat_type'] != 2 :
                # Not Concrete then SKIP
                print(f'Frame ({story} {label}) skips')
                # print(etabs.Frames.get_section(frame))
                # print(etabs.Define.Material.get(etabs.Frames.get_section(frame)))
                continue

            ftype, size, mat = self.reg_sect.findall(sect)[0]

            if mat == story_suffix[story][ftype] :
                # print(f'Frame ({story} {label}) doesn\'t need change')
                continue
            else :
                sect = ftype + size + story_suffix[story][ftype]
                print(f'Frame ({story} {label}) change to {sect}')

                etabs.Frames.set_section(frame, sect)
        



if __name__ == '__main__' :
    from yc_etabs_api.etabs import ETABS
    etabs = ETABS()

    changeSection = ChangeSection(etabs=etabs)

    # print(changeSection.story_suffix)

    # result = changeSection.reg_sect.findall("B40.570.5CJ")
    # print(result)

    changeSection.run()