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

        self.__value2str = ['/'.join(s) for s in self.__octave]
        self.__str2value = self.__get_str2value()
        self.keys = list(self.__value2str.copy())
        self.available_keys = list(self.__str2value.keys())

    def __get_str2value(self):
        res = {}
        for i, notes in enumerate(self.__octave):
            for note in notes:
                res[note] = i
            res['/'.join(notes)] = i
        return res

    def value2str(self, v):
        return self.__value2str[v]

    def str2value(self, s):
        return self.__str2value[s]

    def get_note(self, index):
        from .note import Note
        return Note('/'.join(self.__octave[index]))

CIRCLE_1 = Circle(offset=0, interval=1)
CIRCLE_5 = Circle(offset=0, interval=5)

