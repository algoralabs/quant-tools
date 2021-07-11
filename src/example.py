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

    print(f"Getting transaction table by date {date}.")
    df = sdr.get_transactions_table(date=date, asset_class=asset_class)

    print(df)

    print("Getting unique enum values. You can use these values to query a table view.")
    response = sdr.get_enum_values(asset_class=asset_class)

    print(response)
    print()

    filters = [
        {
            "field": "repository",
            "operator": "IN",
            "selected_values": [
                "CME",
                "DTCC",
                "ICE"
            ]
        }, {
            "field": "sector",
            "operator": "IN",
            "selected_values": [
                "Energy"
            ]
        }
    ]
    df = sdr.get_transactions_view(asset_class=asset_class, filters=filters)

    print(f"Getting transaction view with filters.\n{filters}")
    print(df)


if __name__ == "__main__":
    args = docopt(__doc__)

    main(username=args['--username'],
         password=args['--password'],
         asset_class=args['--asset_class'],
         date=args['--date'])
