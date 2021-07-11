import pandas as pd

from api.api_gateway import ApiGateway


class Sdr(ApiGateway):
    def __init__(self, username, password, extension='/data'):
        super().__init__(username=username, password=password)
        self.extension = extension

    def get_transactions_table(self, date, asset_class, repository='CME,DTCC,ICE'):
        response = self.authenticated_request(
            uri=f'{self.extension}/sdr/{asset_class}/{date}?repository={repository}'
        )

        df = pd.DataFrame.from_records(response)

        return df

    def get_transactions_view(self, asset_class, filters):
        response = self.authenticated_request(
            uri=f'{self.extension}/sdr/{asset_class}/view',
            method='POST',
            json=filters
        )

        df = pd.DataFrame.from_records(response)

        return df

    def get_enum_values(self, asset_class):
        response = self.authenticated_request(
            uri=f'{self.extension}/sdr/{asset_class}/enum',
            method='GET'
        )

        return response
