import itertools
import math
import random

from .note import Note
from .chord import Chord


class Container:

    def __init__(self, notes=None, chords=None, seed=None):
        self.__chords = set()
        if notes is not None:
            notes = list(map(lambda x: Note(x), notes))
            for num in range(2, len(notes)+1):
                for notes_ in itertools.combinations(notes, num):
                    self.__chords.add(Chord(notes_))
        if chords is not None:
            for chord in chords:
                self.__chords.add(chord)
        self.__random = random.Random(seed)

    def chords(self):
        return self.__chords.copy()

    def add(self, chord):
        self.__chords.add(chord)

    def remove(self, chord):
        self.__chords.remove(chord)

    def add_by_notes(self, notes, num):
        notes = list(map(lambda x: Note(x), notes))
        for notes in itertools.combinations(notes, num):
            self.__chords.add(Chord(notes))

    def infer(self, chord, color, tension, temperature=0.05):
        def key(chord2):
            r1, theta1 = chord.harmony(), chord.angle_5()
            r2, theta2 = chord2.harmony(), chord2.angle_5()
            x1 = r1 * math.cos(theta1)
            y1 = r1 * math.sin(theta1)
            x2 = r2 * math.cos(theta2)
            y2 = r2 * math.sin(theta2)
            return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        chords = sorted(self.__chords, key=key)

        # `+1` for not return []
        return self.__random.choice(chords[:int(temperature*len(chords))+1])

    def __str__(self):
        return '; '.join([str(_) for _ in self.__chords])

    def __repr__(self):
        return f"<Container {self.__str__()}>"

