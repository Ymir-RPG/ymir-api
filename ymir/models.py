from ymir import db


def date2str(date):
    if date is None:
        return None
    return date.strftime('%Y-%m-%dT%H:%M:%S')


class World(db.Model):
    __tablename__ = "worlds"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    last_updated = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastUpdated": date2str(self.last_updated),
        }

    def __repr__(self):
        return "<World(name='%s')>" % self.name


class Character(db.Model):
    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    world_id = db.Column(db.Integer, db.ForeignKey("worlds.id"))
    world = db.relationship("World", backref=db.backref("characters", order_by=id))
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"))
    place = db.relationship("Place", backref=db.backref("characters", order_by=id))
    last_updated = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "worldId": self.world_id,
            "placeId": self.place_id,
            "lastUpdated": date2str(self.last_updated),
        }

    def __repr__(self):
        return "<Character(name='%s')>" % self.name


class Place(db.Model):
    __tablename__ = "places"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    world_id = db.Column(db.Integer, db.ForeignKey("worlds.id"))
    world = db.relationship("World", backref=db.backref("places", order_by=id))
    last_updated = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "worldId": self.world_id,
            "lastUpdated": date2str(self.last_updated),
        }

    def __repr__(self):
        return "<Place(name='%s')>" % self.name


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    world_id = db.Column(db.Integer, db.ForeignKey("worlds.id"))
    world = db.relationship("World", backref=db.backref("items", order_by=id))
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"))
    place = db.relationship("Place", backref=db.backref("items", order_by=id))
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))
    character = db.relationship("Character", backref=db.backref("items", order_by=id))
    last_updated = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "worldId": self.world_id,
            "placeId": self.place_id,
            "characterId": self.character_id,
            "lastUpdated": date2str(self.last_updated),
        }

    def __repr__(self):
        return "<Items(name='%s')>" % self.name
