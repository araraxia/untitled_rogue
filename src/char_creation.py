
class CharCreator:
    def __init__(self, root):
        self.root = root
        self.log = root.logger
        self.conf = root.conf
        self.init_menu()
        
    def init_menu(self):
        ...
        
        
class CharMenu(CharCreator):
    def __init__(self, root):
        self.root = root
        self.log = root.logger
        self.window_width = self.root.window_width
        self.window_height = self.root.window_height
        self.init_menu()
        self.log.debug("Initializing character creation menu.")
        
    def init_menu(self):
        self.frame_width = int(self.window_width * 0.4)
        self.frame_height = int(self.window_height * 0.8)
        
        self.frame_cent_pos = (
            (self.window_width * .5) // 2,
            self.window_height // 2
        )
        
        self.log.debug("Frame dimensions: %dx%d at position %s",
                        self.frame_width, self.frame_height, self.frame_cent_pos)
        self.root.helper.create_frame(
            self.root,
            
        )

    def choose_race(self):
        self.log.debug("Creating character.")
        
        
        
        pass
    
class CharStatWindow(CharCreator):
    def __init__(self, root):
        self.root = root
        self.log = root.logger
        self.log.debug("Initializing character stats window.")
        self.create_stats_window()

    def create_stats_window(self):
        self.log.debug("Creating character stats window.")
        
        pass  # Implement the logic to create the character stats window

class CharImageWindow(CharCreator):
    def __init__(self, root):
        self.root = root
        self.log = root.logger
        self.log.debug("Initializing character image window.")
        self.create_image_window()

    def create_image_window(self):
        self.log.debug("Creating character image window.")
        
        pass  # Implement the logic to create the character image window