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

