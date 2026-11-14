#!/usr/bin/env python3
"""Choose the newest stable upstream tag newer than any published fork release."""
import json
import re
import sys

UPSTREAM = re.compile(r"v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)\Z")
FORK = re.compile(r"v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)-shizuku-clipboard\Z")


def version(pattern, value):
    match = pattern.fullmatch(value)
    return tuple(map(int, match.groups())) if match else None


def select(tags, releases):
    stable = [(parsed, tag) for tag in tags if (parsed := version(UPSTREAM, tag))]
    if not stable:
        raise ValueError("No stable vX.Y.Z upstream tags found")
    published = [parsed for release in releases
                 if not release.get("isDraft") and not release.get("isPrerelease")
                 if (parsed := version(FORK, release.get("tagName", "")))]
    latest, tag = max(stable)
    return tag if not published or latest > max(published) else None


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as tags_file:
        tags = tags_file.read().splitlines()
    with open(sys.argv[2], encoding="utf-8") as releases_file:
        releases = json.load(releases_file)
    try:
        print(select(tags, releases) or "")
    except ValueError as error:
        sys.exit(str(error))
