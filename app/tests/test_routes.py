from werkzeug.exceptions import HTTPException
from app.models.planet import Planet
from app.routes.planets import validate_model
import pytest

def test_get_planets_with_no_records(client):
    # act
    response = client.get('/planets')
    response_body = response.get_json()

    # assert
    assert response_body == []
    assert response.status_code == 200

def test_get_one_planet(client, two_saved_planets):
    # act
    response = client.get('/planets/1')
    response_body = response.get_json()

    # assert
    assert response_body == {"id": 1,
        "name": "Earth",
        "mass": 5,
        "description": "Home Planet"}
    
    assert response.status_code == 200

def test_get_one_planet_with_no_data(client):
    # act
    response = client.get('/planets/1')
    response_body = response.get_json()

    # assert
    assert response_body == {"message": "Planet 1 is not found"}
    
    assert response.status_code == 404

def test_get_all_planets(client, two_saved_planets):
    # act
    response = client.get('/planets')
    response_body = response.get_json()

    # assert
    assert response_body == [{"id": 1,
        "name": "Earth",
        "mass": 5,
        "description": "Home Planet"},

        {"id": 2,
        "name": "Mars",
        "mass": 3,
        "description": "Martians' home"}
        ]
    
    assert response.status_code == 200

def test_post_one_planet(client):
    # act
    response = client.post('/planets', json= {
        "name": "Earth",
        "mass": 5,
        "description": "Home Planet"})
    response_body = response.get_json()

    # assert
    assert response_body == "Planet 1 successfully created."
    assert response.status_code == 201


def test_post_one_planet_with_no_name(client):
    # act
    response = client.post('/planets', json= {
        "mass": 5,
        "description": "Home Planet"})
    response_body = response.get_json()

    # assert
    assert response_body == {'message': 'Planet input data incomplete.  Make sure you ahve a name, description and mass.'}
    assert response.status_code == 400


def test_post_one_planet_with_no_description(client):
    # act
    response = client.post('/planets', json= {
        "name": "Earth",
        "mass": 5,})
    response_body = response.get_json()

    # assert
    assert response_body == {'message': 'Planet input data incomplete.  Make sure you ahve a name, description and mass.'}
    assert response.status_code == 400

def test_post_one_planet_with_no_mass(client):
    # act
    response = client.post('/planets', json= {
        "name": "Earth",
        "description": "Home Planet"})
    response_body = response.get_json()

    # assert
    assert response_body == {'message': 'Planet input data incomplete.  Make sure you ahve a name, description and mass.'}
    assert response.status_code == 400


def test_validate_model_returns_model(two_saved_planets):
    # Arrange
    model_id = 1
    model = Planet

    # Act
    output = validate_model(model, model_id)

    # Assert
    assert output == Planet.query.get(model_id)

def test_validate_model_returns_invalid_id(two_saved_planets):
    with pytest.raises(HTTPException):
        result = validate_model(Planet, "cat")

def test_validate_model_returns_not_found(two_saved_planets):
    with pytest.raises(HTTPException):
        result = validate_model(Planet, 3)