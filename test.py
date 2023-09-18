import unittest
import itertools

from colorharmony import Circle, Note, Chord, Container
from colorharmony.circle import CIRCLE_1, CIRCLE_5


class TestNote(unittest.TestCase):

    cases_1 = [
        [Note("C"), 1, Note("C#/Db")],
        [Note("F#/Gb"), 1, Note("G")],
        [Note("B"), 1, Note("C")],
        [Note("C"), 2, Note("D")],
        [Note("F"), 5, Note("A#/Bb")],
        [Note("A"), 8, Note("F")],
    ]
    cases_5 = [
        [Note("C"), 1, Note("F")],
        [Note("F#/Gb"), 1, Note("B")],
        [Note("B"), 1, Note("E")],
        [Note("C"), 2, Note("A#/Bb")],
        [Note("F"), 5, Note("F#/Gb")],
        [Note("A"), 8, Note("C#/Db")],
    ]

    def test_init(self):
        self.assertNotEqual(Note(1), Note(0))
        self.assertNotEqual(Note(11), Note(5))

        unsupported_ints = [
            -1,
            -2,
            13,
        ]
        for v in unsupported_ints:
            with self.assertRaises(ValueError):
                Note(v)

        self.assertTrue(Note("C#") == Note("Db") == Note("C#/Db"))
        self.assertTrue(Note("F#") == Note("Gb") == Note("F#/Gb"))
        self.assertNotEqual(Note("C"), Note("G"))
        self.assertNotEqual(Note("A"), Note("A#"))

        unsupported_strs = [
            "H",
            "I",
            "Csharp",
        ]
        for v in unsupported_strs:
            with self.assertRaises(ValueError):
                Note(v)

        unsupported_type_instances = [
            1.2,
        ]
        for v in unsupported_type_instances:
            with self.assertRaises(TypeError):
                Note(v)

    def test_repr(self):
        for i, s in enumerate(CIRCLE_1.keys):
            self.assertEqual(Note(s).__repr__(), f'<Note "{s}"({i})>')

    def test_interval_1_to(self):
        for (i1, s1), (i2, s2) in itertools.product(
                enumerate(CIRCLE_1.keys),
                repeat=2):
            n1 = Note(s1)
            n2 = Note(s2)
            try:
                self.assertEqual(n1.interval_1_to(n2), (i1 - i2) % 12)
            except AssertionError as e:
                e.add_note(f"{n1=}, {n2=}, {i1=}, {i2=}")
                e.add_note(f"{n1.interval_1_to(n2)=}, {(i1 - i2) % 12=}")
                raise

    def test_interval_5_to(self):
        circle_5 = Circle(offset=0, interval=5)
        for (i1, s1), (i2, s2) in itertools.product(
                enumerate(circle_5.keys),
                repeat=2):
            n1 = Note(s1)
            n2 = Note(s2)
            try:
                self.assertEqual(n1.interval_5_to(n2), (i1 - i2) % 12)
            except AssertionError as e:
                e.add_note(f"{n1=}, {n2=}, {i1=}, {i2=}")
                e.add_note(f"{n1.interval_1_to(n2)=}, {(i1 - i2) % 12=}")
                raise

    def test_eq(self):
        for v1, v2 in itertools.product(CIRCLE_5.keys, repeat=2):
            n1 = Note(v1)
            n2 = Note(v2)
            try:
                self.assertEqual(n1 == n2, v1 == v2)
            except AssertionError as e:
                e.add_note(f"{n1=}, {n2=}, {v1=}, {v2=}")
                raise

    def test_next_1(self):
        for note0, n, note in self.cases_1:
            self.assertEqual(note0.next_1(n), note)

        with self.assertRaises(ValueError):
            Note("C").next_1(13)

    def test_next_5(self):
        for note0, n, note in self.cases_5:
            self.assertEqual(note0.next_5(n), note)

        with self.assertRaises(ValueError):
            Note("C").next_5(13)

    # TODO: test to_musicpy_note


class TestCircle(unittest.TestCase):

    circle = Circle(offset=11, interval=5)
    str2value = {'B': 0, 'E': 1, 'A': 2, 'D': 3, 'G': 4, 'C': 5, 'F': 6, 'A#': 7, 'Bb': 7, 'A#/Bb': 7, 'D#': 8, 'Eb': 8, 'D#/Eb': 8, 'G#': 9, 'Ab': 9, 'G#/Ab': 9, 'C#': 10, 'Db': 10, 'C#/Db': 10, 'F#': 11, 'Gb': 11, 'F#/Gb': 11}
    value2str = {0: 'B', 1: 'E', 2: 'A', 3: 'D', 4: 'G', 5: 'C', 6: 'F', 7: 'A#/Bb', 8: 'D#/Eb', 9: 'G#/Ab', 10: 'C#/Db', 11: 'F#/Gb'}

    def test_init(self):
        self.assertEqual(self.circle.keys, list(self.value2str.values()))
        self.assertEqual(self.circle.available_keys, list(self.str2value.keys()))

    def test_value2str(self):
        for i, s in self.value2str.items():
            self.assertEqual(self.circle.value2str(i), s)

    def test_str2value(self):
        for s, v in self.str2value.items():
            self.assertEqual(self.circle.str2value(s), v)

    def test_get_note(self):
        for v in range(12):
            n1 = self.circle.get_note(v)
            n2 = Note(self.value2str[v])
            self.assertEqual(n1, n2)

