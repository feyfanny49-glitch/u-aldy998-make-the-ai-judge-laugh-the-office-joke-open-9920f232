#!/usr/bin/env python3
"""Emit the one-line office joke as the judged text artifact.

Rules enforced here so an invalid artifact can never reach the judge:
  * UTF-8 text, 1..200 characters, not whitespace-only
  * exact bytes, no trailing newline
  * atomic publication: temp file in the destination directory + os.replace
"""
import hashlib
import os
import tempfile
from pathlib import Path

OUTPUT = Path("/output/entry.txt")
ENTRY = "New hire asked where the coffee is. We formed a committee. The coffee is now cross-functional."


def validate(text: str) -> bytes:
    """Return the exact bytes to publish, or refuse the entry outright."""
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1..200 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be whitespace only")
    data = text.encode("utf-8")  # strict: refuses anything not UTF-8 encodable
    if data[-1:] in (b"\n", b"\r"):
        raise ValueError("entry must not end with a newline")
    return data


def write_atomic(dest: Path, data: bytes) -> None:
    """Publish data in one rename; never leave a half-written artifact."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=".entry-", dir=str(dest.parent))
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, dest)
        try:  # persist the rename itself where the filesystem allows it
            dir_fd = os.open(str(dest.parent), os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except OSError:
            pass
    except BaseException:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def main() -> None:
    data = validate(ENTRY)      # validate before touching the destination
    write_atomic(OUTPUT, data)  # readers see either the old file or the whole new one
    digest = hashlib.sha256(data).hexdigest()
    print(f"{OUTPUT}: {len(ENTRY)} chars, {len(data)} bytes, sha256 {digest}")


if __name__ == "__main__":
    main()
