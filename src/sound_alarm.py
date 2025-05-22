from pygame import mixer

class SoundAlarm:
    def __init__(self, sound_path):
        mixer.init()
        self.sound = mixer.Sound(sound_path)

    def play(self):
        try:
            self.sound.play()
        except Exception as e:
            print(f"Error playing sound: {e}")

    def stop(self):
        try:
            self.sound.stop()
        except Exception as e:
            print(f"Error stopping sound: {e}")
