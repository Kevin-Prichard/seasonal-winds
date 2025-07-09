#!/usr/bin/env python3

from csv import DictReader
from datetime import datetime as dt
from os import walk
from sys import stderr
from typing import Mapping, Generator


def narrow(base_dir, wanted_flds: Mapping[str, str]) -> Generator[Mapping[str, str], None, None]:
    for root, dirs, files in walk(base_dir):
        for file in sorted(files):
            stderr.write(f"${file}\n")
            if file.endswith('.psv'):
                path = f"{root}/{file}"
                with open(path, 'r', encoding='utf-8') as f:
                    fields = f.readline().strip().split('|')
                    reader = DictReader(f, delimiter='|', fieldnames=fields)
                    for row in reader:
                        nurow = {k: v.strip()
                                 for k, v in row.items()
                                 if k in wanted_flds}
                        yield nurow


def main(base_dir):
    with open("var/fields_min.txt", "r") as f:
        wanted_flds = {line.strip(): line.strip() for line in f if line.strip()}
    for row in narrow(base_dir, wanted_flds):
        d = row.get('DATE', None)
        t = row.get('temperature', None)
        w = row.get('wind_speed', None)

        print(f"d:{{{int(dt.fromisoformat(d).timestamp() * 1000) if d else 'null'},"
              f",t:{t if t else 'null'}"
              f",w:{w if w else 'null'}}}")


if __name__ == "__main__":
    main("data")
