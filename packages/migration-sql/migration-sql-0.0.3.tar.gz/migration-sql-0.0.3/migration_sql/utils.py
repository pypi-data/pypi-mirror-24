import re

from .db import DB


def get_db_information_from_url(url) -> (str, int, str, str, str):
    """for ex url=mysql+pymysql://root:root@127.0.0.1:3306/master"""
    pattern = re.compile(r'''
                        (?P<name>[\w\+]+)://
                        (?:
                            (?P<username>[^:/]*)
                            (?::(?P<password>.*))?
                        @)?
                        (?:
                            (?:
                                \[(?P<ipv6host>[^/]+)\] |
                                (?P<ipv4host>[^/:]+)
                            )?
                            (?::(?P<port>[^/]*))?
                        )?
                        (?:/(?P<database>.*))?
                        ''', re.X)

    m = pattern.match(url)
    c = m.groupdict()

    return c["ipv4host"], int(c["port"]), c["username"], c["password"], c["database"]

    
def get_db_from_url(url) -> DB:
    host, port, username, password, name = get_db_information_from_url(url)
    return DB(host, port, username, password, name)
