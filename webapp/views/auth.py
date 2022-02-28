# -*- coding: utf-8 -*-
from flask import *
from werkzeug.security import generate_password_hash,check_password_hash
from webapp.models import  *
from webapp.forms import *
from webapp.models import *

bp=Blueprint('auth',__name__)

@bp.route('/login',methods=('GET','POST'))
def login():
    #session.pop('_flashes',None)

    if 'userid' in session:
        return redirect('/user/home')

    form=LoginForm(request.form)


    if form.validate_on_submit():
        user=User.query.filter_by(username=request.form['username']).first()
        if not user:
            flash('Usuario no valido','danger')
            return redirect(url_for('.login'))

        if not check_password_hash(user.password,request.form['password']) :
            flash(u'Contraseña no valida','danger')
            return redirect(url_for('.login'))

        session['userid']=user.id

        flash('Binevenido ! %s'%(user.username),'success')

        return redirect('/user/home')

    return render_template('auth/login.html',form=form,title='Login')

@bp.route('/logout')
def logout():
    session.pop('userid',None)
    session.clear()
    flash(u'Sesión terminada.','success')
    return redirect('/auth/login')


