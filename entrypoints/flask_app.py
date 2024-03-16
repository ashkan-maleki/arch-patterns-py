from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import domain.model as model
from adapters import orm
from adapters import repository
import service_layer.services as services

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_progress_uri()))
app = Flask(__name__)



@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    line = model.OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"]
    )
    
    try:
        batchref = services.allocate(line, repo, session)
    except (model.OutOfStock, services.InvalidSku) as e:
        return {"message": str(e)}, 400
    
    return {"batchref": batchref}, 201