from typing import Dict, List, Optional


CO_INSTANCE: Optional["PrintCoordinator"] = None
LONGEST_PACKAGE_LEN = 0


def set_longest(pkg_name: str) -> None:
	global LONGEST_PACKAGE_LEN
	if len(pkg_name) > LONGEST_PACKAGE_LEN:
		LONGEST_PACKAGE_LEN = len(pkg_name)


def human_readable(number: int) -> str:
	for unit in ['','K','M','G','T']:
		if number < 10240:
			return f"{number}{unit}B"
		number = number // 1024
	return f"{number}PB"


class PrintCoordinator:
	def __init__(self) -> None:
		self._printers: Dict[str, str] = {}
		self._len = 0

	def register(self, name: str) -> None:
		self._len += 1
		self._printers[name] = ""
		print()

	def print(self, name: str, line: str) -> None:
		self._printers[name] = line

		print(f"\033[A" * self._len, end="")
		for print_line in self._printers.values():
			print(print_line)

	def unregister(self, name: str) -> None:
		print(f"\033[A" * self._len, end="")
		print(self._printers[name])
		self._len -= 1
		self._printers.pop(name)
		for print_line in self._printers.values():
			print(print_line)


def _get_co() -> PrintCoordinator:
	global CO_INSTANCE
	if CO_INSTANCE is None:
		CO_INSTANCE = PrintCoordinator()

	return CO_INSTANCE


class ProgressBar:
	def __init__(self, file_name: str) -> None:
		self._file_name = file_name
		set_longest(file_name)
		self._name_print = file_name + ((LONGEST_PACKAGE_LEN - len(file_name)) + 1) * " "

		self._co = _get_co()
		self._co.register(self._file_name)

		self._width = 50
		self._char_percent = 100 // self._width

		self._co.print(self._file_name, "\t" + self._name_print + f"[{self._width * ' '}]")

	def update(self, part: int, total: int) -> None:
		"""Update the current progress."""
		percent = int((part / total) * 100)
		bar_size = percent // self._char_percent
		whitespace_size = self._width - bar_size
		if percent < 100:
			beak = '>'
			whitespace_size -= 1
		else:
			beak = ''

		bar_str = '=' * bar_size
		whitespace = ' ' * whitespace_size

		self._name_print = self._file_name + ((LONGEST_PACKAGE_LEN - len(self._file_name)) + 1) * " "
		bar = f"[{bar_str}{beak}{whitespace}] {percent}% "
		bar += f"{human_readable(part)}/{human_readable(total)}"
		self._co.print(self._file_name, "\t" + self._name_print + bar)

	def close(self) -> None:
		self._co.unregister(self._file_name)
