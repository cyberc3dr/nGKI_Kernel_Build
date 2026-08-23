#!/usr/bin/env python3
"""Add the Android-context ksud bootstrap command to ReSukiSU's init rc."""
from pathlib import Path
import sys

INSTALL = (
    '    "\\texec u:r:" KERNEL_SU_DOMAIN ":s0 root -- " '
    '"/data/adb/ksu-bootstrap/ksud" '
    '" install --libadbroot /data/adb/ksu-bootstrap/libadbroot.so\\n"\n'
    '    "\\texec u:r:" KERNEL_SU_DOMAIN ":s0 root -- " '
    '"/data/adb/ksu-bootstrap/bootstrap-meta.sh\\n"\n'
)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} KSUD_INTEGRATION_C", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    text = path.read_text()
    marker = "install --libadbroot /data/adb/ksu-bootstrap/libadbroot.so"
    if marker in text:
        print("ksud install command already present")
        return 0
    lines = text.splitlines(keepends=True)
    hits = [i for i, line in enumerate(lines) if '"on post-fs-data\\n"' in line]
    if len(hits) != 1:
        raise SystemExit(f"post-fs-data anchor count={len(hits)}, expected exactly 1")
    lines.insert(hits[0] + 1, INSTALL)
    path.write_text("".join(lines))
    if path.read_text().count(marker) != 1:
        raise SystemExit("ksud install injection verification failed")
    print("ksud install scheduled in Android post-fs-data")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
