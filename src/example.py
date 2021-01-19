"""Main Program

Usage:
  Main [options]
  Main -h | --help

Options:
  -h --help                         Show this screen.
  -u --username=<username>          Username for API Gateway.
  -p --password=<password>          Password for API Gateway.
  -d --date=<date>                  Date (yyyy-MM-dd; "2020-12-31").
  -ac --asset_class=<asset_class>   Asset Class (lowercase; "commodity", etc).
"""
from docopt import docopt

from api.sdr import Sdr


def main(username, password, asset_class, date):
    sdr = Sdr(username=username, password=password)

    df = sdr.get_transactions_table(date=date, asset_class=asset_class)

    print(df)


if __name__ == "__main__":
    args = docopt(__doc__)

    main(username=args['--username'], password=args['--password'], asset_class=args['--asset_class'],
         date=args['--date'])
