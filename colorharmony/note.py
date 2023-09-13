from .const import CIRCLE_1, CIRCLE_5


class Note:
    # TODO: English translation
    """ 色彩和声理论中的音符。

    这些音符都十二平均律中，并且按照五度圈排列，具体顺序为`B` `E` `A` `D` `G` `C` `F` `A#/Bb` `D#/Eb` `G#/Ab` `C#/Db` `F#/Gb`。

    `Note`没有音高，`C4`和`C5`将被视为同一个`Note`。

    Attributes
    ----------
    __value : int
        在 C 大调中的位置，从 0 开始。
    """

    def __init__(self, value):
        if isinstance(value, str):
            if value in CIRCLE_1.str2value.keys():
                self.__value = CIRCLE_1.str2value[value]
            else:
                raise ValueError(
                    f"expected value in "
                    f"{list(CIRCLE_1.str2value.keys())}, "
                    f"got {value}"
                )
        elif isinstance(value, int):
            if 0 <= value < 12:
                self.__value = value
            else:
                raise ValueError(
                    f"expected value in range(0, 12), got {value}"
                )
        else:
            raise TypeError(f"unsupported type: {type(value)}")

    def __str__(self):
        return f'"{CIRCLE_1.value2str[self.__value]}"({self.__value})'

    def __repr__(self):
        return f"<Note {str(self)}>"

    def value(self):
        return self.__value

    def name(self):
        return CIRCLE_1.value2str[self.__value]

    def interval_1_to(self, other):
        if not isinstance(other, Note):
            raise TypeError(f"expected Note, got {type(other)}")
        return self.__interval_to(other, step=1)

    def interval_5_to(self, other):
        if not isinstance(other, Note):
            raise TypeError(f"expected Note, got {type(other)}")
        return self.__interval_to(other, step=5)

    def __interval_to(self, other, step):
        """
        Notes
        -----
        使用了乘法逆元，mod 12 时，x 的逆元是 x 自身。
        """
        return (self.__value - other.__value) * step % 12

    def next_1(self, step=1):
        if not isinstance(step, int):
            raise TypeError(f"expected int, got {type(step)}")
        if not (0 <= step < 12):
            raise ValueError(f"expected step in range(0, 12), got {step}")
        return self.__next(step * 1)

    def next_5(self, step=1):
        if not isinstance(step, int):
            raise TypeError(f"expected int, got {type(step)}")
        if not (0 <= step < 12):
            raise ValueError(f"expected step in range(0, 12), got {step}")
        return self.__next(step * 5)

    def __next(self, step):
        value = (self.__value + step) % 12
        return Note(value)

    def __eq__(self, other):
        return self.__value == other.__value

