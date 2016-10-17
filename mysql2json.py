#!/usr/bin/env python3
import MySQLdb
import MySQLdb.cursors
import argparse
import re
import json
import datetime
import sys


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--user", required=True)
    argparser.add_argument("--password", default="")
    argparser.add_argument("--database", required=True)
    argparser.add_argument("--execute", required=True)
    args = argparser.parse_args()

    db = MySQLdb.connect(user=args.user, password=args.password, db=args.database, charset='utf8')

    results = []
    c = db.cursor(MySQLdb.cursors.DictCursor)
    c.execute(args.execute)
    row = c.fetchone()
    while row is not None:
        results.append(row)
        row = c.fetchone()

    json.dump(results, sys.stdout, default=json_serial, sort_keys=True, ensure_ascii=False)


def escape_table_name(table_name):
    if not re.search(r'^[a-zA-Z0-9_-]*$', table_name):
        raise(Exception("Table name %s could not be escaped because it has unusual characters"))
    return "`%s`" % (table_name,)

def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise(TypeError("Type %r not serializable" % type(obj)))

if __name__ == "__main__":
    main()
