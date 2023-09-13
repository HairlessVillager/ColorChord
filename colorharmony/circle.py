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

        self.value2str = self.__get_value2str()
        self.str2value = self.__get_str2value()

    def __get_value2str(self):
        return {i: '/'.join(s) for i, s in enumerate(self.__octave)}

    def __get_str2value(self):
        res = {}
        for i, notes in enumerate(self.__octave):
            for note in notes:
                res[note] = i
            res['/'.join(notes)] = i
        return res

    def get_note(self, value):
        from .note import Note
        return Note('/'.join(self.__octave[value]))


