import json
from datetime import datetime

from flask import request, abort
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

from ymir.models import World, Character, Place, Item
from ymir import app, db


def set_session(conn_str):
    app.config['SQLALCHEMY_DATABASE_URI'] = conn_str
    db.create_all()


def _get_request_data(request):
    results = {}
    results.update(request.args)
    results.update(request.form)
    try:
        results.update(json.loads(request.get_data()))
    except ValueError:
        pass
    return results


@app.route("/worlds", methods=["GET"])
def worlds_get():
    data = _get_request_data(request)
    query = db.session.query(World)
    if data.get('chronological', False):
        query = query.order_by(World.last_updated.desc())
    return json.dumps([i.to_dict() for i in query.all()])


@app.route("/worlds", methods=["POST"])
def worlds_post():
    data = _get_request_data(request)
    name = data["name"]
    world = World(name=name, last_updated=datetime.now())
    db.session.add(world)
    db.session.commit()
    return json.dumps(world.to_dict())


@app.route("/worlds/<world_id>", methods=["GET"])
def world_id_get(world_id):
    try:
        return json.dumps(World.query.filter(World.id == world_id).one().to_dict())
    except NoResultFound:
        abort(404)


@app.route("/worlds/<world_id>", methods=["PUT"])
def world_id_put(world_id):
    data = _get_request_data(request)
    world = World.query.filter(World.id == world_id).one()
    world.name = data.get("name", world.name)
    world.last_updated = datetime.now()
    db.session.commit()
    return json.dumps(world.to_dict())


@app.route("/worlds/<world_id>", methods=["DELETE"])
def world_id_delete(world_id):
    try:
        world = World.query.filter(World.id == world_id).one()
    except NoResultFound:
        abort(404)
    db.session.delete(world)
    db.session.commit()
    return ('', 204)


@app.route("/worlds/<world_id>/characters", methods=["GET"])
def characters_get(world_id):
    data = _get_request_data(request)
    query = Character.query.filter(Character.world_id == world_id)
    if data.get('chronological', False):
        query = query.order_by(Character.last_updated.desc())
    if "placeId" in data:
        query = query.filter(Character.place_id == data["placeId"])
    return json.dumps([i.to_dict() for i in query.all()])


@app.route("/worlds/<world_id>/characters", methods=["POST"])
def characters_post(world_id):
    data = _get_request_data(request)
    name = data["name"]
    character = Character(name=name, world_id=world_id)
    if "placeId" in data:
        character.place_id = data["placeId"]
    character.last_updated = datetime.now()
    db.session.add(character)
    db.session.commit()
    return json.dumps(character.to_dict())


@app.route("/worlds/<world_id>/characters/<character_id>", methods=["GET"])
def character_id_get(world_id, character_id):
    try:
        return json.dumps(Character.query.filter(and_(
            Character.world_id == world_id,
            Character.id == character_id)).one().to_dict())
    except NoResultFound:
        abort(404)


@app.route("/worlds/<world_id>/characters/<character_id>", methods=["PUT"])
def character_name_put(world_id, character_id):
    data = _get_request_data(request)
    try:
        character = Character.query.filter(
            and_(Character.world_id == world_id, Character.id == character_id)).one()
    except NoResultFound:
        abort(404)
    character.name = data.get("name", character.name)
    character.place_id = data.get("place_id", character.place_id)
    character.last_updated = datetime.now()
    db.session.commit()
    # TODO(Skyler): If there is no change, we should return a different status
    return json.dumps(character.to_dict())


@app.route("/worlds/<world_id>/characters/<character_id>",
           methods=["DELETE"])
def character_name_delete(world_id, character_id):
    try:
        character = Character.query.filter(
            and_(Character.world_id == world_id, Character.id == character_id)).one()
    except NoResultFound:
        abort(404)
    db.session.delete(character)
    db.session.commit()
    return ('', 204)


