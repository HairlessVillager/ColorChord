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

        self.__notes = sorted(list(set(self.__notes)))
        if len(self.__notes) < 2:
            raise ValueError(f"expected length >= 2, got {len(self.__notes)}")

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

    def __hash__(self):
        return hash(tuple(self.__notes))

    def angle_5(self, base_note=Note("C")):
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

        这里采用一套比较简单的方法计算协和度。
        统计和弦中各个音程的数量，赋予其权重，计算加权平均值得到协和度。

        完全协和音程：纯四度、纯五度
        不完全协和音程：大小三度、大小六度
        不协和音程：大小二度、大小七度、增减、倍增减

        例如：对于 C 大三和弦`[0, 4, 7]`，(0, 4)为大三度，(4, 7)为小三度，
        (7, 0)为纯四度，计算加权平均值得协和度为 5.33
        """
        # TODO: 另请参考：《色彩和声》第352页“谱例7-4 和弦紧张度等级划分细则”
        interval_weights = [
            0,     # 0  纯一度，占位用
            0,     # 1  小二度
            0,     # 2  大二度
            4,     # 3  小三度
            4,     # 4  大三度
            8,     # 5  纯四度
            0,     # 6  增四度/减五度
            8,     # 7  纯五度
            4,     # 8  小六度
            4,     # 9  大六度
            0,     # 10 小七度
            0,     # 11 大七度
        ]
        interval_counts = \
            [self.count_1(_) for _ in range(len(interval_weights))]
        assert interval_counts[0] == 0
        return sum(map(lambda x, y: x*y,
                       interval_counts,
                       interval_weights)) / sum(interval_counts)

    def count_1(self, pattern):
        if isinstance(pattern, int):
            if pattern == 0:
                return 0
            else:
                pattern = [0, pattern]
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
