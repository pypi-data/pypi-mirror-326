from _typeshed import Incomplete
from ydata.sdk.common.model import BaseModel
from ydata.sdk.datasources._models.metadata.data_types import DataType, VariableType

class Column(BaseModel):
    model_config: Incomplete
    name: str
    datatype: DataType
    vartype: VariableType
