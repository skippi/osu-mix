import audioop

from pydub import AudioSegment


def audioseg_adjust_volume(audio: AudioSegment, factor: float):
    return audio._spawn(data=audioop.mul(audio._data, audio.sample_width, factor))
