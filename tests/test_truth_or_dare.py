from library.truth_or_dare import TruthOrDare

TEST_FILE_NAME = "test.csv"

class TestTruthOrDare:
    def test___init__(self):
        TruthOrDare()
        pass

    def test_get_data(self):
        TruthOrDare().get_data(TEST_FILE_NAME)
        pass
