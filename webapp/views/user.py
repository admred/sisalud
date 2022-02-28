# -*- coding: utf-8 -*-
from flask import redirect,render_template,request,url_for,abort,session,abort,Blueprint,flash,current_app,Markup,g
from webapp.models import User,Profile,db
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from wtforms import *
from wtforms.widgets import *
from wtforms.widgets.html5 import *
from wtforms.ext.sqlalchemy.orm import model_form
from webapp.models import *
from webapp.forms import  *
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from sqlalchemy.exc import  IntegrityError

bp=Blueprint('user',__name__)



@bp.route('/create',methods=['GET','POST'])
def create():
    title='Crear usuario'
    form=UserForm(request.form)

    # this request came from not logged user or profile is patient
    if 'userid' not in session or g.profile == 'patient':
        title='Registrar paciente'
        #  unused fields
        del form.speciality
        del form.license_
        del form.profile



    if form.validate_on_submit():


        if request.form['password'] != request.form['password2'] :
            flash('Las claves deben coincidir','danger')
            return render_template('form.html',form=form,title=title)


        if 'userid' not in session:
            obj=Patient()
            obj.profile_id=3 # patient
        else:
            # FIXED: map the correct class, WTForms act weird with User
            Cls=(None,Admin,Doctor,Patient,Receptionist)[request.form.get('profile',0,int) ]
            obj=Cls()

        # FIXED: don't forget hash the password or will be unable to get login
        form.populate_obj(obj)
        obj.password=generate_password_hash(request.form['password'])

        try:
            db.session.add(obj)
            db.session.commit()


        except IntegrityError as ex:
            db.session.rollback()
            current_app.logger.error(str(ex))
            flash('DNI o usuario ya existe','danger')
            return render_template('form.html',form=form,title=title)

        flash('Alta exitosa','success')
        return redirect('/')

    """ GET """
    return render_template('form.html',form=form,title=title)


@bp.route('/list')
def list():
    title='Listado de usuarios'
    if g.profile == 'patient':
        return redirect('/user/home')

    aPatient=aliased(Patient)
    query=(db.session
        .query(User,Profile)
        .filter(
            User.profile_id == Profile.id,
            )
        .group_by(User)
        .order_by(User.lastname)
        )



    q=request.args.get('q')
    if q:
        q=q.strip()
        q=q.split(',. ')

        result=(query.filter(
            or_(
                User.username.in_(q),
                User.firstname.in_(q),
                User.secondname.in_(q),
                User.lastname.in_(q),
                User.dni.in_(q),
            ))
            .group_by(User)
            .order_by(User.lastname)
            .paginate(per_page=20)

        )

    else:
        result=(query
            .group_by(User)
            .order_by(User.lastname)
            .paginate(per_page=20)
            )



    rows=[ (u.id,u.username,u.dni,u.fullname,p.name) for u,p in result.items ]
    headers=('Usuario','DNI','Nombre','Tipo')
    return render_template('list.html',rows=rows,paginated=result,headers=headers,title=title)

@bp.route('/patients')
def patients():


    title='Listado de pacientes'
    query=(db.session
        .query(User)
        .filter(
            User.profile_id==3,
        )
        .group_by(User)
        )



    q=request.args.get('q')
    if q:
        q=q.strip()
        q=q.split(',. ')

        result=(query.filter(
            or_(
                User.username.in_(q),
                User.firstname.in_(q),
                User.secondname.in_(q),
                User.lastname.in_(q),
                User.dni.in_(q),
            ))
            .group_by(User)
            .order_by(User.lastname)
            .paginate(per_page=20)

        )

    else:
        result=(query
            .group_by(User)
            .order_by(User.lastname)
            .paginate(per_page=20)
            )



    rows=[ (u.id,u.fullname,u.dni) for u in result.items ]
    headers=('Paciente','DNI')
    return render_template('list.html',rows=rows,paginated=result,headers=headers,title=title)


@bp.route('/update/<int:idx>',methods=('GET','POST'))
def update(idx):
    title='Modificar usuario'


    obj=User.query.get(idx)
    if not obj:
        flash('Usuario no existe','danger')
        return redirect(url_for('.list'))


    form=UserForm(request.form,obj=obj)

    if g.profile in ['patient','doctor']:
        if idx != session['userid']:
            return abort(403) # forbiden

        # remove unused fields
        g.writable = True # allow write with personal account
        form.profile.render_kw={'readonly':'','disabled':''}
        form.dni.render_kw={'readonly':'','disabled':''}
        form.username.render_kw={'readonly':'','disabled':''}

    if g.profile == "patient":
        del form.speciality
        del form.license_
    elif g.profile == 'doctor':
        del form.socialsecure

    if form.validate_on_submit():
        if request.form['password'] != request.form['password2'] :
            flash('Las claves deben coincidir','danger')
            return render_template('form.html',form=form,title=title)

        old_password=obj.password
        form.populate_obj(obj)



        if old_password != request.form['password']:
            obj.password=generate_password_hash(request.form['password'])
        try:
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            current_app.logger.error(str(ex))
            flash( str(ex)  ,'danger')
            return render_template('form.html',form=form,title=title)

        flash('Se actualizo un registro con exito','success')
        return redirect(url_for('.list'))

    return render_template('form.html',form=form,title=title)

@bp.route('/detail/<int:idx>',methods=('GET','POST'))
def detail(idx):
    title="Detalle de usuario"
    if request.method == 'POST':
        return redirect(url_for('.list'))
    obj=User.query.get(idx)
    if not obj:
        current_app.logger.error(str(ex))
        flash(str(ex),'danger')
        return redirect(url_for('.list'))

    # FIXED: map the correct Object, WTForms act weird with User
    obj=[None,Admin,Doctor,Patient,Receptionist][obj.profile_id].query.get(idx)

    form=UserForm(obj=obj)

    # delete unused fields
    if obj.profile_id == 3 :
        del form.speciality
        del form.license_
    elif obj.profile_id == 2:
        del form.socialsecure


    return render_template('form.html',form=form,title=title)


@bp.post('/delete')
@bp.route('/delete/<int:idx>',methods=('GET','POST'))
def delete(idx=0):

    title="Eliminar usuario"
    if request.method == 'POST':
        ids=[]
        if idx != 0 :
            ids.append(idx)
        elif  request.form.get('marca',None):
            ids=request.form.getlist('marca')
        else:
            flash('Debe marcar al menos un item','warning')
            return redirect(url_for('.list'))

        for idx in ids :
            obj=User.query.get(idx)
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

    """ GET """
    obj=User.query.get(idx)
    if not obj:
        flash('El registro no exite','danger')
        return redirect(url_for('.list'))

    form=UserForm(request.form,obj=obj)

    return render_template('form.html',form=form,title=title)

@bp.route('/home')
def home():
    title='Bienvenido!'
    return render_template('user/home.html',title=title)

