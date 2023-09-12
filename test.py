import unittest
import itertools

from colorharmony import Circle, Note, Chord, str2value, value2str


class TestNote(unittest.TestCase):

    def test_init_with_str(self):
        for s, v in str2value.items():
            self.assertEqual(Note(s).value(), v)

        unsupported_strs = [
            "H",
            "I",
            "Csharp",
        ]
        for v in unsupported_strs:
            with self.assertRaises(ValueError):
                Note(v)

    def test_init_with_int(self):
        for v in range(12):
            self.assertEqual(Note(v).value(), v)

        unsupported_ints = [
            13,
            20,
            -1,
        ]
        for v in unsupported_ints:
            with self.assertRaises(ValueError):
                Note(v)


    def test_init_in_unexpected_type(self):
        unsupported_type_instances = [
            1.2,
        ]
        for v in unsupported_type_instances:
            with self.assertRaises(TypeError):
                Note(v)

    def test_value(self):
        for v in range(12):
            self.assertEqual(Note(v).value(), v)

    def test_name(self):
        for v, s in value2str.items():
            self.assertEqual(Note(v).name(), s)

    def test_repr(self):
        for v, s in value2str.items():
            self.assertEqual(Note(s).__repr__(), f'<Note {v}: "{s}">')
            self.assertEqual(Note(v).__repr__(), f'<Note {v}: "{s}">')

    def test_interval_to(self):
        for v1, v2 in itertools.product(range(12), repeat=2):
            n1 = Note(v1)
            n2 = Note(v2)
            self.assertEqual(n1.interval_to(n2), v1 - v2)

    def test_sub(self):
        for v1, v2 in itertools.product(range(12), repeat=2):
            n1 = Note(v1)
            n2 = Note(v2)
            self.assertEqual(n1 - n2, v1 - v2)

    def test_gt_lt_eq(self):
        for v1, v2 in itertools.product(range(12), repeat=2):
            n1 = Note(v1)
            n2 = Note(v2)
            self.assertEqual(n1 < n2, v1 < v2)
            self.assertEqual(n1 > n2, v1 > v2)
            self.assertEqual(n1 == n2, v1 == v2)

    def test_next(self):
        for v in range(12):
            n = Note(v)
            n2 = Note((v+1)%12)
            self.assertEqual(n.next(), n2)

        for v1, v2 in itertools.product(range(12), repeat=2):
            n1 = Note(v1)
            n2 = Note(v2)
            self.assertEqual(n1.next(v2-v1), n2)

    # TODO: test to_musicpy_note


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

    def test_init_without_exception(self):
        for case_ in self.cases:
            for i in range(1, len(case_)):
                self.assertEqual(
                    Chord(case_[0]).values(),
                    Chord(case_[i]).values()
                )

    def test_init_with_exception(self):
        with self.assertRaises(TypeError):
            Chord([1.2, 2.3, 3.4])

    def test_value(self):
        for case_ in self.cases:
            for i in range(1, len(case_)):
                self.assertEqual(
                    Chord(case_[i]).values(),
                    case_[0]
                )

    def test_repr(self):
        v = [5, 1, 4]
        s = '<Chord 5: "C"; 1: "E"; 4: "G">'
        self.assertEqual(Chord(v).__repr__(), s)

    def test_avg_value(self):
        v = [5, 1, 4]
        avg_value = sum(v) / len(v)
        self.assertEqual(Chord(v).avg_value(), avg_value)


if __name__ == "__main__":
    unittest.main()