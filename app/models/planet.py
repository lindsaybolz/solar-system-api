from flask import jsonify
class Planet:
    def __init__(self, id, name, description, mass):
        self.id = id
        self.name = name
        self.description = description
        self.mass = mass

    def __str__(self):
        return str({
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "mass": self.mass
        })