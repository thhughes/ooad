from abc import ABC
from typing import Dict, Callable, Any
from functools import wraps

class Mockable:
	class MockMethod:
		def __init__(self, original_method):
			self.original_method = original_method
			self.remaining_calls = 0
			self.instance = None
			self.call_count = 0
			self.mocked_return = None
			self.mock_called = False 	## True if one of the mocking methods was called after last reset 
			self.mocked_to_expect_call = True ## False if method is expected to never be calledf  
			self._ignore_calls = False 

		def __call__(self, *args, **kwargs):
			if self._ignore_calls: 
				return self.original_method(self.instance, *args, **kwargs) 
			
			assert self.mocked_to_expect_call, 'Method is not expected to be called'

			if not self.mock_called: 
				return self.original_method(self.instance, *args, **kwargs)
			
			assert self.remaining_calls > 0, 'Mocked '\
				'method called too many times. No calls remaining.'
			
			self.call_count += 1
			self.remaining_calls -= 1
			
			return self.mocked_return

		def __get__(self, instance, owner):
			self.instance = instance  # Store the instance
			return self

		def ignore_calls(self): 
			self._ignore_calls = True 

		def expect_no_calls(self): 
			assert not self._ignore_calls, "Cannot Ignore and Expect 0 calls"
			self.mocked_to_expect_call = False 
			self.mock_called = True 

		def expect_call(self, return_value): 
			return self.expect_n_calls(return_value, 1)

		def expect_n_calls(self, return_value, expected_call_count):
			assert not self._ignore_calls, "Cannot Ignore and Expect N calls"
			if 0 == expected_call_count: 
				return self.expect_no_calls()
			
			self.mocked_return = return_value
			self.remaining_calls = expected_call_count
			self.call_count = 0
			self.mock_called = True

		def mock_reset(self):
			self.remaining_calls = 0
			self.call_count = 0
			self.mocked_return = None
			self.mock_called = False
			self.mocked_to_expect_call = True 
			self._ignore_calls = False 
            
		def check_mock_expectations(self):
			return self.remaining_calls == 0
		def __str__(self): 
			return f'Mock({self.original_method}) Remaining[{self.remaining_calls}] Count[{self.call_count}]'

	def __init_subclass__(cls, **kwargs):
		super().__init_subclass__(**kwargs)
		for name, method in cls.__dict__.items():
			if callable(method) and not name.startswith('__'):
				setattr(cls, name, cls.MockMethod(method))

	def check_mock_expectations(self): 
		for name, attr in self.__class__.__dict__.items():
			if isinstance(attr, self.MockMethod):
				atr = getattr(self, name)
				assert atr.check_mock_expectations(), f'Mock {name} failed to meet expectations {str(atr)}'
	
	def mock_reset(self): 
		for name, attr in self.__class__.__dict__.items():
			if isinstance(attr, self.MockMethod):
				getattr(self, name).mock_reset()

		

if __name__ == "__main__": 

	class Example(Mockable): 
		def some_method(self, *args, **kwargs): 
			return 'over 9000'


	e = Example()
	e.some_method.ignore_calls()
	print(e.some_method())
	print(e.some_method())
	print(e.some_method())
	e.check_mock_expectations()
	e.mock_reset()
	e.some_method.expect_n_calls('return', 2)
	print(e.some_method())
	print(e.some_method())
	e.check_mock_expectations()



