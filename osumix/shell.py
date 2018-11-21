import os
import sys

import click
from pydub import AudioSegment
from slider.beatmap import Beatmap
from ._pydub_util import audioseg_adjust_volume
from .audio import load_sounds
from .track import Track


@click.command(options_metavar='[options]')
@click.argument('input', nargs=1, metavar='<input>')
@click.argument('output', nargs=1, metavar='<output>')
@click.option('--beatmap-sounds', nargs=1, help='beatmap sounds directory', metavar='<dir>')
@click.option('--music', nargs=1, help='music audio', metavar='<file>')
@click.option('--music-volume', nargs=1, type=float, default=1.0, help='music volume (default: 1.0)', metavar='<float>')
def main(input, output, beatmap_sounds, music, music_volume):
    """Compiles a beatmap <input> to an audio file <output>."""
    output_format = os.path.splitext(output)[1][1:]

    bm_audios = load_sounds(beatmap_sounds) if beatmap_sounds else {}

    beatmap = Beatmap.from_path(input)
    track = Track.from_beatmap(beatmap, bm_audios)
    beatmap_audio = track.compile()

    result = beatmap_audio

    if music:
        music_audio = AudioSegment.from_file(music)
        music_audio = audioseg_adjust_volume(music_audio, music_volume)

        result = music_audio.overlay(AudioSegment.silent(24) + result)

    result.export(output, output_format)

    return 0
