from typing import Set, List
import pytest

import domain.model as model
from adapters import repository
from service_layer import services
from service_layer import unit_of_work

class FakeRepository(repository.AbstractRepository):
    def __init__(self, batches: List[model.Batch]) -> None:
        self._batches: Set[model.Batch] = set(batches)
        
    def add(self, batch: model.Batch) -> None:
        self._batches.add(batch)
        
    def get(self, reference: str) -> model.Batch:
        return next(b for b in self._batches 
                    if b.reference == reference)
        
    def list(self):
        return list(self._batches)
        

class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.batches = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass

def test_add_batch():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)
    assert uow.batches.get("b1") is not None
    assert uow.committed
        
def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "COMPLICATED-LAMP", 100, None, uow)
    result = services.allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert result == "b1"
    
def test_allocate_error_for_invalid_sku():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "AREALSKU", 100, None, uow)
    
    with pytest.raises(services.InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        services.allocate("o1", "NONEXISTENTSKU", 10, uow)
        
def test_commits():
    uow = FakeUnitOfWork()
    services.add_batch("b1", "OMINOUS-MIRROR", 100, None, uow)
    services.allocate("o1", "OMINOUS-MIRROR", 10, uow)
    assert uow.committed is True