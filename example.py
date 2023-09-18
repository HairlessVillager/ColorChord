import matplotlib.pyplot as plt
import numpy as np

from colorharmony import Note, Container, show_chords


CDEFGAB = [Note(_) for _ in "CDEFGAB"]
print(CDEFGAB)
container = Container()
container.add_by_notes(CDEFGAB, 3)
container.add_by_notes(CDEFGAB, 4)

for chord in container.chords():
    print(f"{chord}\t{chord.angle_5():.3}\t{chord.harmony():.3}")

show_chords(container.chords())

