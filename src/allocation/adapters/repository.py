import abc
import domain.model as model
from typing import List
from sqlalchemy.orm import Session


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, product: model.Product) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get(self, sku: str) -> model.Product:
        raise NotImplementedError

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session) -> None:
        self.session = session
        
    def add(self, product: model.Product) -> None:
        self.session.add(product)
        
    def get(self, sku: str) -> model.Product:
        return self.session.query(model.Product).filter_by(sku=sku).first()
    
    
    