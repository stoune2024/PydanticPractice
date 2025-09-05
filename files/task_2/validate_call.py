from pydantic import BaseModel, validate_call


class UserModel(BaseModel):
    tab_number: int
    username: str


@validate_call
def user_process_func(data: UserModel) -> str:
    return (
        f"User's username is {data.username}, and his tab_number is {data.tab_number}"
    )
