from sqlalchemy import Column, func,  BigInteger, DateTime,Integer,JSON,String
from Class.DataBase import DataBase as DB

class CufesInformation(DB.base_class):
    __tablename__ = 'cufes_information'

    cufes_information_id = Column(BigInteger, primary_key=True, nullable=False)
    cufes = Column(String(255), nullable=False)
    extracted_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(), default=func.current_timestamp(), nullable=False)
    active = Column(Integer, default=1, nullable=False)

    def __init__(self, cufes_information: dict):
        self.cufes = cufes_information['cufes']
        self.extracted_data = cufes_information["extracted_data"]
    
    def as_dict(self):
        created_at = str(self.created_at) if self.created_at else None
        # Resto del código
        result_dict = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        result_dict["created_at"] = created_at
        return result_dict