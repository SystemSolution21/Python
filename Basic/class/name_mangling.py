# REAL-WORLD BEST PRACTICE: API Resilience via Private Method Aliases
# This pattern ensures that internal class logic (like __init__) remains
# functional even if a subclass provides an incompatible method override.
# Name mangling allows a subclass to override methods
# without breaking internal class method calls.


class BaseService:
    """A base class for processing service requests."""

    def __init__(self, settings: list[str]) -> None:
        self.active_config: list[str] = []
        # We call the 'mangled' version to ensure we use the
        # original implementation defined in THIS class.
        self.__configure_internal(settings=settings)

    def configure(self, settings: list[str]) -> None:
        """Default configuration logic: expects a list of strings."""
        for item in settings:
            self.active_config.append(str(item).upper())

    # Create a private reference to the original method.
    # This is mangled to _BaseService__configure_internal.
    __configure_internal = configure


class SpecializedService(BaseService):
    """A subclass that changes the public API for configuration."""

    def configure(self, key: str, value: str) -> None:  # type: ignore[override]
        """
        Provides a completely different signature for 'configure'.

        In a standard class, this would crash BaseService.__init__ because
        the base constructor only passes ONE argument, but this requires TWO.
        """
        print(f"Applying specialized config: {key}={value}")
        self.active_config.append(f"{key}:{value}")


if __name__ == "__main__":
    # 1. Initialization remains safe:
    # BaseService.__init__ calls the private alias, which points to the 1-arg version.
    service = SpecializedService(settings=["mode_on", "debug_off"])
    print(f"Initial Config: {service.active_config}")

    # 2. The subclass can still use its new, specialized 2-arg API:
    service.configure("timeout", "30s")
    print(f"Final Config: {service.active_config}")
