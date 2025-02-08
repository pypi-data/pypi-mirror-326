from dataclasses import dataclass
from ydata.sdk.datasources._models.datasource import DataSource
from ydata.sdk.datasources._models.filetype import FileType

@dataclass
class AzureBlobDataSource(DataSource):
    filetype: FileType = ...
    path: str = ...
    separator: str = ...
    def to_payload(self): ...
    def __init__(self, filetype=..., path=..., separator=...) -> None: ...
