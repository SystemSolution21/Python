# relative import from sub_package1(parent package)

from .. import package1_file2


def file() -> None:
    print("relative import package1_file2 from sub_package1 sub_file.py:")
    package1_file2.file2()
    print("This is sub_file.py in sub_package1")
