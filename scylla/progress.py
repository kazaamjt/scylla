from typing import List, Optional


CO_INSTANCE: Optional["PrintCoordinator"] = None
LONGEST_PACKAGE_LEN = 0


class PrintCoordinator:
	def __init__(self) -> None:
		self._lines: List[str] = []

	def register(self) -> int:
		self._lines.append("")
		print()
		return len(self._lines) - 1

	def print(self, tag: int, line: str) -> None:
		self._lines[tag] = line

		print(f"\033[A" * len(self._lines), end="")
		print(*self._lines, sep="\n")


def _get_co() -> PrintCoordinator:
	global CO_INSTANCE
	if CO_INSTANCE is None:
		CO_INSTANCE = PrintCoordinator()

	return CO_INSTANCE


class ProgressBar:
	def __init__(self, file_name: str) -> None:
		self._name_print = file_name + ((LONGEST_PACKAGE_LEN - len(file_name)) + 1) * " "

		self._co = _get_co()
		self._tag = self._co.register()

		self._width = 50
		self._char_percent = 100 // self._width

		self._co.print(self._tag, "\t" + self._name_print + f"[{self._width * ' '}]")

	def update(self, percent: int) -> None:
		"""Update the current progress."""
		bar_size = percent // self._char_percent
		whitespace_size = self._width - bar_size
		if percent < 100:
			beak = '>'
			whitespace_size -= 1
		else:
			beak = ''

		bar_str = '=' * bar_size
		whitespace = ' ' * whitespace_size

		bar = f"[{bar_str}{beak}{whitespace}]"
		self._co.print(self._tag, "\t" + self._name_print + bar)
