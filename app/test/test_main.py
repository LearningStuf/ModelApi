from fastapi.testclient import TestClient
from fastapi import Depends
from src.main import app
from src import models
import pytest
import json


client = TestClient(app)


def test_correctValue_post():
    response = client.post("/bot-score",json={"x1" : 0.5, "x2" : 0.5})
    assert response.status_code == 200

def test_incorrectValue_post():
    response = client.post("/bot-score",json={"x1" : "a", "x2" : 0.5})
    assert response.status_code == 422

def test_extraValue_post():
    response = client.post("/bot-score",json={"x1" : 0.7, "x2" : 0.5, "x3" : 0.99 })
    assert response.status_code == 422

def test_intValue_post():
    response = client.post("/bot-score",json={"x1" : "1", "x2" : "2" })
    assert response.status_code == 200

def test_emptyValue_post():
    response = client.post("/bot-score",json={"x1" : "", "x2" : "" })
    assert response.status_code == 422

def test_protected_EmptyHeader_post():
    response = client.post("/protected/bot-score",json={"x1" : "", "x2" : "" })
    assert response.status_code == 403

def test_register_user_post():
    response = client.post("/register",json={"username" : "TestCase1", "password" : "123password" })
    assert response.status_code == 200

def test_register_error_post():
    response = client.post("/register",json={"username" : "TestCase1", "password" : "123password" })
    assert response.status_code == 400

def test_login_post():
    response = client.post("/login",json={"username" : "TestCase1", "password" : "123password" })
    assert response.status_code == 200

def test_login_error_post():
    response = client.post("/login",json={"username" : "TestCase1", "password" : "1234password" })
    assert response.status_code == 401

def test_protected_withoutAuthHeader_post():
    response = client.post("/protected/bot-score",json={"x1" : "", "x2" : "" })
    assert response.status_code == 403

def test_protected_withAuthHeader_post():
    response = client.post("/login",json={"username" : "TestCase1", "password" : "123password" })
    response_data = response.json()
    
    token = response_data['token']
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    response = client.post("/protected/bot-score",json={"x1" : "1", "x2" : "1" }, headers=headers)
    assert response.status_code == 200
