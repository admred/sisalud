# -*- coding: utf-8 -*-
from flask import redirect,render_template,request,url_for,abort,session,abort,Blueprint,flash,current_app,g
from webapp.models import *
from datetime import datetime , timedelta
from sqlalchemy import or_
import re
from webapp.forms import ScheduleForm

bp=Blueprint('schedule',__name__)


@bp.get('/search')
@bp.get('/list')
def list():
    title='Horarios'


    query=(db.session
        .query(Appointment,Doctor,Speciality)
        .filter(
            Appointment.doctor_id == Doctor.id,
            Speciality.id == Doctor.speciality_id,
            Appointment.when >= datetime.today(),
            )
        .group_by(Appointment)
        .order_by(Speciality.name)
        )
    q=request.args.get('q','',str).strip()
    if q and re.match('^[\w\s,:.-]{1,30}$',q):
        paginated=(query.filter(
                or_(
                    Appointment.when.like(f'%{q}%'),
                    Speciality.name.ilike(f'%{q}%'),
                    ))
            .group_by(Appointment)
            .order_by(Speciality.name)
            .paginate(per_page=20)
            )

    else:
        paginated=(query
            .group_by(Appointment)
            .order_by(Speciality.name)
            .paginate(per_page=20)
            )


    rows = [
                (
                    a.id,
                    s.name,
                    d.lastname,
                    a.when,
                    a.when+timedelta(hours=a.duration),
                )
            for a,d,s in paginated.items
        ]
    headers = ('Especialidad','Medico','Desde','Hasta' )
    return render_template('list.html',rows=rows,paginated=paginated,headers=headers,title=title)


@bp.get('/detail/<int:_id>')
def detail(_id):
    title="Detalle"
    query=(db.session
        .query(Appointment,Doctor,Speciality)
        .filter(
            Appointment.doctor_id == Doctor.id,
            Speciality.id == Doctor.speciality_id,
            Appointment.when >= datetime.today(),
            Appointment.id == _id,
            )
        .group_by(Appointment)
        .order_by(Speciality.name)
        .first()
        )
    if not query:
        return abort(501)

    form=ScheduleForm(data={
        'speciality':query.Speciality.name,
        'doctor':query.Doctor.fullname,
        'from_':query.Appointment.when,
        'to': query.Appointment.when+timedelta(hours=query.Appointment.duration),
        })


    return render_template('form.html',title=title,form=form)