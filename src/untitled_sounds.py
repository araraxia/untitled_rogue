
import os

class UntitledSounds:
    def __init__(self, root, name):
        self.root = root
        self.log = root.logger
        self.conf = root.config
        
        self.name = name
        
    def load_sound(self):
        mapping = {
            "example_name": "example_sound.wav",
        }
        sound_path = os.path.join("sounds", mapping.get(self.name, "default_sound.wav"))
        with open(sound_path, 'rb') as sound_file:
            sound_data = sound_file.read()
            self.log.debug(f"Loaded sound: {self.name} from {sound_path}")
            
        self.data = sound_data