import asyncio
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from typing import Any, Callable, Coroutine, Dict, List, Optional

import aiohttp

from.progress import ProgressBar


@dataclass
class ChunkReport:
	name: str
	downloaded: int
	total_size: int


@dataclass
class DownloadError:
	name: str
	error: Exception


ChunkReportCallback = Callable[[ChunkReport], None]


class DownloadException(Exception):
	"""Raised by the download class if something goes wrong."""


class Download:
	def __init__(
		self,
		url: str,
		output_dir: Path,
		chunk_report_cb: Optional[ChunkReportCallback] = None,
	) -> None:
		self.url = url

		try:
			self._url_parts = urlparse(url)
		except ValueError:
			raise DownloadException(
				f"Unable to download: Malformed url: {url}"
			)
		self.name = Path(self._url_parts.path).name
		self._file_path = output_dir / self.name
		self._chunk_report_cb = chunk_report_cb

	async def start(
		self,
		session: aiohttp.ClientSession,
		done_cb: Callable[[str], Coroutine[Any, Any, None]],
		error_cb: Callable[[DownloadError], None],
	) -> None:
		try:
			response = await session.get(self.url)
			total_dl_size = int(response.headers.get("CONTENT-LENGTH", 0))

			downloaded = 0
			with open(self._file_path, "wb") as f:
				async for data, _ in response.content.iter_chunks():
					f.write(data)
					if self._chunk_report_cb is not None:
						downloaded += sys.getsizeof(data)
						if total_dl_size < downloaded:
							total_dl_size = downloaded

						self._chunk_report_cb(
							ChunkReport(self.name, downloaded // 8, total_dl_size // 8)
						)
		except aiohttp.ClientError as e:
			error_cb(DownloadError(self.name, e))

		await done_cb(self.name)


class Downloader:
	def __init__(
		self,
		urls: List[str],
		output_dir: Path,
		max_concurrent: int = 5,
		chunk_report_cb: Optional[ChunkReportCallback] = None,
		report_done_cb: Optional[Callable[[str], None]] = None,
	) -> None:
		self.urls = urls
		self.errors: List[DownloadError] = []
		self._output_dir = output_dir
		self._tasks: Dict[str, asyncio.Task] = {}
		self._handled = 0

		if max_concurrent == 0:
			self._max_concurrent = len(urls)
		else:
			self._max_concurrent = max_concurrent

		self._chunk_report_cb = chunk_report_cb
		self._report_done_cb = report_done_cb

		if not self._output_dir.exists():
			raise RuntimeError(f"Output dir: No such directory: {self._output_dir}")

		self._concurrent = 0
		self._done_queue: asyncio.Queue[str] = asyncio.Queue()

	async def start(self) -> None:
		n_urls = len(self.urls)
		async with aiohttp.ClientSession() as session:
			for url in self.urls:
				self.schedule_download(session, url)
				self._concurrent += 1
				if self._concurrent >= self._max_concurrent:
					await self._wait_until_next()

			while self._handled < n_urls:
				await asyncio.sleep(0)

	async def _wait_until_next(self) -> None:
		await self._done_queue.get()
		self._done_queue.task_done()

	def schedule_download(self, session: aiohttp.ClientSession, url: str) -> None:
		try:
			download = Download(url, self._output_dir, self._chunk_report_cb)
		except DownloadException as e:
			self.errors.append(DownloadError(url, e))
		else:
			task = asyncio.create_task(
				download.start(
					session,
					self._done_cb,
					self._error_cb,
				),
				name=download.name,
			)
			self._tasks[download.name] = task

	def _error_cb(self, error: DownloadError) -> None:
		self.errors.append(error)

	async def _done_cb(self, name: str) -> None:
		await self._done_queue.put(name)
		self._concurrent -= 1
		self._handled += 1
		self._tasks.pop(name)
		if self._report_done_cb is not None:
			self._report_done_cb(name)


class GraphicDownloader(Downloader):
	def __init__(self, urls: List[str], output_dir: Path, max_concurrent: int) -> None:
		super().__init__(
			urls, output_dir,
			max_concurrent=max_concurrent,
			chunk_report_cb=self.chunk_report_cb,
			report_done_cb=self.download_done_cb,
		)
		self.progress_writers: Dict[str, ProgressBar] = {}

	def chunk_report_cb(self, report: ChunkReport) -> None:
		bar = self.progress_writers.get(report.name, None)
		if bar is None:
			bar = ProgressBar(report.name)
			self.progress_writers[report.name] = bar
		bar.update(report.downloaded, report.total_size)

	def download_done_cb(self, name: str) -> None:
		writer = self.progress_writers.get(name, None)
		if writer is not None:
			writer.close()
