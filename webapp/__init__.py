# -*- coding: utf-8 -*-
import os
import locale
from flask import Flask,session,g,redirect,url_for,request,abort
from flask_bootstrap  import Bootstrap4 as Bootstrap
from webapp.models import *
from webapp.forms import ScheduleForm

# old app factory ported from python 2.7 to python 3.6
def create_app(config=None):
    app=Flask(__name__.split('.')[0])
    app.config.from_pyfile('config.py')
    app.config.from_object(config)

    Bootstrap(app)
    from .models import db,init_db,User
    app.cli.add_command(init_db)

    db.init_app(app)

    # access control
    @app.before_request
    def before_request_func():

        if 'static' in request.path or request.endpoint in (None,'site.home') :
            return # OK, skip it

        g.writable = False
        g.readable = False
        g.deletion =  False
        g.current_user = None
        g.profile = None
        uid=None
        result=None

        # get the user and profile, if it we had a session
        if 'userid' in session:

            uid=session['userid']

            result=(db.session
                .query(User,Profile,Access)
                .filter(
                    User.profile_id == Profile.id,
                    Access.profile_id == Profile.id,
                    User.id == uid,
                    )
                .group_by(User)
                .first()
                )


            if result != None:
                g.current_user = result[0]
                g.profile = result[1].name


        endpoint=request.endpoint  # ex 'turn.update'
        obj,action=endpoint.split('.')

        # control access
        if uid:
            # endpoints for forms and semipublic ones
            if endpoint in (
                'ajax.doctor_by_speciality',
                'ajax.turn_by_doctor',
                'ajax.speciality',
                'ajax.turn_by_id',
                'ajax.patient_by_id',
                'report.doctor_turn_by_month',
                'ajax.patient_by_dni'):

                g.readable=True
                return # OK,

            #  find this endpoint in DB

            for access in g.current_user.profile.accesses:

                if obj == access.endpoint :

                    if access.is_writable:
                        g.writable = True

                        return #OK
                    else:
                        g.readable = True
                        return #OK


        # public endpoints
        if endpoint in (
            'auth.login',
            'auth.logout',
            'speciality.list',
            'speciality.detail',
            'socialsecure.list',
            'socialsecure.detail',
            'report.turn_by_speciality',
            'report.doctor_by_speciality',
            'report.turn_by_month',
            'schedule.list',
            'schedule.detail',
            ):
            g.readable=True
            return # OK

        elif endpoint == 'user.create' and 'userid' not in session:
            # FIXED: allow submit a register with no session
            g.writable = True

            return # OK

        return abort(403) # 403 forbiden

    # end before_request()

    # pattern matching
    locale.setlocale(locale.LC_ALL,'es_AR')

    # FIXED: error, no instance folder found
    try:
        os.makedirs(app.instance_path)
    except:
        pass

    from webapp.views import user,speciality,auth,turn,appointment,report,socialsecure,schedule,site
    from webapp import ajax

    app.register_blueprint(ajax.bp,url_prefix='/ajax')
    app.register_blueprint(auth.bp,url_prefix='/auth')
    app.register_blueprint(user.bp,url_prefix='/user')
    app.register_blueprint(speciality.bp,url_prefix='/speciality')
    app.register_blueprint(turn.bp,url_prefix='/turn')
    app.register_blueprint(appointment.bp,url_prefix='/appointment')
    app.register_blueprint(report.bp,url_prefix='/report')
    app.register_blueprint(socialsecure.bp,url_prefix='/socialsecure')
    app.register_blueprint(schedule.bp,url_prefix='/schedule')
    app.register_blueprint(site.bp)

    return app