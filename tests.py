from functions.get_file_content import get_file_content


def test():
    result = get_file_content("calculator", "main.py")
    print("Result for 'main.py' file:")
    print(result)

    result = get_file_content("calculator", "pkg/calculator.py")
    print("Result for 'pkg/calculator.py' file:")
    print(result)

    result = get_file_content("calculator", "/bin/cat")
    print("Result for '/bin/cat' file:")
    print(result)


if __name__ == "__main__":
    test()