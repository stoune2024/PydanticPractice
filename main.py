from files.task_2 import test_validate_call


def main():
    test_validate_call(tab_number=12345, username="johndoe")
    test_validate_call(tab_number="some_letters_instead", username="johndoe")


if __name__ == "__main__":
    main()
