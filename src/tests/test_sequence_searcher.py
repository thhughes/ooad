from game.sequence_searcher import SequenceSearchInterface, SequenceSearcher
# pylint: disable=unused-variable

def i_build(size, **kwargs) -> SequenceSearchInterface: 
	return SequenceSearcher(size, **kwargs)

def test_sequence_searcher_size(): 
	assert i_build(0).sequence_size() == 0, "Incorrect Sequence Size"
	assert i_build(100).sequence_size() == 100, "Incorrect Sequence Size" 
