from .validate_call import user_process_func, UserModel
from pydantic import ValidationError


def test_validate_call_valid():
    try:
        result = user_process_func(UserModel(tab_number=12345, username='johndoe'))
        return print(result)
    except ValidationError as e:
        print(f'An error has occured: {e}')
    finally:
        print('Some exit logic here!')

def test_validate_call_invalid():
    try:
        result = user_process_func(UserModel(tab_number='some_letters_instead!', username='johndoe'))
        return print(result)
    except ValidationError as e:
        print(f'An error has occured: {e}')
    finally:
        print('Some exit logic here!')
