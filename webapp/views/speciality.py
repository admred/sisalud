# -*- coding: utf-8 -*-
from flask import redirect,render_template,request,url_for,abort,session,abort,Blueprint,flash,current_app
from webapp.models import Speciality,db
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from webapp.forms import SpecialityForm
from sqlalchemy import select,or_
import re

bp=Blueprint('speciality',__name__)

@bp.route('/update/<int:_id>',methods=('get','post'))
@bp.route('/create',methods=('get','post'))
def edit(_id=None):
    if _id:
        obj=Speciality.query.get(_id)
        title='Actualizar'
    else:
        title='Crear'
        obj=Speciality()

    form=SpecialityForm(request.form,obj=obj)
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

    return render_template('form.html',form=form,title=title)

@bp.get('/detail/<int:_id>')
def detail(_id):
    title='Detalle'
    obj=Speciality.query.get(_id)
    form=SpecialityForm(obj=obj)
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
        obj=Speciality.query.get(idx)
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
    q=request.args.get('q','',str)
    if q and re.match('[\w\d ]{1,20}',q):
        match=f"%{q}%"
        paginated=(
                Speciality.query
                .filter(
                    or_(
                        Speciality.name.like(match),
                        Speciality.description.like(match)
                        ))
                .paginate(per_page=10)
                )
    else:
        paginated=Speciality.query.paginate(per_page=10)

    rows=[ (x.id,x.name,x.description) for x in paginated.items ]
    headers=('Nombre','Descripción')
    return render_template('list.html',rows=rows,paginated=paginated,headers=headers,title=title)


