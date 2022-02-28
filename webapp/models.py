# -*- coding: utf-8 -*-
import click
from flask import current_app as app
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

db = SQLAlchemy()

class Access(db.Model):
    __tablename__ = 'access'
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(10), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    is_writable = db.Column(db.Boolean, default=False)

    profile = db.relationship('Profile', back_populates='accesses')

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    accesses = db.relationship('Access')
    users = db.relationship('User')


    def __str__(self):
        return self.name

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer, unique=True,nullable=False)
    username = db.Column(db.String(30), nullable=False,unique=True)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    secondname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(30), nullable=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))

    profile = db.relationship('Profile', back_populates='users')


    def __str__(self):
        return self.fullname

    def setPassword(self, pw):
        self.password = generate_password_hash(pw)

    def checkPassword(self, pw):
        return check_password_hash(pw, db.password)

    @property
    def fullname(self):
        return u'%s, %s %s'%(self.lastname,self.firstname,self.secondname)

    _type = db.Column(db.String(30), nullable=True)
    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':_type
    }

class Doctor(User):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    license_ = db.Column(db.Integer)
    speciality_id = db.Column(db.Integer, db.ForeignKey('speciality.id'))

    speciality = db.relationship('Speciality', back_populates='doctors')
    appointments = db.relationship('Appointment')
    turns = db.relationship('Turn')

    __mapper_args__ = {
            'polymorphic_identity':'doctor',
            }

class Patient(User):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    socialsecure_id = db.Column(db.Integer, db.ForeignKey('socialsecure.id'))

    socialsecure = db.relationship('SocialSecure', back_populates='patients')
    turns = db.relationship('Turn')

    __mapper_args__ = {
            'polymorphic_identity':'patient',
            }


class Speciality(db.Model):
    __tablename__ = 'speciality'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60),nullable=False)
    description = db.Column(db.Text(4096), nullable=True)

    doctors = db.relationship('Doctor')


    def __str__(self):
        return self.name

class SocialSecure(db.Model):
    __tablename__ = 'socialsecure'
    id = db.Column(db.Integer, primary_key=True)
    rnos = db.Column(db.Integer, nullable=True)
    short = db.Column(db.String(30), nullable=True)
    name = db.Column(db.String(255), nullable=False )
    address = db.Column(db.String(255),nullable=False)
    phone = db.Column(db.String(30))
    email = db.Column(db.String(30))

    patients = db.relationship('Patient')


    def __str__(self):
        return self.name

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    when = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # hours
    is_canceled = db.Column(db.Boolean(),default=False)

    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    doctor = db.relationship('Doctor', back_populates='appointments' )




class Turn(db.Model):
    __tablename__ = 'turn'
    id = db.Column(db.Integer, primary_key=True)
    when = db.Column(db.DateTime,nullable=False)
    duration = db.Column(db.Integer())
    is_available = db.Column(db.Boolean(), default=True)
    is_missed = db.Column(db.Boolean(), default=False)
    is_canceled = db.Column(db.Boolean(), default=False)

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))

    patient = db.relationship('Patient', back_populates='turns')
    doctor = db.relationship('Doctor', back_populates='turns')



# FIXED :  avoid "AssertionError: No such polymorphic_identity ..."
class Admin(User):
    __tablename__ = 'admin'
    __mapper_args__ = {
            'polymorphic_identity':'admin',
            }
class Receptionist(User):
    __tablename__ = 'receptionist'
    __mapper_args__ = {
            'polymorphic_identity':'receptionist',
            }


@click.command('init-db', short_help = 'Inicialize  DB')
@with_appcontext
def init_db():

    db.init_app(app)
    db.drop_all()
    db.session.commit()
    db.create_all()
    db.session.commit()
    with db.engine.connect() as conn:
        # profiles
        conn.exec_driver_sql('INSERT INTO profile (id,name) VALUES (?,?)',[
        (1,'admin',),
        (2,'doctor',),
        (3,'patient',),
        (4,'receptionist',)
        ])

        # TODO : re-work this !!
        conn.exec_driver_sql('INSERT INTO access (profile_id, endpoint, is_writable)  VALUES (?,?,?)',[
            (1, 'user',True),
            (1, 'speciality',True),
            (1, 'socialsecure',True),
            (1, 'schedule',False),
            (1, 'turn',True),
            (1, 'appointment',True),
            (2, 'user',False),
            (2, 'speciality',False),
            (2, 'socialsecure',False),
            (2, 'schedule',False),
            (2, 'turn',True),
            (2, 'appointment',True),
            (3, 'user',False),
            (3, 'speciality',False),
            (3, 'socialsecure',False),
            (3, 'schedule',False),
            (3, 'turn',False),
            (4, 'user',True),
            (4, 'speciality',True),
            (4, 'socialsecure',True),
            (4, 'schedule',False),
            (4, 'turn',True),
            (4, 'appointment',False)
        ])


        # admin:1234
        conn.exec_driver_sql('INSERT INTO user (username, password, dni, firstname, secondname, lastname,profile_id,_type) VALUES (?,?,?,?,?,?,?,?)',[
            ('admin', 'pbkdf2:sha256:260000$LV7blDpwoLr9UBQz$6fbcab58aa092124df94cd5b10fecff8565cef2c68e544cb0272d7fc836d1454',11222333,'Marcos','Esteban','Bethoven',1,'admin')
            ])

    db.session.commit()
    click.echo('DB it was initizalized. Your username is "admin", your password is "1234". Do not forget change it.')


"""
@app.teardown_appcontext
def close_connection(exception):
    #db = getattr(g, '_database', None)
    if db is not None:
        db.close()
"""
