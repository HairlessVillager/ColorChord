from . import Note


class Chord:

    def __init__(self, notes):
        self.__notes = []
        for elem in notes:
            if isinstance(elem, Note):
                pass
            elif isinstance(elem, int|str):
                elem = Note(elem)
            else:
                raise TypeError(f"expected int or Note, got {type(elem)}")
            self.__notes.append(elem)
        self.__notes.sort()

    def values(self):
        return [_.value() for _ in self.__notes]

    def __iter__(self):
        return iter(self.values())

    def __str__(self):
        return f'"{" ".join([_.name() for _ in self.__notes])}"' \
               f'({", ".join([str(_.value()) for _ in self.__notes])})'

    def __repr__(self):
        return f"<Chord {str(self)}>"

    def __eq__(self, other):
        return self.__notes == other.__notes

    def angle(self, base_note=Note("C")):
        """ 和弦方向。

        将和弦中的所有音符在五度圈中的角度取平均值。
        """
        if not isinstance(base_note, Note):
            raise TypeError(f"expected Note, got {type(base_note)}")
        notes_in_circle_5 = list(map(lambda x: x.interval_5_to(base_note),
                                     self.__notes))
        return sum(notes_in_circle_5) / len(notes_in_circle_5)

    def harmony(self):
        """ 和弦协和度。

        将和弦归类为 I~X 十类三十小类，从而得到协和度。

        半音数量越多，协和度越低。

        另请参考：《色彩和声》第352页“谱例7-4 和弦紧张度等级划分细则”
        """
        raise

    def count_1(self, pattern):
        if isinstance(pattern, int):
            pattern = [0, pattern]
        else:
            pattern = Chord(pattern).values()
        assert isinstance(pattern, list)

        if len(self.__notes) < len(pattern):
            return 0

        pattern = list(map(lambda x: x - min(pattern), pattern))
        length = len(self.__notes)
        note_values = [_.value() for _ in self.__notes]
        counter = 0
        for offset in range(12):
            offseted_pattern = map(lambda x: (x + offset) % 12, pattern)
            if all((_ in note_values) for _ in offseted_pattern):
                counter += 1
        return counter

    def count_5(self, pattern):
        raise NotImplementedError