class TestChord(unittest.TestCase):
    cases = []
    cases.append([
        [1, 4, 6],
        [Note(1), Note(4), Note(6)],
        [1, Note(4), Note(6)],
        [Note(1), Note(4), 6],
    ])
    cases.append([
        [5, 7, 2, 11],
        [Note(5), Note(7), Note(2), Note(11)],
        [5, Note(7), 2, Note(11)],
        [Note(5), 7, Note(2), 11],
    ])
    cases.append([
        [0, 11],
        [Note(0), Note(11)],
        [0, Note(11)],
        [Note(0), 11],
    ])
    cases.append([
        list(range(12)),
        [Note(_) for _ in range(12)],
    ])
    cases.append([
        [0, 1, 2, 3, 4],
        [0, 1, 1, 2, 2, 3, 3, 4, 4],
        [0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 4],
        [4, 3, 2, 1, 0],
        [1, 1, 4, 5 -1, 4, 0, 2, 3],
    ])

    def test_init(self):
        Chord([0, 3, 5])
        Chord({0, 3, 5})
        Chord(range(0, 12, 3))
        self.assertEqual(Chord([0, 3, 5]), Chord([5, 0, 3]))

        for case_ in self.cases:
            for i in range(1, len(case_)):
                self.assertEqual(
                    Chord(case_[0]).values(),
                    Chord(case_[i]).values()
                )

        with self.assertRaises(TypeError):
            Chord([1.2, 2.3, 3.4])

    def test_value(self):
        for case_ in self.cases:
            for i in range(1, len(case_)):
                self.assertEqual(
                    Chord(case_[i]).values(),
                    sorted(case_[0])
                )

    def test_repr(self):
        v = [0, 4, 7]
        s = '<Chord "C E G"(0, 4, 7)>'
        self.assertEqual(Chord(v).__repr__(), s)

    def test_angle_5(self):
        chord = Chord([Note("F"), Note("C"), Note("G")])
        self.assertEqual(chord.angle_5(Note("C")), (11 + 0 + 1) / 3)

    def test_count_1(self):
        chord = Chord(range(12))
        for interval in range(1, 12):
            self.assertEqual(chord.count_1(interval), 12)
            self.assertEqual(chord.count_1([0, interval]), 12)

        chord = Chord([0, 1, 2, 3, 5, 7, 11])
        self.assertEqual(chord.count_1([0, 1, 2]), 3)
        self.assertEqual(chord.count_1([2, 3, 5]), 3)
        self.assertEqual(chord.count_1([1, 2, 4]), 3)
        self.assertEqual(chord.count_1([0, 2, 4, 6, 8, 10]), 0)

        self.assertEqual(chord.count_1(Chord([2, 3, 5])), chord.count_1([2, 3, 5]))

        with self.assertRaises(ValueError):
            chord.count_1([9, 10, 11, 12, 13])

    def test_harmony(self):
        cases = [
            [[0, 4, 7], 16 / 3],
            [[1, 5, 8], 16 / 3],
            [[2, 6, 9], 16 / 3],
            [[0, 2, 7, 11], 24 / 6],
            [[0, 1, 4, 7], 20 / 6],
        ]
        for v, h in cases:
            self.assertEqual(Chord(v).harmony(), h)


class TestContainer(unittest.TestCase):

    def test_init(self):
        self.assertEqual(Container().chords(), set())
        chords = {
            Chord([0, 4, 7]),
            Chord([2, 5, 8]),
            Chord([1, 3, 5, 7]),
        }
        self.assertEqual(Container(chords=chords).chords(), chords)

    def test_add(self):
        chord = Chord([0, 1, 2])
        container = Container()
        container.add(chord)
        self.assertIn(chord, container.chords())

    def test_remove(self):
        chord = Chord([0, 1, 2])
        container = Container(notes=[0, 1, 2])
        container.remove(chord)
        self.assertNotIn(chord, container.chords())

    def test_add_by_notes(self):
        container = Container()
        container.add_by_notes([0, 2, 4, 5, 7, 9, 11], 3)
        self.assertEqual(container.chords(),
            {
                Chord((0, 2, 4)), Chord((0, 2, 5)), Chord((0, 2, 7)),
                Chord((0, 2, 9)), Chord((0, 2, 11)), Chord((0, 4, 5)),
                Chord((0, 4, 7)), Chord((0, 4, 9)), Chord((0, 4, 11)),
                Chord((0, 5, 7)), Chord((0, 5, 9)), Chord((0, 5, 11)),
                Chord((0, 7, 9)), Chord((0, 7, 11)), Chord((0, 9, 11)),
                Chord((2, 4, 5)), Chord((2, 4, 7)), Chord((2, 4, 9)),
                Chord((2, 4, 11)), Chord((2, 5, 7)), Chord((2, 5, 9)),
                Chord((2, 5, 11)), Chord((2, 7, 9)), Chord((2, 7, 11)),
                Chord((2, 9, 11)), Chord((4, 5, 7)), Chord((4, 5, 9)),
                Chord((4, 5, 11)), Chord((4, 7, 9)), Chord((4, 7, 11)),
                Chord((4, 9, 11)), Chord((5, 7, 9)), Chord((5, 7, 11)),
                Chord((5, 9, 11)), Chord((7, 9, 11)),
            }
        )

        container = Container()
        container.add_by_notes([0, 3, 6, 9], 2)
        container.add_by_notes([0, 3, 6, 9], 3)
        container.add_by_notes([0, 3, 6, 9], 4)
        self.assertEqual(container.chords(),
            {
                Chord((0, 3)), Chord((0, 6)), Chord((0, 9)),
                Chord((3, 6)), Chord((3, 9)), Chord((6, 9)),
                Chord((0, 3, 6)), Chord((0, 3, 9)), Chord((0, 6, 9)),
                Chord((3, 6, 9)), Chord((0, 3, 6, 9)),
            }
        )

    def test_infer(self):
        raise NotImplementedError


if __name__ == "__main__":
    unittest.main()