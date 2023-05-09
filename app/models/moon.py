from app import db
from app.models.planet import Planet

class Moon(db.Model):
    # def __init__(self, id, name, planet):
    #     self.id = id
    #     self.name = name
    #     self.planet = planet
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    planet = db.relationship("Planet", back_populates= "moons")
    name = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "planet": self.planet.name,
            "name": self.name
        }
    
    @classmethod
    def from_dict(cls, dict_data):
        return Moon(name=dict_data["name"])
