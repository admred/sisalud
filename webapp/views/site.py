# -*- coding: utf-8 -*-
from flask import redirect,session,Blueprint

bp=Blueprint('site',__name__)


@bp.route('/')
def home():
    if 'userid' in session:
        return redirect('/user/home')

    return redirect('/auth/login')


