# -*- coding: utf-8 -*-
from flask import Blueprint,jsonify
from webapp.models import *
from sqlalchemy.orm import aliased
from datetime import datetime,timedelta

bp=Blueprint('ajax',__name__)


@bp.route('/speciality')
@bp.route('/speciality/<int:_id>')
def speciality(_id=None):
    if _id is None:
        query=db.session.query(Speciality).join(Doctor)
    else:
        query=db.session.query(Doctor).filter(Doctor.speciality_id==_id)
    query=query or []
    return jsonify(data=[ (q.id,q.name) for q in query ])


@bp.route('/doctor_by_speciality/<int:_id>')
def doctor_by_speciality(_id):

    query=[ (q.id,q.fullname) for q in Doctor.query.filter_by(speciality_id=_id) ]

    return jsonify(data=query)


@bp.route('/turn_by_doctor/<int:_id>')
def turn_by_doctor(_id):
    query=(Turn.query
            .filter(
                Turn.doctor_id==_id,
                Turn.is_available==True,
                Turn.when >=datetime.today(),
                )
            .order_by(Turn.when.asc())
            .limit(20)
            )
    if query:
        data=[ (x.id,str(x.when)) for x in query ]
    else:
        data=[]
    return jsonify(data=data )

@bp.get('/turn_by_id/<int:_id>')
def turn_by_id(_id):

    query=(db.session
            .query(Turn,Doctor)
            .filter(
                Turn.doctor_id == Doctor.id,
                Turn.id == _id,
                )
            .group_by(Turn)
            .first()
            )
    if not query:
        data=[]
    else:
        t,d=query
        data={
                'turn_id':t.id,
                'when':str(t.when),
                'duration':t.duration,
                'is_available':t.is_available,
                'is_missed':t.is_missed,
                'doctor_id':t.doctor_id,
                'patient_id':t.patient.id,
                'speciality_id':d.speciality_id
                }

    return jsonify(data=data)


"""
@bp.get('/doctor_by_id/<int:_id>')
def doctor_by_id(_id):
    query=Doctor.query.get(_id)
    if not query:
        query=[]

    else:
        query=

"""


@bp.get('/patient_by_id/<int:_id>')
def patient_by_id(_id):

    p=Patient.query.get(_id)
    if not p:
        data=None
    else:
        data={'id':p.id,'fullname':p.fullname}

    return jsonify(data=data)

@bp.get('/patient_by_dni/<int:dni>')
def patient_by_dni(dni):
    p=Patient.query.filter_by(dni=dni).first()
    if not p:
        data=None
    else:
        data={'id':p.id,'dni':p.dni,'fullname':p.fullname}

    return jsonify(data=data)
