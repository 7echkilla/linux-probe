import pkgutil
import importlib
import logging

import probe.modules

from probe.module import Module

logger = logging.getLogger(__name__)

def load_modules():
    """
    Detect and load modules from designated directory
    """
    modules = {}

    for _, name, _ in pkgutil.iter_modules(probe.modules.__path__):
        module = importlib.import_module(f"probe.modules.{name}")

        for member in vars(module).values():
            if (isinstance(member, type) and issubclass(member, Module) and member is not Module):
                instance = member()

                if (not instance.name):
                    logger.warning("Skipped invalid module with no name")

                elif (instance.name in modules):
                    logger.warning("Skipped module with duplicate name: %s", instance.name)

                else:
                    instance.warm_up()
                    modules[instance.name] = instance

    return modules

if __name__ == "__main__":
    print(load_modules())
