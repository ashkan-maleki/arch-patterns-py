#pylint: disable=protected-access
import model
import repository

from sqlalchemy.orm import Session


def test_repository_can_save_a_batch(session: Session):
    batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)
    
    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)
    
    rows = session.execute(
        'SELECT reference, sku, _purchased_quantity, eta FROM "batches"'
    )
    assert list(rows) == [("batch1", "RUSTY-SOAPDISH", 100, None)]
    
def insert_order_line(session: Session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty)"
        ' VALUES ("order1", "GENERIC-SOFA", 12)'
    )
    [[order_line_id]] = session.execute(
        "SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku",
        dict(orderid="order1", sku="GENERIC-SOFA"),
    )
    return order_line_id

def insert_batch(session: Session, batch_id: str) -> str:
    session.execute(
        "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
        ' VALUES (:batch_id, "GENERIC-SOFA", 100, null)',
        dict(batch_id=batch_id),
    )
    [[batch_id]] = session.execute(
        'SELECT id FROM batches WHERE reference=:batch_id AND sku="GENERIC-SOFA"',
        dict(batch_id=batch_id),
    )
    return batch_id

def insert_allocation(session: Session, orderline_id: int, batch_id: int):
    session.execute(
        "INSERT INTO allocations (orderline_id, batch_id)"
        " VALUES (:orderline_id, :batch_id)",
        dict(orderline_id=orderline_id, batch_id=batch_id),
    )
    

def test_repository_can_retrieve_a_batch_with_allocations(session: Session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)
    
    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")
    
    excepted = model.Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == excepted
    assert retrieved.sku == excepted.sku
    assert retrieved._purchased_quantity == excepted._purchased_quantity
    assert retrieved._allocations == {
        model.OrderLine("order1", "GENERIC-SOFA", 12),
    }