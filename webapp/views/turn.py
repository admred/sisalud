# -*- coding: utf-8 -*-
from flask import redirect,render_template,request,url_for,abort,session,Blueprint,flash,current_app,g
from webapp.models import *
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from webapp.forms import TurnFormCreate,TurnFormRequest,TurnFormEdit
from datetime import timedelta,datetime
import re

bp=Blueprint('turn',__name__)

@bp.route('/update/<int:_id>',methods=('GET','POST'))
def update(_id):
    title='Modificar'
    obj=Turn.query.get(_id)
    if not obj :
        return abort(404)

    form=TurnFormEdit(request.form,obj=obj)

    # FIXED: Bug? BooleanField is not set
    if request.method == 'GET':
        form.is_missed.data=obj.is_missed
        form.is_available.data=obj.is_available
        form.is_canceled.data=obj.is_canceled


    if g.profile == 'doctor':
        form.doctor.data=g.current_user
        form.doctor.render_kw={'selected':'','readonly':'','disabled':''}
    

    if form.validate_on_submit():
        form.populate_obj(obj)
        if obj.patient_id:
            obj.is_available=False
        else:
            obj.is_available=True

        try:
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(str(ex))
            flash(str(ex),'danger')
            return render_template('form.html',title=title,turn_id=_id,form=form)

        flash('Operacion exitosa','success')
        return redirect(url_for('.list'))

    return render_template('form.html',title=title,form=form)

@bp.get('/detail/<int:_id>')
def detail(_id):
    title='Detalle'
    obj=Turn.query.get(_id)
    form=TurnFormEdit(obj=obj)
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
        obj=Turn.query.get(idx)
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



@bp.route('/list')
def list():
    title='Listado de todos los turnos'

    # FIXED: SQLAlchemy can not resolve inherance at same time on query
    aPatient=aliased(User)

    query=(db.session
            .query(Turn,Doctor,aPatient)
            .join(Doctor,Doctor.id==Turn.doctor_id)
            .outerjoin(aPatient,Turn.patient_id==aPatient.id)
            .group_by(Turn)
            )
    if g.profile == 'doctor':
        query=query.filter(Doctor.id==session['userid'])
    elif g.profile == 'patient':
        query=query.filter(aPatient.id==session['userid'])

    """ user submit a search, do a filtered list"""
    q=request.args.get('q','',str).strip()

    if q and re.match('^[\w\s,:.-]{1,30}$',q):
        words=q.split(', ')
        paginated=(query.filter(
                or_(
                    Doctor.firstname.in_(words),
                    Doctor.secondname.in_(words),
                    Doctor.lastname.in_(words),
                    aPatient.firstname.in_(words),
                    aPatient.secondname.in_(words),
                    aPatient.lastname.in_(words),
                    Turn.when.like(f'%{q}%'),
                    )
                )
            .group_by(Turn)
            .paginate(per_page=20)
            )


    else:
        paginated=(query.group_by(Turn).paginate(per_page=20))

    rows = [
                (
                    t.id,
                    t.when,
                    d.fullname if d else "No asignado",
                    p.fullname if p else "No asignado",
                    t.duration
                )
            for t,d,p in paginated.items
        ]
    headers = ('Fecha y Hora','Medico','Paciente','Duracion (min)' )
    return render_template('list.html',rows=rows,paginated=paginated,headers=headers,title=title)


@bp.route('/available')
def available():
    title='Listado de turnos disponibles'

    query=(db.session
            .query(Turn,Doctor)
            .filter(
                Turn.doctor_id == Doctor.id,
                Turn.when >= datetime.today(),
                Turn.is_available == True,
                )
            .group_by(Turn)
            )
    if g.profile == 'doctor':
        query=query.filter(Doctor.id==session['userid'])


    """ user submit a search, do a filtered list"""
    q=request.args.get('q','',str).strip()

    if q and re.match('^[\w\s,:.-]{1,30}$',q):
        words=q.split(', ')
        paginated=(query.filter(
                or_(
                    Doctor.firstname.in_(words),
                    Doctor.secondname.in_(words),
                    Doctor.lastname.in_(words),
                    Turn.when.like(f'%{q}%'),
                    )
                )
            .group_by(Turn)
            .paginate(per_page=20)
            )
    else:
        paginated=(query.group_by(Turn).paginate(per_page=20))

    rows = [
                (
                    t.id,
                    t.when,
                    d.fullname if d else "No asignado",
                    t.duration
                )
            for t,d in paginated.items
        ]
    headers = ('Fecha y Hora','Medico','Duracion' )
    return render_template('list.html',rows=rows,paginated=paginated,headers=headers,title=title)



@bp.route('/missed')
def missed():
    title='Listado de turnos perdidos'

    # FIXED: SQLAlchemy can not resolve inherance at same time on query
    aPatient=aliased(User)

    query=(db.session
            .query(Turn,Doctor,aPatient)
            .filter(
                Doctor.id == Turn.doctor_id,
                aPatient.id == Turn.patient_id,
                Turn.when <= datetime.today(),
                Turn.is_missed,
                )
            .group_by(Turn)
            .order_by(Turn.when.desc())
            )

    if g.profile in ['patient','doctor'] :
        #g.writable = False
        query=(query
            .filter(
                or_(
                    Turn.patient_id == session['userid'],
                    Turn.doctor_id == session['userid'],
                    )
                )
            .group_by(Turn)
            )


    """ user submit a search, do a filtered list"""
    q=request.args.get('q','',str).strip()

    if q and re.match('^[\w\s,:.-]{1,30}$',q):
        if q.isdigit():
            dni=int(q)
            paginated=(query
                .filter(
                    Doctor.dni.like(f'%{dni}%'),
                    )
                .group_by(Turn)
                .paginate(per_page=20)
                )

        else:
            words=q.split(', ')
            paginated=(query.filter(
                    or_(
                        Doctor.firstname.in_(words),
                        Doctor.secondname.in_(words),
                        Doctor.lastname.in_(words),
                        aPatient.firstname.in_(words),
                        aPatient.secondname.in_(words),
                        aPatient.lastname.in_(words),
                        Turn.when.like(f'%{q}%'),
                        )
                    )
                .group_by(Turn)
                .paginate(per_page=20)
                )


    else:
        paginated=(query.group_by(Turn).paginate(per_page=20))

    rows = [
                (
                    t.id,
                    t.when,
                    d.fullname,
                    p.fullname,
                    t.duration
                )
            for t,d,p in paginated.items
        ]
    headers = ('Fecha y Hora','Medico','Paciente','Duracion (min)' )
    return render_template('list.html',rows=rows,paginated=paginated,headers=headers,title=title)

