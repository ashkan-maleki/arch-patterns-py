from __future__ import annotations
import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

import src.allocation.config as config
from adapters import repository

class AbstractUnitOfWork(abc.ABC):
    products: repository.AbstractRepositroy
    
    def __enter__(self) -> AbstractUnitOfWork:
        return self
    
    def __exit__(self, *args):
        self.rollback()
        
    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError
    
    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
    
DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_progress_uri(),
    )
)

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY) -> None:
        self.session_factory = session_factory
        
    def __enter__(self) -> SqlAlchemyUnitOfWork:
        self.session = self.session_factory()
        self.products = repository.SqlAlchemyRepository(self.session)
        return super().__enter__()
    
    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()
        
    def commit(self):
        self.session.commit()
    
    def rollback(self):
        self.session.rollback()