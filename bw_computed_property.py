from functools import wraps
from math import sqrt


class computed_property:
    def __init__(self, *dependencies):
        self.dependencies = dependencies
        self.cache_name = f"_computed_cache_{id(self)}"

    def __call__(self, func):
        self.func = func
        self.name = func.__name__

        @wraps(func)
        def wrapper(instance):
            if not hasattr(instance, self.cache_name):
                setattr(instance, self.cache_name, {})
            cache = getattr(instance, self.cache_name)

            if self.name not in cache:
                cache[self.name] = self.func(instance)
                cache["deps"] = {
                    dep: getattr(instance, dep, None) for dep in self.dependencies
                }
            else:
                for dep in self.dependencies:
                    if getattr(instance, dep, None) != cache["deps"].get(dep):
                        cache[self.name] = self.func(instance)
                        cache["deps"] = {
                            dep: getattr(instance, dep, None)
                            for dep in self.dependencies
                        }
                        break
            return cache[self.name]

        wrapper = property(wrapper)

        @wrapper.setter
        def setter(instance, value):
            if self.func.__name__ == "diameter":
                instance.radius = value / 2
            if hasattr(instance, self.cache_name):
                getattr(instance, self.cache_name).pop(self.name, None)

        @wrapper.deleter
        def deleter(instance):
            if self.func.__name__ == "diameter":
                instance.radius = 0
            if hasattr(instance, self.cache_name):
                getattr(instance, self.cache_name).pop(self.name, None)

        return wrapper


class Vector:
    def __init__(self, x, y, z, color=None):
        self.x, self.y, self.z = x, y, z
        self.color = color

    @computed_property("x", "y", "z")
    def magnitude(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)


v = Vector(7, 2, 5)
print(v.magnitude)
v.color = "red"
print(v.magnitude)
v.y = 18
print(v.magnitude)
