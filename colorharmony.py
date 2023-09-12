import musicpy


class Circle:
    """ Circle of notes. """

    octave = [
        ["C"],
        ["C#", "Db"],
        ["D"],
        ["D#", "Eb"],
        ["E"],
        ["F"],
        ["F#", "Gb"],
        ["G"],
        ["G#", "Ab"],
        ["A"],
        ["A#", "Bb"],
        ["B"],
    ]

    def __init__(self, offset=0, interval=1):
        if not isinstance(interval, int):
            raise TypeError(f"expected int, got {type(interval)}")
        if not isinstance(offset, int):
            raise TypeError(f"expected int, got {type(offset)}")
        if not (0 <= offset < 12) :
            raise ValueError(f"expected offset in range(0, 12), got {offset}")

        self.__octave = []
        i = offset
        for _ in range(12):
            self.__octave.append(self.octave[i])
            i += interval
            i %= 12

    def value2str(self):
        return {i: '/'.join(s) for i, s in enumerate(self.__octave)}

    def str2value(self):
        res = {}
        for i, notes in enumerate(self.__octave):
            for note in notes:
                res[note] = i
            res['/'.join(notes)] = i
        return res


circle_of_fifths = Circle(offset=11, interval=5)
value2str = circle_of_fifths.value2str()
str2value = circle_of_fifths.str2value()

class Note:
    # TODO: English translation
    """ 色彩和声理论中的音符。

    这些音符都十二平均律中，并且按照五度圈排列，具体顺序为`B` `E` `A` `D` `G` `C` `F` `A#/Bb` `D#/Eb` `G#/Ab` `C#/Db` `F#/Gb`。

    `Note`没有音高，`C4`和`C5`将被视为同一个`Note`。
    """

    def __init__(self, value):
        if isinstance(value, int):
            if 0 <= value < 12:
                self.__value = value
            else:
                raise ValueError(f"expected value in range(12), got {value}")
        elif isinstance(value, str):
            if value in str2value.keys():
                self.__value = str2value[value]
            else:
                raise ValueError(f"expected value in {str2value.keys()}, got {value}")
        else:
            raise TypeError(f"unsupported type: {type(value)}")

    def __str__(self):
        return f'{self.__value}: "{value2str[self.__value]}"'

    def __repr__(self):
        return f"<Note {str(self)}>"

    def value(self):
        return self.__value

    def name(self):
        return value2str[self.__value]

    def interval_to(self, other):
        return self.__value - other.__value

    def next(self, num=1):
        if not isinstance(num, int):
            raise TypeError(f"expected int, got {type(num)}")
        value = (self.__value + num) % 12
        return Note(value)

    def __sub__(self, other):
        return self.interval_to(other)

    def __gt__(self, other):
        return self.interval_to(other) > 0

    def __lt__(self, other):
        return self.interval_to(other) < 0

    def __eq__(self, other):
        return self.interval_to(other) == 0


class Chord:

    def __init__(self, notes):
        notes = notes.copy()
        if not isinstance(notes, list):
            raise TypeError(f"expected list, got {type(notes)}")
        for i in range(len(notes)):
            if isinstance(notes[i], Note):
                pass
            elif isinstance(notes[i], int|str):
                notes[i] = Note(notes[i])
            else:
                raise TypeError(f"expected int or Note, got {type(notes[i])}")
        self.__notes = notes

    def values(self):
        return [_.value() for _ in self.__notes]

    def __str__(self):
        return '; '.join([str(_) for _ in self.__notes])

    def __repr__(self):
        return f"<Chord {str(self)}>"

    def avg_value(self):
        return sum(self.values()) / len(self.values())
