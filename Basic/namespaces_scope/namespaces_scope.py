# global variable
global_variable: int = 10
print(f"{global_variable = }")


def outer_function() -> None:
    nonlocal_variable: int = 20
    print(f"{nonlocal_variable = }")

    def inner_function() -> None:
        local_variable: int = 30

        nonlocal nonlocal_variable  # using 'nonlocal' keyword nonlocal variable is accessible
        nonlocal_variable += local_variable

        global global_variable  # using 'global' keyword global variable is accessible
        global_variable += local_variable

        print(f"{local_variable = }")
        print(f"modified {nonlocal_variable = }")
        print(f"modified {global_variable = }")

    inner_function()


outer_function()
