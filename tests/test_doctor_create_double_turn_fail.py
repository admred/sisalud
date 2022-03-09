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

turn=dict(
        when = '2022-10-01T11:00',
        duration = '60',
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

def test_doctor_create_double_turn_fail(client):
    # first step register doctor with admin account
    r=client.post('/auth/login',data={
        'username':'admin',
        'password':'1234',
        },follow_redirects=True)
    assert r.status_code == 200

    r=client.post('/user/create',data=data,follow_redirects=True)
    assert r.status_code == 200 

    r=client.get('/auth/logout',follow_redirects=True)
    assert r.status_code == 200 
    
    # second login as doctor
    r=client.post('/auth/login',data={
        'username':data['username'],
        'password':data['password'],
        },follow_redirects=True)
    assert r.status_code == 200 
    
    # first OK
    r=client.post('/turn/create',data=turn,follow_redirects=True)
    assert  "Se dio de alta un turno" in str(r.data)

    # second it must fail
    r=client.post('/turn/create',data=turn,follow_redirects=True)
    assert  "El turno ya esta registrado" in str(r.data)
