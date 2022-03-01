#!/usr/bin/env python3
import pytest
from random import randint
from webapp import create_app

data=dict(
            profile   = '2',
            username  = 'doctor%d'%randint(1,1000),
            password  = '1234',
            password2 = '1234',
            dni       = '%d'%randint(10000000,50999999),
            firstname = 'firstname',
            secondname= 'secondname',
            lastname  = 'lastname',
            phone     = '123456698',
            address   = 'address',
            email     = 'email@example.com',
            license_  = '%d'%randint(1,100000000),
            speciality= '1',
            )
class TestingConfig():
    TESTING= True
    WTF_CSRF_ENABLED=False

@pytest.fixture()
def app():
    app = create_app(TestingConfig)
    return app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_register(client):
    r=client.post('/auth/login',data={
        'username':'admin',
        'password':'1234',
        },follow_redirects=True)
    assert r.status_code == 200

    r=client.post('/user/create',data=data,follow_redirects=True)
    assert r.status_code == 200
