import sys 
import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.mock_move_support import MockLegalMoveChecker, MockMove
"""
	File to help with rapid prototyping of code in tests folder. 
	used to help development. 
"""
if __name__ == "__main__": 
	m = MockLegalMoveChecker() 
	m.is_legal_move.expect_call(False)
	assert False == m.is_legal_move(MockMove()), 'Failed Mock test'
	m.check_mock_expectations()
	m.mock_reset()
	m.is_legal_move.ignore_calls()
	assert m.is_legal_move(MockMove()), 'Failed default return test' 
	m.check_mock_expectations()
	m.mock_reset()
