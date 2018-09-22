from music_generator.analysis import regen_models

def test_fft_branches_filter():

    fragment_length = 4096

    model = regen_models.FftBranchesFilter(fragment_length, learning_rate=1e-4, loss_fct='fft_loss').build_model()

    pass

