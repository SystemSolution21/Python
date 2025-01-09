# relative import from package1(same package)

from . import package1_file2


def file1() -> None:
    print("relative import package1_file2 from package1_file1.py:")
    package1_file2.file2()
    print("This is file1 function in package1")


if __name__ == "__main__":
    ...
