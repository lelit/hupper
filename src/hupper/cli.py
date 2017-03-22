from __future__ import print_function

import argparse
import re
import sys

from .reloader import start_reloader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", dest="module", required=True)
    parser.add_argument("--file-re", dest="file_filters", action="append")
    parser.add_argument("--module-re", dest="module_filters", action="append")

    args, unknown_args = parser.parse_known_args()

    sys.argv[1:] = unknown_args
    sys.path.insert(0, "")

    if args.file_filters:
        file_filters = [re.compile(f) for f in args.file_filters]
        def file_filter(path):
            for f in file_filters:
                if f.match(path):
                    return True
    else:
        file_filter = None

    if args.module_filters:
        module_filters = [re.compile(f) for f in args.module_filters]
        def module_filter(module):
            for f in module_filters:
                if f.match(module):
                    return True
    else:
        module_filter = None

    start_reloader(
        "runpy.run_module",
        file_filter=file_filter,
        module_filter=module_filter,
        worker_args=[args.module],
        worker_kwargs={"alter_sys": True, "run_name": "__main__"})
