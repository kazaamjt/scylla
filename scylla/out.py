import sys
from enum import Enum
from typing import Any

from colorama import Fore


class LogLevel(int, Enum):
	"""Enum class to indicate the loglevel."""
	NORMAL = 0
	VERBOSE_1 = 1
	VERBOSE_2 = 2
	VERBOSE_3 = 3


LOG_LEVEL = LogLevel.NORMAL


def info(*args: str, **kwargs: Any) -> None:
	"""Print an info level message."""
	print(Fore.GREEN + "INFO:" + Fore.RESET, *args, **kwargs)


def warning(*args: str, **kwargs: Any) -> None:
	"""Print a warning."""
	print(Fore.YELLOW + "WARNING:" + Fore.RESET, *args, **kwargs)


def error(*args: str, exit: bool = True, **kwargs: Any) -> None:
	"""Print a big fat error."""
	print(Fore.RED + "ERROR:" + Fore.RESET , *args, **kwargs)
	if exit:
		sys.exit(1)


def verbose_1(*args: str, **kwargs: Any) -> None:
	"""Print a verbose level 1 message."""
	if LOG_LEVEL == LogLevel.VERBOSE_1:
		print(Fore.LIGHTBLUE_EX + "VERBOSE 1:" + Fore.RESET, *args, **kwargs)


def verbose_2(*args: str, **kwargs: Any) -> None:
	"""Print a verbose level 2 message."""
	if LOG_LEVEL == LogLevel.VERBOSE_2:
		print(Fore.LIGHTBLUE_EX + "VERBOSE 2:" + Fore.RESET, *args, **kwargs)


def verbose_3(*args: str, **kwargs: Any) -> None:
	"""Print a verbose level 3 message."""
	if LOG_LEVEL == LogLevel.VERBOSE_3:
		print(Fore.LIGHTBLUE_EX + "VERBOSE 3:" + Fore.RESET, *args, **kwargs)


def set_level(level: int) -> None:
	global LOG_LEVEL
	if level > 3:
		level = 3

	LOG_LEVEL = LogLevel(level)
	verbose_1(f"Set verbosity to level {level}")
