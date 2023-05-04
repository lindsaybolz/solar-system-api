import pytest
from app import create_app 
from app import db
from app.models.planet import Planet
from app.models.moon import Moon
from flask.signals import request_finished

@pytest.fixture
def app():
    app = create_app(test_config=True)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()
    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()     

@pytest.fixture
def two_saved_planets():   
    planet_1 = Planet(
        name = "Earth",
        mass = 5,
        description = "Home Planet"
    )

    planet_2 =  Planet( 
        name = "Mars",
        mass = 3,
        description = "Martians' home"
    )

    db.session.add_all([planet_1, planet_2])
    db.session.commit()