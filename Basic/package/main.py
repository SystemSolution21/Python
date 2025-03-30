from package1 import package1_file1
from package1.sub_package1 import sub_file
from package2.package2_file import pac2_file1, pac2_file2

# from package2 import *


def main() -> None:
    package1_file1.file1()
    sub_file.file()
    pac2_file1()
    print("This is main module in package")


if __name__ == "__main__":
    main()
