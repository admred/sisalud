# -*- coding: utf-8 -*-
from flask import redirect,render_template,request,url_for,abort,session,abort,Blueprint,flash,current_app
from webapp.models import SocialSecure,db
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from webapp.forms import SocialSecureForm
from sqlalchemy import select,or_
import re

bp=Blueprint('socialsecure',__name__)

@bp.route('/update/<int:_id>',methods=('get','post'))
@bp.route('/create',methods=('get','post'))
def edit(_id=None):
    if _id:
        obj=SocialSecure.query.get(_id)
        title='Actualizar'
    else:
        title='Crear'
        obj=SocialSecure()

    form=SocialSecureForm(request.form,obj=obj)
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
    obj=SocialSecure.query.get(_id)
    form=SocialSecureForm(obj=obj)
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
        obj=SocialSecure.query.get(idx)
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
                SocialSecure.query
                .filter(
                    or_(
                        SocialSecure.rnos.like(match),
                        SocialSecure.short.like(match),
                        SocialSecure.name.like(match),
                        ))
                .paginate(per_page=10)
                )
    else:
        paginated=SocialSecure.query.paginate(per_page=10)

    rows=[ (
        x.id,
        x.rnos or "-",
        x.short or "-",
        x.name,
        ) for x in paginated.items ]

    headers=('RNOS','Siglas','Nombre')
    return render_template('list.html',rows=rows,paginated=paginated,headers=headers,title=title)


