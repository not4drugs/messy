from logging import (Logger,
                     _levelToName)

from hypothesis import strategies

from .utils import names

log_levels = strategies.sampled_from(_levelToName.keys())
loggers = strategies.builds(Logger,
                            name=names,
                            level=log_levels)
instances_names = names
