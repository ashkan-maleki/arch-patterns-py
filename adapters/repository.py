import abc
import domain.model as model
from typing import List
from sqlalchemy.orm import Session


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get(self, reference: str) -> model.Batch:
        raise NotImplementedError

class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session) -> None:
        self.session = session
        
    def add(self, batch: model.Batch) -> None:
        self.session.add(batch)
        
    def get(self, reference: str) -> model.Batch:
        return self.session.query(model.Batch).filter_by(reference=reference).one()
    
    def list(self) -> List[model.Batch]:
        return self.session.query(model.Batch).all()
    