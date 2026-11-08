# Copyright (C) 2021-2026 Katelynn Cadwallader. Part of AMPAPI_Python, under the GPL v3 (see LICENSE).
# ruff: noqa: INP001 # the samples are scripts run directly, not a package
"""List a shard's files, upload a small text file, read it back, download it, then delete it.

Everything it makes goes in an `ampapi-sample` folder in the shard, which is deleted at the end. With the library
installed, set the panel's URL, a login and the shard's ID, then run it:

    AMP_URL=http://192.168.1.10:8443 AMP_USER=admin AMP_PASSWORD=... AMP_SHARD=<shard ID> python samples/files.py
"""

from __future__ import annotations

import asyncio
import os

from ampapi import Panel, Session, Shard, ShardFileContentResponse, ShardFileResponse

FOLDER: str = "ampapi-sample"
GREETING: bytes = b"Hello from AMPAPI_Python!\n"


async def main() -> None:
    """Round trip one small file through a shard."""
    session = Session(url=os.environ["AMP_URL"], username=os.environ["AMP_USER"], password=os.environ["AMP_PASSWORD"])

    async with Panel(session=session) as panel:
        shard: Shard = await panel.get_shard(shard_id=os.environ["AMP_SHARD"])

        # Paths are relative to the shard's own folder, and "" is the top of it.
        entries: list[ShardFileResponse] = await shard.get_files(path="")
        for entry in entries:
            size: str = "folder" if entry["isDirectory"] is True else f"{entry['size']} bytes"
            print(f"{entry['path']} | {size} | Modified: {entry['modified']}")

        # `upload_files` sends small files in one request, and `upload_file` sends a big one in chunks.
        await shard.upload_files(folder=FOLDER, files={"hello.txt": GREETING})
        print(f"Uploaded {FOLDER}/hello.txt")

        # A text file can be read back as a string.
        content: ShardFileContentResponse = await shard.get_file_content(path=f"{FOLDER}/hello.txt")
        print(f"Its content: {content['content']!r}")

        # Or downloaded as bytes, which works for any file. The whole file is held in memory, so mind the big ones.
        downloaded: bytes = await shard.download_file(path=f"{FOLDER}/hello.txt")
        print(f"Downloaded {len(downloaded)} bytes, the same as we sent: {downloaded == GREETING}")
        # Want to keep it? `Path("hello.txt").write_bytes(downloaded)` saves it next to you.

        # Deleting a folder takes everything in it.
        await shard.delete_file(path=FOLDER)
        remaining: list[ShardFileResponse] = await shard.get_files(path="")
        print(f"{FOLDER} is gone: {all(entry['name'] != FOLDER for entry in remaining)}")


if __name__ == "__main__":
    asyncio.run(main())
