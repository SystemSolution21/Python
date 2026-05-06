class Demo:
    def regular(self, x):
        return f"regular: self={self}, x={x}"

    @staticmethod
    def static(x, y):
        return f"static: x={x}, y={y}"

    @classmethod
    def class_method(cls, x):
        return f"classmethod: cls={cls.__name__}, x={x}"

    def simple(x, y):
        return f"simple: x={x}, y={y}"


# Create an instance
d = Demo()

# --- Regular method ---
print("Regular via instance:", d.regular(10))
# print("Regular via class:", Demo.regular(x=10))  # ❌ TypeError (missing self)

# --- Static method ---
print("Static via class:", Demo.static(2, 3))
print("Static via instance:", d.static(2, 3))

# --- Class method ---
print("Classmethod via class:", Demo.class_method(5))
print("Classmethod via instance:", d.class_method(5))

# --- Simple method (no self, no decorator) ---
print("Simple via class:", Demo.simple(x=2, y=3))
# print(
#     "Simple via instance:", d.simple(2, 3)
# )  # ❌ TypeError: simple() takes 2 positional args but 3 were given
