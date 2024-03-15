from __future__ import annotations
from typing import List, Optional
from datetime import date

from sqlalchemy.orm import Session

import domain.model as model
from domain.model import OrderLine
from adapters.repository import AbstractRepository


class InvalidSku(Exception):
    pass

def is_valid_sku(sku: str, batches: List[model.Batch]):
    return sku in {b.sku for b in batches}

def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], 
              repo: AbstractRepository, session: Session) -> None:
    repo.add(model.Batch(ref, sku, qty, eta))
    session.commit()

def allocate(line: OrderLine, repo: AbstractRepository, session: Session) -> str:
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref