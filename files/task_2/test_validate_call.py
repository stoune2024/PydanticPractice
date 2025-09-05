from .validate_call import user_process_func, UserModel
from pydantic import ValidationError


def test_validate_call(tab_number: int, username: str):
    try:
        result = user_process_func(UserModel(tab_number=tab_number, username=username))
        return print(result)
    except ValidationError as e:
        print(f"An error has occured: {e}")
    finally:
        print("Some exit logic here!")
