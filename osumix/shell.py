import os
import sys

import click
from pydub import AudioSegment
from slider.beatmap import Beatmap
from .audio import load_sounds
from .track import Track


@click.command(options_metavar='[options]')
@click.argument('input', nargs=1, metavar='<input>')
@click.argument('output', nargs=1, metavar='<output>')
@click.option('--audio', nargs=1, help='music audio', metavar='<file>')
@click.option('--beatmap-sounds', nargs=1, help='beatmap sounds directory', metavar='<file>')
def main(input, output, audio, beatmap_sounds):
    """Compiles a beatmap <input> to an audio file <output>."""
    output_format = os.path.splitext(output)[1][1:]

    bm_audios = load_sounds(beatmap_sounds) if beatmap_sounds else {}

    beatmap = Beatmap.from_path(input)
    track = Track.from_beatmap(beatmap, bm_audios)
    beatmap_audio = track.compile()

    result = beatmap_audio

    if audio:
        music_audio = AudioSegment.from_file(audio)
        result = music_audio.overlay(AudioSegment.silent(24) + result)

    result.export(output, output_format)

    return 0
