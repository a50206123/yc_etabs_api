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

# from yc_etabs_api import ETABS

class TedChuMethods :
    def __init__(self, etabs, print_log) :
        self.etabs = etabs
        self.print_log = print_log

    #### Function Zone ####
    ## Common Operations
    def release(self, release_end = "", isSelectAfterAssigning = True) :
        self.etabs.model_unlock()
        selected_frames = self.etabs.Select.get(type_='Frame')
        
        for frame in selected_frames :
            if release_end == "" :
                self.etabs.Frames.assign_release(frame)
            else :
                self.etabs.Frames.assign_release(frame, quick = release_end)
        
        if isSelectAfterAssigning :
            self.etabs.Select.clear()

        self.etabs.refresh()
    
    def torsion_reduction(self, reduction = 0.1, isSelectAfterAssigning = True) :
        self.etabs.model_unlock()    
        frames = self.etabs.Frames.get_name_list(by_unique = True)
        
        # What's beam will be reduced
        prefix = ['B', 'S']

        # Assign Torsion Reduction
        for frame in frames :
            section = self.etabs.Frames.get_section(frame)
            J_orig = self.etabs.Frames.get_modifier(frame)[3]

            if section[0] in prefix and J_orig != reduction :
                self.etabs.Frames.assign_modifier(frame, T = reduction)

        if isSelectAfterAssigning :
            self.etabs.Select.clear()

        # Return
        self.etabs.refresh()

    def set_nonsway(self, isSelectAfterAssigning = True) :
        self.etabs.model_unlock()    
        frames = self.etabs.Frames.get_name_list(by_unique = True)

        # What's beam will be reduced
        frame_prefix = ['F', 'S']

        # Assign Non-Sway
        for frame in frames :
            if self.etabs.Define.Material.get(self.etabs.Frames.get_section(frame))['mat_type'] != 2 :
                # Not Concrete then SKIP
                continue
            
            sect = self.etabs.Frames.get_section(frame)
            frame_type = self.etabs.Design.ConcreteFrame.get_overwrite(frame, 0, quick = 'frame type')

            if (sect[0] in frame_prefix) and (frame_type != 'nonsway') :
                self.etabs.Design.ConcFrame.set_overwrite(frame, 0, 0, quick = 'nonsway')
            elif not (sect[0] in frame_prefix) and (frame_type != 'sway') :
                self.etabs.Design.ConcFrame.set_overwrite(frame, 0, 0, quick = 'sway')
        
        if isSelectAfterAssigning :
            self.etabs.Select.clear()

        # Return
        self.etabs.refresh()

    ## Rules of Definition
    def create_concrete_column(self, column_info) :
        obj = self.etabs.sapModel

        # Column Information
        # BxH, fc, fy, cover
        b = column_info['B']
        h = column_info['H']
        fc = column_info['fc']
        fy = column_info['fy']
        cover = column_info['cover']

        # Define Column Section

        # Return
        

    def create_concrete_beam(self, beam_info, prefix) :
        obj = self.etabs.sapModel

        # Column Information
        # BxH, fc, fy, cover
        b = beam_info['B']
        h = beam_info['H']
        fc = beam_info['fc']
        fy = beam_info['fy']
        cover_top, cover_bot = beam_info['cover']


        # Define Column Section

        # Return

    def change_story_material(self, story_material) :
        #################################
        #
        # story_material = {
        #   story:str : [fc:str, fy_c:str, fy_b:str, fy_sb:str, fy_fb:str]
        # }
        #
        #################################
        
        obj = self.etabs.sapModel

    
