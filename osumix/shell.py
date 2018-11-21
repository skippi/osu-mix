import logging
import os
import sys

import click
from pydub import AudioSegment
from slider.beatmap import Beatmap
from ._pydub_util import audioseg_adjust_volume
from .audio import load_sounds
from .track import Track


@click.command(options_metavar='[options]')
@click.option('--beatmap-sounds', nargs=1, help='beatmap sounds directory', metavar='<dir>')
@click.option('--effect-volume', nargs=1, type=float, default=1.0, help='effect volume (default: 1.0)', metavar='<float>')
@click.option('--music', nargs=1, help='music audio', metavar='<file>')
@click.option('--music-volume', nargs=1, type=float, default=1.0, help='music volume (default: 1.0)', metavar='<float>')
@click.option('--skin', nargs=1, help='skin directory', metavar='<dir>')
@click.argument('input', nargs=1, metavar='<input>')
@click.argument('output', nargs=1, metavar='<output>')
def main(beatmap_sounds, effect_volume, music, music_volume, skin, input, output):
    """Compiles a beatmap <input> to an audio file <output>."""
    output_format = os.path.splitext(output)[1][1:]

    bm_audios = load_sounds(beatmap_sounds) if beatmap_sounds else {}
    skin_audios = load_sounds(skin) if skin else {}

    beatmap = Beatmap.from_path(input)
    track = Track.from_beatmap(beatmap, bm_audios, skin_audios)
    beatmap_audio = track.compile()
    beatmap_audio = audioseg_adjust_volume(beatmap_audio, effect_volume)

    result = beatmap_audio

    if music:
        music_audio = AudioSegment.from_file(music)
        music_audio = audioseg_adjust_volume(music_audio, music_volume)

        result = music_audio.overlay(AudioSegment.silent(24) + result)

    result.export(output, output_format)

    return 0