@app.route("/worlds/<world_id>/places", methods=["GET"])
def places_get(world_id):
    data = _get_request_data(request)
    query = Place.query.filter(Place.world_id == world_id)
    if data.get('chronological', False):
        query = query.order_by(Place.last_updated.desc())
    return json.dumps([i.to_dict() for i in query.all()])


@app.route("/worlds/<world_id>/places", methods=["POST"])
def places_post(world_id):
    data = _get_request_data(request)
    name = data["name"]
    place = Place(name=name, world_id=world_id)
    place.last_updated = datetime.now()
    db.session.add(place)
    db.session.commit()
    return json.dumps(place.to_dict())


@app.route("/worlds/<world_id>/places/<places_id>", methods=["GET"])
def places_id_get(world_id, places_id):
    try:
        return json.dumps(Place.query.filter(and_(
            Place.world_id == world_id, Place.id == places_id)).one().to_dict())
    except NoResultFound:
        abort(404)


@app.route("/worlds/<world_id>/places/<place_id>", methods=["PUT"])
def places_name_put(world_id, place_id):
    data = _get_request_data(request)
    try:
        place = Place.query.filter(
            and_(Place.world_id == world_id, Place.id == place_id)).one()
    except NoResultFound:
        abort(404)
    place.name = data.get("name", place.name)
    place.last_updated = datetime.now()
    db.session.commit()
    # TODO(Skyler): If there is no change, we should return a different status
    return json.dumps(place.to_dict())


@app.route("/worlds/<world_id>/places/<place_id>",
           methods=["DELETE"])
def places_name_delete(world_id, place_id):
    try:
        place = Place.query.filter(
            and_(Place.world_id == world_id, Place.id == place_id)).one()
    except NoResultFound:
        abort(404)
    db.session.delete(place)
    db.session.commit()
    return ('', 204)


@app.route("/worlds/<world_id>/items", methods=["GET"])
def items_get(world_id):
    data = _get_request_data(request)
    query = Item.query.filter(Item.world_id == world_id)
    if data.get('chronological', False):
        query = query.order_by(Item.last_updated.desc())
    if "placeId" in data:
        query = query.filter(Character.place_id == data["placeId"])
    if "characterId" in data:
        query = query.filter(Item.character_id == data["itemId"])
    return json.dumps([i.to_dict() for i in query.all()])


@app.route("/worlds/<world_id>/items", methods=["POST"])
def items_post(world_id):
    data = _get_request_data(request)
    name = data["name"]
    item = Item(name=name, world_id=world_id)
    if "placeId" in data:
        item.place_id = data["placeId"]
    if "characterId" in data:
        item.character_id = data["characterId"]
    item.last_updated = datetime.now()
    db.session.add(item)
    db.session.commit()
    return json.dumps(item.to_dict())


@app.route("/worlds/<world_id>/items/<item_id>", methods=["GET"])
def item_get(world_id, item_id):
    try:
        return json.dumps(Item.query.filter(and_(
            Item.world_id == world_id,
            Item.id == item_id)).one().to_dict())
    except NoResultFound:
        abort(404)


@app.route("/worlds/<world_id>/items/<item_id>", methods=["PUT"])
def item_put(world_id, item_id):
    data = _get_request_data(request)
    try:
        item = Item.query.filter(
            and_(Item.world_id == world_id, Item.id == item_id)).one()
    except NoResultFound:
        abort(404)
    item.name = data.get("name", item.name)
    item.place_id = data.get("place_id", item.place_id)
    item.character_id = data.get("character_id", item.character_id)
    item.last_updated = datetime.now()
    db.session.commit()
    # TODO(Skyler): If there is no change, we should return a different status
    return json.dumps(item.to_dict())


@app.route("/worlds/<world_id>/items/<item_id>", methods=["DELETE"])
def item_delete(world_id, item_id):
    try:
        item = Item.query.filter(
            and_(Item.world_id == world_id, Item.id == item_id)).one()
    except NoResultFound:
        abort(404)
    db.session.delete(item)
    db.session.commit()
    return ('', 204)
