from music_generator.music.notes import Note


class GenericScale(object):
    def __init__(self, root: str, steps):
        self.steps = steps
        self.root = root

    def __repr__(self):
        return ', '.join([n.get_symbol() for n in self.generate(0, 1)])

    def generate(self, start_octave=0, end_octave=8):

        notes = []
        for octave in range(start_octave, end_octave):

            for step in self.steps:
                generator_note = Note(self.root, octave)
                notes.append(generator_note.increment(step))

        return notes

    def get_symbols(self):
        return [x.get_symbol() for x in self.generate(0, 1)]


def major_scale(root):
    return GenericScale(root, [0, 2, 4, 5, 7, 9, 11])


def minor_scale(root):
    return GenericScale(root, [0, 2, 3, 5, 7, 8, 10])


def chromatic_scale(root):
    return GenericScale(root, range(0, 12))


