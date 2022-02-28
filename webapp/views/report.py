# -*- coding: utf-8 -*-
from flask import redirect,render_template,request,url_for,abort,session,abort,Blueprint,flash,current_app,g
from webapp.models import *
from sqlalchemy import func

import pandas as pd
import json
import plotly
import plotly.express as px

bp=Blueprint('report',__name__)

"""
    General Statistics
"""
@bp.get('/turn-by-speciality')
def turn_by_speciality():
    title='Turnos por especialidad'
    details=None
    graphJSON=None

    query=(db.session
        .query(Turn,Doctor,Speciality,func.count(Speciality.id))
        .filter(
            Turn.doctor_id==Doctor.id,
            Doctor.speciality_id==Speciality.id,
            )
        .group_by(Speciality)
        )
    total=Turn.query.count()


    if not query or query.count() == 0:
        flash('Error no se puede obtener datos','danger')
    else:
        labels=[]
        values=[]
        for t,d,s,n in query:
            labels.append(s.name)
            values.append(n/total*100)

        assert labels != []
        assert values !=  []

        df = pd.DataFrame({
            'labels':labels,
            'values':values,
            })
        fig = px.pie(df, values='values' , names = 'labels', title=title ) # Figure
        graphJSON = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)  # encoding to JSON
    return render_template('report/report.html',title=title,graphJSON=graphJSON,details=details)


@bp.get('/turn-by-month')
def turn_by_month():
    title='Turnos por mes'
    details=None
    graphJSON=None

    query=(db.session
        .query(
            func.strftime("%Y-%m",Turn.when),
            func.count(Turn.id),
            )
        .group_by(func.strftime("%Y-%m",Turn.when))
        .order_by(func.strftime("%Y-%m",Turn.when))
        .limit(12)
        )

    if not query or query.count() == 0:
        flash('Error no se puede obtener datos','danger')
    else:
        months=[]
        counts=[]
        for m,c in query:
            months.append(m)
            counts.append(c)

        df = pd.DataFrame({
            'Tiempo':months,
            'Cantidad':counts,
            })

        fig = px.bar(df, x='Tiempo' , y='Cantidad' ,title=title ) # Figure
        graphJSON = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)  # encoding to JSON
    return render_template('report/report.html',title=title,graphJSON=graphJSON,details=details)

"""
    Doctor statistics
"""

@bp.get('/doctor-turn-by-month')
def doctor_turn_by_month():
    title='Turnos por mes'
    details=None
    graphJSON=None

    query=(db.session
        .query(
            Turn.doctor_id==session['userid'],
            func.strftime("%Y-%m",Turn.when),
            func.count(Turn.id),
            )
        .group_by(func.strftime("%Y-%m",Turn.when))
        .order_by(func.strftime("%Y-%m",Turn.when))
        .limit(12)
        )

    if not query or query.count() == 0:
        flash('Error no se puede obtener datos','danger')
    else:
        months=[]
        counts=[]
        for _,m,c in query:
            months.append(m)
            counts.append(c)

        df = pd.DataFrame({
            'Tiempo':months,
            'Cantidad':counts,
            })

        fig = px.bar(df, x='Tiempo' , y='Cantidad' ,title=title ) # Figure
        graphJSON = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)  # encoding to JSON
    return render_template('report/report.html',title=title,graphJSON=graphJSON,details=details)




