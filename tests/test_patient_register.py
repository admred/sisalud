#!/usr/bin/env python3
import os
import tempfile
import pytest
from random import randint
from webapp import create_app
from webapp.models import init_db

patient=dict(
            username  = 'patient%d'%randint(1,1000),
            password  = '1234',
            password2 = '1234',
            dni       = '%d'%randint(10000000,50999999),
            firstname = 'firstname',
            secondname= 'secondname',
            lastname  = 'lastname',
            phone     = '123456698',
            address   = 'address',
            email     = 'email@example.com',
            socialsecure = ''
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
    r=client.post('/user/create',data=patient)
    assert r.status_code == 302 # found