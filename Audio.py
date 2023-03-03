import wave
from pydub import AudioSegment
import simpleaudio

nonoutput = ["gameMusic","fanfare","singleStep","groupStep","denyStep"]
class Audio:
    def __init__(self,filepath ):
        fullpath = f"sounds/output/{filepath}"

        if filepath not in nonoutput:
            sound = AudioSegment.from_mp3(f"{fullpath}.mp3")
            sound.export(f"{fullpath}.wav", format="wav")
            self.player = wave.open(f"{fullpath}.wav", 'rb')
        else  :
            self.player = wave.open(f"sounds/{filepath}.wav", 'rb')

        self.playAudio = simpleaudio.WaveObject.from_wave_read(self.player)

    def play(self ):
        self.playAudio.play()


    def stop(self):
         self.playAudio = simpleaudio.stop_all()

