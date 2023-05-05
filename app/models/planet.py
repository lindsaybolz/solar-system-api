from flask import jsonify
from app import db

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    mass = db.Column(db.Integer)
    moon = db.ForeignKey("planet.moon")


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'mass': self.mass,
        }
    
    @classmethod
    def from_dict(cls, planet_data):
        new_planet = Planet(
            name=planet_data['name'],
            description=planet_data['description'],
            mass=planet_data['mass']
        )
        return new_planet