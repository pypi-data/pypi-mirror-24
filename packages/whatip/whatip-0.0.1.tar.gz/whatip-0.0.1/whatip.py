try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen
import re
from argparse import ArgumentParser
import sys
import logging
import socket

VERSION = '0.0.1'
SOURCES = ['ipapi', 'formyip']


def parse_cli():
    parser = ArgumentParser()
    parser.add_argument('--ip', action='store_true', default=False,
                        help='display only IP') 
    parser.add_argument('-s', '--source', choices=SOURCES,
                        help='use specific source')
    return parser.parse_args()


def parse_formyip():
    data = urlopen('http://formyip.com').read().decode('utf-8')
    ip = re.search(r'Your IP is ([^<]*)', data).group(1)
    cnt = re.search(r'Your Country is: ([^<]*)', data).group(1)
    return ip, cnt


def parse_ipapi():
    data = urlopen('http://ip-api.com/json').read().decode('utf-8')
    ip = re.search(r'query":"(.+?)"', data).group(1)
    cnt = re.search(r'country":"(.+?)"', data).group(1)
    return ip, cnt


def main(**kwargs):
    logging.basicConfig(level=logging.DEBUG)
    socket.setdefaulttimeout(5)
    opts = parse_cli()
    if opts.source in SOURCES:
        sources = [opts.source]
    else:
        sources = SOURCES
    ip, cnt = None, None
    for source in sources:
        try:
            ip, cnt = globals()['parse_%s' % source]()
        except Exception as ex:
            logging.error('Failed to parse %s source: %s' % (source, ex))
    if ip is None:
        logging.error('Fatal error: all sources failed')
        sys.exit(1)
    if opts.ip:
        print(ip)
    else:
        print('%s %s' % (ip, cnt))


if __name__ == '__main__':
    main()
