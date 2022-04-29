from pydantic import BaseModel


class DataModel(BaseModel):
    databaseName: str = 'APPDB'
    collectionName: str = 'ES'
    categoryName: str
    nickName: str
    propertyName: dict
    relationships: dict
