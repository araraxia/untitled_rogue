


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
        self.log.debug("Initializing character creation menu.")
        self.create_character()

    def create_character(self):
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