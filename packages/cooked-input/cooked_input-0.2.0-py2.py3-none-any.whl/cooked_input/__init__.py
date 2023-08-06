# -*- coding: utf-8 -*-

__version__ = '0.2.0'

from .get_input import get_input, get_table_input, process_value, make_pretty_table
from .get_input import TABLE_ID, TABLE_VALUE, TABLE_ID_OR_VALUE
from .error_callbacks import print_error, log_error, silent_error, DEFAULT_CONVERTOR_ERROR, DEFAULT_VALIDATOR_ERROR

from .convertors import Convertor, IntConvertor, FloatConvertor, BooleanConvertor
from .convertors import ListConvertor, DateConvertor, YesNoConvertor, TableConvertor
from .validators import Validator, ExactLengthValidator, InLengthValidator, ExactValueValidator, InRangeValidator
from .validators import InAnyValidator, NotInValidator, InChoicesValidator, RegexValidator, PasswordValidator
from .validators import ListValidator, SimpleValidator
from .validators import in_all, in_any, not_in, validate
from .cleaners import Cleaner, UpperCleaner, LowerCleaner, CapitalizeCleaner
from .cleaners import StripCleaner, ReplaceCleaner

__all__ = ['get_input', 'convertors', 'validators', 'cleaners', 'error_callbacks']
