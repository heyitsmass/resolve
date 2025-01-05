import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from typing import Iterable

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    "-s", metavar="site", help="ip address or domain to check."
)
arg_parser.add_argument(
    "-f", metavar="file", help="file of domains to enumerate"
)
arg_parser.add_argument(
    "-t", metavar="threads", help="thread count", default=10
)
arg_parser.add_argument(
    "-o", metavar="output", help="output filename", default="resolve.out"
)


args = arg_parser.parse_args()

if not any((args.f, args.s)):
    print("Host, filename, or both must be passed in.")
    exit(1)


hosts = [args.s] if args.s else []

if args.f:
    import os
    from urllib import parse

    if os.path.isfile(args.f):
        valid = []
        with open(args.f, "r") as fp:
            for item in fp.readlines():
                try:
                    parse.urlparse(item)
                    hosts.append(item.removesuffix("\n"))
                except Exception:
                    print(f"Skiped:{item}")
                    continue

import re


class HostForms:
    WWW = 0
    HTTP = 1
    HTTPS = 2

    @staticmethod
    def apply_split_tok(value: str, tok: str, prefix: str = None):
        if re.match(tok, value):
            return re.split(tok, value)[1]
        return f"{prefix}{value}" if prefix else value

    @property
    def handlers(self):
        return {
            self.WWW: lambda x: self.apply_split_tok(
                x, r"^(www\.)", "www."
            ),
            self.HTTPS: lambda x: self.apply_split_tok(
                x, r"^(https?://)", "https://"
            ),
            self.HTTP: lambda x: self.apply_split_tok(
                x, r"^(http://)", "http://"
            ),
        }

    def get_host_set(self, host: str):
        res = set([host])
        for handler in self.handlers.values():
            res.add(handler(host))
        return res

    def get_valid_hosts(self, host: str):
        res = []
        for host in self.get_host_set(host):
            try:
                socket.gethostbyname(host)
                res.append(host)
            except:
                continue

        return res if len(res) else None


lock = Lock()


def save_results(results: Iterable[str]):
    with open(args.o, "w+") as fp:
        fp.writelines("\n".join(results))


def run_concurrently():
    results = set()
    host_forms = HostForms()

    def check_host(host: str):
        if res := host_forms.get_valid_hosts(host):
            with lock:
                results.update(res)

    with ThreadPoolExecutor(max_workers=args.t) as executor:
        for i, host in enumerate(hosts):
            executor.submit(check_host, host)

            if i == 10:
                break

    save_results(results)


if __name__ == "__main__":
    run_concurrently()
