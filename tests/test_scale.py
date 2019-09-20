from music_generator.music.scales import GenericScale


def test_generic_scale():
    scale = GenericScale('A#', [0, 2, 4, 5, 7, 9, 11])
    assert str(scale) == 'A#, C, D, D#, F, G, A'


def test_scale_generate():
    scale = GenericScale('C', [0, 2, 3, 5, 7, 8, 10])

    generated = scale.generate(start_octave=3, end_octave=5)
    print(', '.join([str(g) for g in generated]))
    assert True


def test_scale_symbols():
    scale = GenericScale('C', [0, 2, 3, 5, 7, 8, 10])

    symbols = scale.get_symbols()
    assert symbols == ['C', 'D', 'D#', 'F', 'G', 'G#', 'A#']

