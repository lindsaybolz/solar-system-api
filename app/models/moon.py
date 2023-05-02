from app import db
from app.models.planet import Planet
from sqlalchemy.orm import relationship, backref

class Moon(db.Model):
    # def __init__(self, id, name, planet):
    #     self.id = id
    #     self.name = name
    #     self.planet = planet
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    planet = db.relationship("Planet", backref= backref("planet", uselist=False))

    name = db.Column(db.String)
