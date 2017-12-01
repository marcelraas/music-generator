from music_generator.musical.notes import Note


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
