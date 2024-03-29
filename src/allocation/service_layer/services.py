from __future__ import annotations
from typing import List, Optional
from datetime import date

from sqlalchemy.orm import Session


from allocation.domain import  model
from allocation.domain.model import OrderLine
from allocation.adapters.repository import AbstractRepository
from allocation.service_layer import unit_of_work


class InvalidSku(Exception):
    pass

def is_valid_sku(sku: str, batches: List[model.Batch]):
    return sku in {b.sku for b in batches}

def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], 
              uow: unit_of_work.AbastractUnitOfWork) -> None:
    with uow:
        product = uow.products.get(sku=sku)
        if product is None:
            product = model.Product(sku, batches=[])
            uow.products.add(product)
        product.batches.append(model.Batch(ref, sku, qty, eta))
        uow.commit()

def allocate(orderid: str, sku: str, qty: int,
             uow: unit_of_work.AbastractUnitOfWork) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        product = uow.products.get(sku=line.sku)
        if product is None:
            raise InvalidSku(f"Invalid sku {line.sku}")
        batchref = product.allocate(line)
        uow.commit()
    return batchref