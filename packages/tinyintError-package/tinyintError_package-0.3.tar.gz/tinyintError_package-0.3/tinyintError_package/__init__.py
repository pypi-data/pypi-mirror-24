
from .validate import validate_val, validate_tiny_int
from .error import TinyIntError

def tiny_int(val, call_back = None):
    try:
      if validate_val(val) and validate_tiny_int(val):
        return True
      else:
       raise TinyIntError()
    except TinyIntError as error:
      if call_back is not None:
        call_back()
      else:
        print(error)
        print(error)

def call_back_function():
    print("Esto se ejecuta cuando existe un error")