@bp.route('/waiting')
def waiting():
    title='Listado de turnos en espera'

    # FIXED: SQLAlchemy doesnt resolve inherance at same time on query
    aPatient=aliased(User)

    query=(db.session
            .query(Turn,Doctor,aPatient)
            .filter(
                Doctor.id == Turn.doctor_id,
                aPatient.id == Turn.patient_id,
                Turn.when >= datetime.today(),
                Turn.is_available == False,
                Turn.is_missed == False,
                )
            .group_by(Turn)
            .order_by(Turn.when.asc())
            )

    if g.profile in ['patient','doctor'] :
        query=(query
            .filter(
                or_(
                    Turn.patient_id == session['userid'],
                    Turn.doctor_id == session['userid'],
                    )
                )
            .group_by(Turn)
            )

    """ user submit a search, do a filtered list"""
    q=request.args.get('q','',str).strip()

    if q and re.match('^[\w\s,:.-]{1,30}$',q):
        if q.isdigit():
            dni=int(q)
            paginated=(query
                .filter(
                    Doctor.dni.like(f'%{dni}%'),
                    )
                .group_by(Turn)
                .paginate(per_page=20)
                )

        else:
            words=q.split(', ')
            paginated=(query.filter(
                    or_(
                        Doctor.firstname.in_(words),
                        Doctor.secondname.in_(words),
                        Doctor.lastname.in_(words),
                        aPatient.firstname.in_(words),
                        aPatient.secondname.in_(words),
                        aPatient.lastname.in_(words),
                        Turn.when.like(f'%{q}%'),
                        )
                    )
                .group_by(Turn)
                .paginate(per_page=20)
                )


    else:
        paginated=(query.group_by(Turn).paginate(per_page=20))

    rows = [
                (
                    t.id,
                    t.when,
                    d.fullname,
                    p.fullname,
                    t.duration
                )
            for t,d,p in paginated.items
        ]
    headers = ('Fecha y Hora','Medico','Paciente','Duracion (min)' )
    return render_template('list.html',rows=rows,paginated=paginated,headers=headers,title=title)

"""
   NOTE: Patients shouldn't be allowed to access this endpoint
"""
@bp.route('/create',methods=('GET','POST'))
def create():
    form=TurnFormCreate(request.form)

    if g.profile == 'doctor':
        del form.doctor


    if form.validate_on_submit():
        if g.profile == 'doctor':
            doctor_id=session['userid']
        else:
            doctor_id=request.form.get('doctor',0,int)

        when=datetime.strptime(request.form.get('when',''),'%Y-%m-%dT%H:%M')

        query=(db.session
            .query(Turn)
            .filter(
                Turn.doctor_id == doctor_id,
                Turn.when == when,
                )
            .first()
            )
        if query:
            flash("El turno ya esta registrado : %s"%(when,),'danger')
            return render_template('form.html',title='Crear turno',form=form)

        # BUG: the turn appear on query but not in DB
        # better place the checking before Turn()
        obj=Turn()
        form.populate_obj(obj)
        obj.doctor_id=doctor_id

        try:
            db.session.add(obj)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(str(ex))
            flash(str(ex),'danger')
            return render_template('form.html',title='Crear turno',form=form)

        # set next date
        next_date=obj.when + timedelta(minutes=int(obj.duration))
        form.when.raw_data=[next_date.strftime('%Y-%m-%dT%H:%M')]

        flash(f'Se dio de alta un turno : {obj.when}','success')

    return render_template('form.html',title='Crear turno',form=form)


"""
    This function (endpoint) asign a turn
"""
@bp.route('/request',methods=('GET','POST') )
def request_turn():
    title='Solicitar Turno'
    form=TurnFormRequest(request.form)
    if g.profile == 'patient':
        form.patient_id.data = session['userid']

    if request.method == 'POST':
        if g.profile == 'patient'and form.patient_id.data != session['userid']:
            return abort(403)

        if form.validate_on_submit():
            obj=Turn.query.get(request.form.get('turn',0,int) )
            if not obj:
                flash('No se encontro el turno','danger')
                return render_template('turn/request.html',title=title,form=form)

            obj.is_available=0
            form.populate_obj(obj)

            try:
                db.session.commit()
            except Exception as ex:
                db.session.rollback()
                current_app.logger.error(str(ex))
                flash(str(ex),'danger')
                return render_template('turn/request.html',title=title,form=form)

            flash('Se asigno un turno a un paciente','success')

        else:
            current_app.logger.error(str(form.errors))
            flash('Paciente no encontrado','danger')
            return render_template('turn/request.html',title=title,form=form)


    return render_template('turn/request.html',title='Solicitar Turno',form=form)
