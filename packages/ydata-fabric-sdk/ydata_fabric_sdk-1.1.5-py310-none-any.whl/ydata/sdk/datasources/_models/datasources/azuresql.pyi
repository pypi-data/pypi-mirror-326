from dataclasses import dataclass
from ydata.sdk.datasources._models.datasource import DataSource

@dataclass
class AzureSQLDataSource(DataSource):
    query: str = ...
    def to_payload(self) -> None: ...
    def __init__(self, query=...) -> None: ...
