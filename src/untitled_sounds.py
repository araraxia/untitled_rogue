
import os, io, pygame

class UntitledSounds:
    def __init__(self, root, name: str="example_name"):
        self.root = root
        self.log = root.logger
        self.conf = root.config
        self.sound = None
        self.name = name
        self.load_sound()
        
    def load_sound(self):
        mapping = self.root.audio_map
        sound_path = os.path.join("sounds", mapping.get(self.name, "default_sound.wav"))
        with open(sound_path, 'rb') as sound_file:
            sound_data = sound_file.read()
            self.log.debug(f"Loaded sound: {self.name} from {sound_path}")
        sound_io = io.BytesIO(sound_data)
        self.sound = pygame.mixer.Sound(sound_io)