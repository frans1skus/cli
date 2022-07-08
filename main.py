import argparse
from pathlib import Path
import os
import json
import re


def main():
    sourcePath = '/var/log/'
    targetPath = '/var/result/'
    fname = "error.log"

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-data_dir",
        type=Path,
        default=sourcePath,
        help="Path to the data directory",
    )

    parser.add_argument(
        "-t",
        type=str,
        default='txt',
        help="convert log file with default '*.txt' extention",
    )

    parser.add_argument(
        "-o",
        type=Path,
        default=targetPath,
        help="Target Path for data directory",
    )

    p = parser.parse_args()

    type = str(p.t)
    if type != "json":
        type = "txt"

    target_file = p.o
    if target_file == Path(targetPath):
        target_file = Path.joinpath(
            p.o, os.path.splitext(fname)[0]+"."+type)
    source_file = Path.joinpath(p.data_dir, fname)
    if Path(target_file).is_file():
        os.remove(target_file)
    with open(source_file, 'r') as log_file,\
            open(target_file, 'w') as write_file:
        if type == "json":
            json_data = re.search(
                r'(Response:\s*)(.*)(?=\(HttpClientUtil\))', log_file.read(), re.DOTALL)
            if json_data:
                json.dump(json.loads(json_data.group(2)), write_file)
        else:
            write_file.write(log_file.read())
            write_file.close()


if __name__ == "__main__":
    main()
