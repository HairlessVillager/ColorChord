import unittest
import itertools

from colorharmony import Circle, Note
from colorharmony.const import CIRCLE_1, CIRCLE_5

str2value = CIRCLE_5.str2value
value2str = CIRCLE_5.value2str

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

    def test_init_with_int(self):
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

    def test_init_with_str(self):
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

    def test_init_in_unexpected_type(self):
        unsupported_type_instances = [
            1.2,
        ]
        for v in unsupported_type_instances:
            with self.assertRaises(TypeError):
                Note(v)

    def test_repr(self):
        for v, s in CIRCLE_1.value2str.items():
            self.assertEqual(Note(s).__repr__(), f'<Note "{s}"({v})>')

    def test_interval_1_to(self):
        circle_1 = Circle(offset=0, interval=1)
        for (i1, s1), (i2, s2) in itertools.product(
                enumerate(circle_1.value2str.values()),
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
                enumerate(circle_5.value2str.values()),
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
        for v1, v2 in itertools.product(CIRCLE_5.value2str.values(), repeat=2):
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
        self.assertEqual(self.circle.str2value, self.str2value)
        self.assertEqual(self.circle.value2str, self.value2str)

    def test_get_note(self):
        for v in range(12):
            n1 = self.circle.get_note(v)
            n2 = Note(self.value2str[v])
            self.assertEqual(n1, n2)

class TestChord(unittest.TestCase):
    pass
    # cases = []
    # cases.append([
    #     [1, 4, 6],
    #     [Note(1), Note(4), Note(6)],
    #     [1, Note(4), Note(6)],
    #     [Note(1), Note(4), 6],
    # ])
    # cases.append([
    #     [5, 7, 2, 11],
    #     [Note(5), Note(7), Note(2), Note(11)],
    #     [5, Note(7), 2, Note(11)],
    #     [Note(5), 7, Note(2), 11],
    # ])
    # cases.append([
    #     [0, 11],
    #     [Note(0), Note(11)],
    #     [0, Note(11)],
    #     [Note(0), 11],
    # ])
    # cases.append([
    #     list(range(12)),
    #     [Note(_) for _ in range(12)],
    # ])

    # def test_init_without_exception(self):
    #     for case_ in self.cases:
    #         for i in range(1, len(case_)):
    #             self.assertEqual(
    #                 Chord(case_[0]).values(),
    #                 Chord(case_[i]).values()
    #             )

    # def test_init_with_exception(self):
    #     with self.assertRaises(TypeError):
    #         Chord([1.2, 2.3, 3.4])

    # def test_value(self):
    #     for case_ in self.cases:
    #         for i in range(1, len(case_)):
    #             self.assertEqual(
    #                 Chord(case_[i]).values(),
    #                 case_[0]
    #             )

    # def test_repr(self):
    #     v = [5, 1, 4]
    #     s = '<Chord 5: "C"; 1: "E"; 4: "G">'
    #     self.assertEqual(Chord(v).__repr__(), s)

    # def test_avg_value(self):
    #     v = [5, 1, 4]
    #     avg_value = sum(v) / len(v)
    #     self.assertEqual(Chord(v).avg_value(), avg_value)


if __name__ == "__main__":
    unittest.main()