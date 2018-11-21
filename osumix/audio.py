import os
from pydub import AudioSegment
from typing import Dict, NamedTuple


class SampleId(NamedTuple):
    sampleset: int
    object_type: str
    sound: int
    index: int

    def __str__(self):
        setname = _sampleset_names[self.sampleset]
        indexname = '' if self.index <= 1 else str(self.index)

        if self.object_type == 'hit':
            soundname = _hitsnd_names[self.sound]
        elif self.object_type == 'slider':
            soundname = _slidersnd_names[self.sound]
        else:
            raise ValueError('must specify hit or slider')

        return f'{setname}-{self.object_type}{soundname}{indexname}'


_sampleset_names = {
    1: 'normal',
    2: 'soft',
    3: 'drum'
}

_hitsnd_names = {
    1: 'normal',
    2: 'whistle',
    4: 'finish',
    8: 'clap'
}

_slidersnd_names = {
    1: 'slide',
    2: 'whistle'
}

sounds: Dict[str, AudioSegment] = {}

_audio_dir = os.path.join(os.path.dirname(__file__), 'audio')
for filename in os.listdir(_audio_dir):
    full_path = os.path.join(_audio_dir, filename)
    sound = AudioSegment.from_file(full_path)
    key = os.path.splitext(filename)[0]
    sounds[key] = sound
