# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField,SelectField,BooleanField,StringField,IntegerField,PasswordField,TextAreaField
from wtforms.widgets import PasswordInput
from wtforms.fields.html5 import DateTimeLocalField,DateField,TimeField,EmailField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Length,DataRequired,EqualTo,Optional

from webapp.models import *

class TurnFormCreate(FlaskForm):
    when=DateTimeLocalField('Fecha y Hora',format="%Y-%m-%dT%H:%M",render_kw={'step':'900','min':'0','max':'2700'})
    doctor=QuerySelectField('Medico', query_factory=lambda:Doctor.query)

    duration=SelectField('Duracion',choices=[(15,'15 min'),(30,'30 min'),(60,'60 min')])

class TurnFormRequest(FlaskForm):
    doctor=QuerySelectField('Medico', query_factory=lambda:Doctor.query)
    patient_id=IntegerField('',validators=[DataRequired()])

class TurnFormEdit(FlaskForm):
    when=DateTimeLocalField('Fecha y Hora',format="%Y-%m-%dT%H:%M",render_kw={'class':'form-control','disabled':'','readonly':''})
    doctor=QuerySelectField('Medico', query_factory=lambda:Doctor.query)
    patient=QuerySelectField('Paciente',query_factory=lambda:Patient.query ,get_label='fullname',allow_blank=True,render_kw={'class':'form-control'})
    duration=SelectField('Duracion (minutos)',choices=[(15,'15 min'),(30,'30 min'),(60,'60 min')],render_kw={'class':'form-control','disabled':'','readonly':''})
    is_missed=BooleanField('Perdido')
    is_available=BooleanField('Disponible')
    is_canceled=BooleanField('Cancelado')



class AppointmentFormUpdate(FlaskForm):
    when=DateTimeLocalField('Fecha y Hora',format="%Y-%m-%dT%H:%M",validators=[DataRequired()])
    doctor=QuerySelectField('Medico', query_factory=lambda:Doctor.query,validators=[DataRequired()])
    duration=IntegerField('Duracion (horas)',validators=[DataRequired()])
    is_canceled = BooleanField('Cancelado',default=False)

class AppointmentFormCreate(FlaskForm):
    when=DateTimeLocalField('Fecha y Hora',format="%Y-%m-%dT%H:%M",validators=[DataRequired()])
    doctor=QuerySelectField('Medico', query_factory=lambda:Doctor.query,validators=[DataRequired()])
    duration=IntegerField('Duracion (horas)',validators=[DataRequired()])

class SearchTurnoForm(FlaskForm):
    dni=IntegerField('DNI',description='DNI del paciente',validators=[DataRequired()])

class UserForm(FlaskForm):
    profile=QuerySelectField('Perfil',query_factory=lambda:Profile.query,get_label='name')

    username=StringField(u'Usuario',description="Obligatorio",validators=[DataRequired()])
    password=StringField(u'Clave',description="Obligatorio",validators=[DataRequired(),EqualTo('password2',message='Las claves debe coincidir')],widget=PasswordInput(hide_value=False) )
    password2=StringField(u'Repetir Clave',description="Obligatorio",validators=[DataRequired(),EqualTo('password',message='Las claves debe coincidir')],widget=PasswordInput(hide_value=False) )

    dni=IntegerField(u'DNI',description="Obligatorio",validators=[DataRequired()])
    firstname=StringField(u'Primer Nombre',description="Obligatorio",validators=[DataRequired()])
    secondname=StringField(u'Segundo Nombre',description="Obligatorio",validators=[DataRequired()])
    lastname=StringField(u'Apellido',description="Obligatorio",validators=[DataRequired()])
    address=StringField(u'Domicilio')
    phone=StringField(u'Telefono')
    email=EmailField(u'Email')

    license_=IntegerField(u'Matricula')
    socialsecure=QuerySelectField('Cobertura',query_factory=lambda:SocialSecure.query,get_label='name',allow_blank=True)
    speciality=QuerySelectField('Especialidad',query_factory=lambda:Speciality.query,get_label='name',allow_blank=True)


    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        self.password2.data=self.password.data


class LoginForm(FlaskForm):
    username=StringField(u'Usuario',validators=[DataRequired()])
    password=PasswordField(u'Contraseña',validators=[DataRequired()])

class SpecialityForm(FlaskForm):
    name = StringField('Nombre',validators=[DataRequired(),Length(max=60)])
    description = TextAreaField(u'Descripción',validators=[Length(max=4000)],render_kw={'rows':10} )

class SocialSecureForm(FlaskForm):
    rnos = IntegerField('RNOS',description='Numero de Registro de Obra Social',validators=[Optional()])
    short = StringField('Siglas',validators=[Length(max=30)])
    name = StringField('Nombre',validators=[DataRequired(),Length(max=255)])
    address = StringField('Domicilio',validators=[DataRequired(),Length(max=255)])
    phone = StringField('Telefono')
    email = EmailField('Email')


class ScheduleForm(FlaskForm):
    speciality=StringField('Especialidad')
    doctor=StringField('Medico')
    from_=StringField('Desde')
    to=StringField('Hasta')
