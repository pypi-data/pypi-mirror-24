
from cooked_input import *

prompt_str = "Enter a number between -1 and 10, but not 0"
validators = [RangeValidator(-10, 10), NoneOfValidator(0)]
response = get_input(prompt=prompt_str, convertor=IntConvertor(), validators=validators, default=5)
print(response)