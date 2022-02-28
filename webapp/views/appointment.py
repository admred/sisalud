# -*- coding: utf-8 -*-
from flask import redirect,render_template,request,url_for,abort,session,abort,Blueprint,flash,current_app,g
from webapp.models import Appointment,db,Doctor
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from webapp.forms import AppointmentFormCreate,AppointmentFormUpdate
from sqlalchemy import select,or_
import re
from datetime import timedelta
bp=Blueprint('appointment',__name__)


"""
   NOTE: Patients shouldn't be allowed to access this endpoint
"""
@bp.route('/create',methods=('GET','POST'))
def create():
    title='Crear'
    form=AppointmentFormCreate(request.form)

    if g.profile == 'doctor':
        form.doctor.data=Doctor.query.get(session['userid'])


    if form.validate_on_submit():
        obj=Appointment()
        form.populate_obj(obj)

        try:
            db.session.add(obj)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(str(ex))
            flash(str(ex),'danger')
            return render_template('appointment/form.html',form=form,title=title)


        flash('Operacion exitosa','success')
        """
        next_date=obj.when + timedelta(hours=int(obj.duration))
        form.when.raw_data=[next_date.strftime('%Y-%m-%dT%H:%M')]
        """
        return redirect(url_for('.list'))

    if g.profile == 'doctor':
        del form.doctor
    return render_template('appointment/form.html',form=form,title=title)

"""
   NOTE: Patients shouldn't be allowed to access this endpoint
"""
@bp.route('/update/<int:_id>',methods=('GET','POST'))
def edit(_id=0):
    title='Actualizar'

    obj=Appointment.query.get(_id)
    if not obj:
        flash('Agenda no encontrado','danger');
        return redirect(url_for('.list'))

    form=AppointmentFormUpdate(request.form,obj=obj)
    if g.profile == 'doctor':
        form.doctor.data=Doctor.query.get(session['userid'])

    if form.validate_on_submit():


        form.populate_obj(obj)

        try:
            if not _id:
                db.session.add(obj)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(str(ex))
            flash(str(ex),'danger')
            return render_template('form.html',form=form,title=title)

        flash('Operacion exitosa','success')
        return redirect(url_for('.list'))

    if g.profile == 'doctor':
        del form.doctor

    return render_template('appointment/form.html',form=form,title=title)

@bp.get('/detail/<int:_id>')
def detail(_id):
    title='Detalle'
    obj=Appointment.query.get(_id)
    form=AppointmentFormUpdate(obj=obj)
    return render_template('form.html',form=form,title=title)


@bp.post('/delete')
@bp.post('/delete/<int:idx>')
def delete(idx=0):
    ids=[]
    if idx != 0 :
        ids.append(idx)
    elif  idx == 0 and request.form.get('marca',None):
        ids=request.form.getlist('marca')
    else:
        flash('Debe marcar al menos un item','warning')
        return redirect(url_for('.list'))

    for idx in ids :
        obj=Appointment.query.get(idx)
        if not obj:
            flash('El registro no exite','danger')
            return redirect(url_for('.list'))
        try:
            db.session.delete(obj)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(str(ex))
            flash(str(ex),'danger')
            return redirect(url_for('.list'))

    flash('Se elimino uno o mas registros','success')
    return redirect(url_for('.list'))


@bp.route('/search')
@bp.route('/list')
def list():
    title='Listado'


    query=(db.session
        .query(Appointment,Doctor)
        .filter(
            Doctor.id==Appointment.doctor_id,
            )
        )

    if g.profile == 'doctor':
        query=query.filter(Doctor.id==session['userid'])

    q=request.args.get('q','',str).strip()
    if q and re.match('^[\w\s,/:.-]{1,30}$',q):
        words=q.split(', ')

        paginated=(query.filter(
                            or_(
                                Appointment.when.like(f'%{q}%'),
                                Doctor.firstname.in_(words),
                                Doctor.secondname.in_(words),
                                Doctor.lastname.in_(words),
                            )
                        )
                    .group_by(Appointment)
                    .paginate(per_page=20)
                    )
    else:
        paginated=query.group_by(Appointment).paginate(per_page=20)

    rows=[
        (
            a.id,
            a.when,
            d.fullname,
            "Si" if a.is_canceled else "No",
            a.duration
        ) for a,d in paginated.items ]



    headers=('Fecha y Hora','Medico','Cancelado','Duracion (horas)')
    return render_template('list.html',rows=rows,paginated=paginated,headers=headers,title=title)
