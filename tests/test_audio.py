import os

import osumix.audio as audio


def test_load_sounds():
    observed = audio.load_sounds(audio.default_sounds_path)
    filenames = [n for n in os.listdir(
        audio.default_sounds_path) if n.endswith('.wav')]
    soundnames = [os.path.splitext(n)[0] for n in filenames]
    for n in soundnames:
        assert n in observed
