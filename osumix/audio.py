import os
import re
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from typing import Dict, NamedTuple


SoundRepo = Dict[str, AudioSegment]


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


def load_sounds(directory: str) -> SoundRepo:
    sounds = {}
    snd_filenames = [n for n in os.listdir(
        directory) if _soundfile_re.match(n)]

    for filename in snd_filenames:
        full_path = os.path.join(directory, filename)
        file_format = os.path.splitext(full_path)[1][1:]

        try:
            sound = AudioSegment.from_file(full_path, file_format)
        except CouldntDecodeError:
            print(f'Error: could not open {filename}. Using empty audio.')
            sound = AudioSegment.empty()

        key = os.path.splitext(filename)[0]
        sounds[key] = sound

    return sounds


_soundfile_re = re.compile('.*\\.(?:wav|mp3|flac|pcm)')


default_sounds_path = os.path.join(os.path.dirname(__file__), 'audio')
sounds = load_sounds(default_sounds_path)


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
