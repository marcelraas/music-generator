from music_generator.musical.notes import NOTES_DF

class GenericScale(object):
    def __init__(self, root, notes, sharp):
        self.root = root
        self.notes = notes

        df = NOTES_DF.copy()

        if sharp:
            df = df[df.flat == 0]
        else:
            df = df[df.sharp == 0]



    def generate(self, start, end):

        pass





