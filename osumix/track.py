
import audioop
import math
from datetime import timedelta
from typing import List, NamedTuple, Tuple

from pydub import AudioSegment
from slider.beatmap import (Beatmap, Circle, Slider, TimingPoint)
from . import audio


class Note(NamedTuple):
    sound: AudioSegment
    timestamp: timedelta
    volume: float = 1.0


class Track(NamedTuple):
    notes: List[Note] = []

    @classmethod
    def from_beatmap(cls, beatmap: Beatmap):
        new_notes = []
        for obj in beatmap.hit_objects:
            tp = beatmap.timing_point_at(obj.time)

            if isinstance(obj, Slider):
                new_notes.extend(_slider2notes(obj, tp))
            else:
                new_notes.extend(_circle2notes(obj, tp))

        return cls(new_notes)

    def compile(self) -> AudioSegment:
        result = AudioSegment.empty()
        result._data = bytearray(result._data)

        for note in self.notes:
            if len(note.sound) == 0:
                continue

            sync_result, note_snd = AudioSegment._sync(result, note.sound)
            if not sync_result is result:
                result = sync_result
                result._data = bytearray(result._data)

            db_gain = 10 * math.log2(note.volume)
            note_snd = note_snd + db_gain

            time_ms = note.timestamp.total_seconds() * 1000
            byte_offset = result._parse_position(time_ms) * result.frame_width
            new_data = note_snd._data
            min_len = byte_offset + len(new_data)

            if len(result._data) < min_len:
                result._data += bytearray(min_len - len(result._data))

            cur_data = result._data[byte_offset:min_len]
            mixed_data = audioop.add(cur_data, new_data, result.sample_width)

            result._data[byte_offset:min_len] = mixed_data

        return result


def _circle2notes(circle: Circle, tp: TimingPoint) -> List[Note]:
    (sampleset, additionset, sampleindex) = _parse_addition(circle.addition, tp)

    hitsnds = _fetch_sounds(sampleset, additionset, 'hit',
                            circle.hitsound, sampleindex)
    notes = [Note(s, circle.time, tp.volume / 100) for s in hitsnds]
    return notes


def _slider2notes(slider: Slider, tp: TimingPoint) -> List[Note]:
    (sampleset, additionset, sampleindex) = _parse_addition(slider.addition, tp)

    duration = slider.end_time - slider.time
    edge_period = duration / slider.repeat

    notes = []
    for n in range(slider.repeat + 1):
        edge_sndbits = slider.hitsound
        if len(slider.edge_sounds) > n:
            edge_sndbits = slider.edge_sounds[n]

        edge_sampleset = 0
        edge_additionset = 0
        if len(slider.edge_additions) > n:
            add_pair = slider.edge_additions[n].split(":")
            edge_sampleset = int(add_pair[0])
            edge_additionset = int(add_pair[1])

        if edge_sampleset == 0:
            edge_sampleset = sampleset
        if edge_additionset == 0:
            edge_additionset = additionset

        edge_snds = _fetch_sounds(
            edge_sampleset, edge_additionset, 'hit', edge_sndbits, sampleindex)
        edge_time = slider.time + (edge_period * n)

        edge_notes = [Note(s, edge_time, tp.volume / 100) for s in edge_snds]

        notes.extend(edge_notes)

    if len(slider.edge_sounds) > n:
        base_slide_snds = _fetch_sounds(
            sampleset, additionset, 'slider', slider.hitsound, sampleindex)
    else:
        base_slide_snds = _fetch_sounds(
            sampleset, additionset, 'slider', 1, sampleindex)

    slide_snds = []
    for s in base_slide_snds:
        canvas = AudioSegment.silent(duration.total_seconds() * 1000)
        slide_snds.append(canvas.overlay(s, loop=True))

    slide_notes = [Note(s, slider.time, tp.volume / 100) for s in slide_snds]
    notes.extend(slide_notes)

    return notes


def _parse_addition(addition: str, tp: TimingPoint) -> Tuple[int, int, int]:
    additions = addition.split(":")

    sampleset = int(additions[0])
    if sampleset == 0:
        sampleset = tp.sample_type

    additionset = int(additions[1])
    if additionset == 0:
        additionset = sampleset

    sampleindex = int(additions[2])
    if sampleindex == 0:
        sampleindex = tp.sample_set

    return (sampleset, additionset, sampleindex)


def _fetch_sounds(sampleset: int, additionset: int, obj_type: str, sndbits: int, index: int):
    if obj_type == 'hit':
        sounds = [1] + [n for n in [2, 4, 8] if sndbits & n == n]
    else:
        sounds = [1] + [n for n in [2] if sndbits & n == n]

    sampleids = []
    for s in sounds:
        used_set = sampleset if s == 1 else additionset
        sampleids.append(audio.SampleId(used_set, obj_type, s, index))

    hitsnds = []
    for id in sampleids:
        temp = audio.SampleId(id.sampleset, id.object_type, id.sound, 0)
        hitsnd = audio.sounds.get(str(temp), AudioSegment.empty())
        # if sampleindex != 0 and name in self.custom_hitsounds:
        #     hitsnd = self.custom_hitsounds[name]

        hitsnds.append(hitsnd)

    return hitsnds
