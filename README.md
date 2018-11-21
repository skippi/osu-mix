# osumix

A command-line tool for converting beatmaps into audio files.

- Generate audio without recording the osu! client.
- Generate beatmap rhythms without recording the osu! client.
- Automate osu! sound recording with scripts.

## Installation

osumix requires python >=3.4 and ffmpeg. You will also need to install poetry.
Use poetry to build and install the distributable osumix package.

```bash
cd osumix
poetry build
cd dist
pip install <osumix.tar.gz>
```

After the pip installation, osumix should be available from the system path.

## Usage

```txt
Usage: osumix [options] <input> <output>

  Compiles a beatmap <input> to an audio file <output>.

Options:
  --beatmap-sounds <dir>   beatmap sounds directory
  --effect-volume <float>  effect volume (default: 1.0)
  --music <file>           music audio
  --music-volume <float>   music volume (default: 1.0)
  --skin <dir>             skin directory
  --help                   Show this message and exit.
```

## Examples

```bash
# Compile a beatmap with default sounds.
osumix my_beatmap.osu output.wav

# Compile a beatmap with beatmap sounds.
osumix --beatmap-sounds ./180138\ Halozy\ -\ Genryuu\ Kaiko/ my_beatmap.osu output.flac

# Compile a beatmap with skin sounds and to FLAC.
osumix --skin ./yugen my_beatmap.osu output.flac

# Compile a beatmap with beatmap audio.
osumix --music ./Yuaru\ -\ Asu.mp3 my_beatmap.osu output.flac

# Same as above, with tuned volumes.
osumix --music ./Yuaru\ -\ Asu.mp3 --effect-volume 0.5 my_beatmap.osu output.flac
```

## Missing Features

Any of the following are open for discussion:

- Any spinner related sounds are not recorded yet. The decision to implement
  this is debatable, as spinner sounds don't really follow along with the
  song's rhythm.
- Error handling is missing in many areas. Users may often hit exceptions
  depending on usage variance.
- A user-friendly UI. Most osu users are casual computer users, which is one of
  osumix's target demographics. Making a UI shouldn't be hard, but packaging
  dependencies with the UI could be difficult in regards to copyright.
- Extra new ideas that the tool could use.

## Contributing

1. Fork it [here](https://github.com/skippi/osumix/fork)
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request

## Contributors

- [skippi](https://github.com/skippi) - creator, maintainer
