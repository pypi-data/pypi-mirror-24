
"""
pytest tests for cooked_input

pytest stuff
    run with:
        pytest cooked_input/

    cmd line args:
        -q <test_file_name>     - run a specific test file
    floating point stuff (https://docs.pytest.org/en/latest/builtin.html?highlight=approx#pytest.approx)
        approx()
    exception raised:
        https://docs.pytest.org/en/latest/getting-started.html#asserting-that-a-certain-exception-is-raised

Len Wanger, 2017
"""

from io import StringIO
from .utils import redirect_stdin

from cooked_input import get_input, get_string
from cooked_input.validators import ExactLengthValidator, InLengthValidator, ChoicesValidator, NoneOfValidator
from cooked_input.cleaners import StripCleaner, LowerCleaner, UpperCleaner
from cooked_input.cleaners import CapitalizeCleaner
from cooked_input.convertors import YesNoConvertor


class TestGetStr(object):

    def test_simple_str(self):
        input_str = 'foo\n\n'

        with redirect_stdin(StringIO(input_str)):
            result = get_input(prompt='Enter any string')
            assert (result == 'foo')

        with redirect_stdin(StringIO(input_str)):
            result = get_input(prompt='Enter any string', blank_ok=True)
            assert (result == 'foo')

            result = get_input(prompt='Enter any string', blank_ok=True)
            assert (result is None)

    def test_capitalize(self):
        input_str = '  \t  bOb JoNeS\t  \t '

        strip_cleaner = StripCleaner()
        rstrip_cleaner = StripCleaner(lstrip=False, rstrip=True)
        lower_cleaner = LowerCleaner()
        upper_cleaner = UpperCleaner()
        strip_and_lower_cleaners = [strip_cleaner, lower_cleaner]
        capitalize_cleaner = CapitalizeCleaner(all_words=False)
        capitalize_all_cleaner = CapitalizeCleaner(all_words=True)

        with redirect_stdin(StringIO(input_str)):
            result = get_input(
                prompt='Enter any string (will be stripped of leading and trailing spaces and converted to lower)',
                cleaners=strip_and_lower_cleaners)
            assert (result == 'bob jones')

        with redirect_stdin(StringIO(input_str)):
            result = get_input(prompt='Enter any string (will be stripped of trailing spaces and converted to upper)',
                               cleaners=[rstrip_cleaner, upper_cleaner])
            assert (result == '  \t  BOB JONES')

        with redirect_stdin(StringIO(input_str)):
            result = get_input(prompt='Enter your name (first word will be capitalized)', cleaners=[strip_cleaner, capitalize_cleaner])
            assert (result == 'Bob jones')

        with redirect_stdin(StringIO(input_str)):
            result = get_input(prompt='Enter your name (all words will be capitalized)',
                               cleaners=[strip_cleaner, capitalize_all_cleaner])
            assert (result == 'Bob Jones')

    def test_choices(self):
        input_str_blank = """
 
            """

        input_str = """
                    licorice
                    booger
                    lemon 
                    """

        colors = ['red', 'green', 'blue']
        good_flavors = ['cherry', 'lime', 'lemon', 'orange']
        bad_flavors = 'licorice'
        choices_validator = ChoicesValidator(choices=colors)
        good_flavor_validator = ChoicesValidator(choices=good_flavors)
        bad_flavor_validator = ChoicesValidator(choices=bad_flavors)
        not_in_choices_validator = NoneOfValidator(validators=[bad_flavor_validator])
        strip_cleaner = StripCleaner()
        lower_cleaner = LowerCleaner()
        strip_and_lower_cleaners = [strip_cleaner, lower_cleaner]

        with redirect_stdin(StringIO(input_str_blank)):
            result = get_input(validators=not_in_choices_validator, default='cherry')
            assert (result == 'cherry')

        with redirect_stdin(StringIO(input_str)):
            result = get_input(validators=not_in_choices_validator, default='cherry')
            assert (result == 'cherry')

        with redirect_stdin(StringIO(input_str)):
            validators = [good_flavor_validator, not_in_choices_validator]
            result = get_input(cleaners=strip_and_lower_cleaners, validators=validators,default='cherry')
            assert (result == 'lemon')

    def test_choices(self):
        input_str_blank = """

            """

        input_str = """
                    a
                    licorice
                    bo
                    lem 
                    """

        length_3_validator = ExactLengthValidator(length=3)
        length_5_plus_validator = InLengthValidator(min_len=5)
        length_2_to_4_validator = InLengthValidator(min_len=2, max_len=4)

        with redirect_stdin(StringIO(input_str)):
            result = get_input(prompt='Enter a three letter string', validators=[length_3_validator])
            assert (result == 'lem')

        with redirect_stdin(StringIO(input_str)):
            result = get_input(prompt='Enter a string at least 5 letters long', validators=[length_5_plus_validator])
            assert (result == 'licorice')

        with redirect_stdin(StringIO(input_str)):
            result = get_input(prompt='Enter a 2 to 4 letter string', validators=[length_2_to_4_validator])
            assert (result == 'bo')

    def test_choices(self):
        input_str_blank = "\n\n"

        input_str_y = " a\ny"

        input_str_n = "a\n  no"

        strip_cleaner = StripCleaner()


        with redirect_stdin(StringIO(input_str_y)):
            result = get_input(cleaners=strip_cleaner, convertor=YesNoConvertor(), default='Y')
            assert (result == 'yes')

        with redirect_stdin(StringIO(input_str_blank)):
            result = get_input(cleaners=strip_cleaner, convertor=YesNoConvertor(), default='Y')
            assert (result == 'yes')

        with redirect_stdin(StringIO(input_str_n)):
            result = get_input(cleaners=strip_cleaner, convertor=YesNoConvertor(), default='Y')
            assert (result == 'no')
