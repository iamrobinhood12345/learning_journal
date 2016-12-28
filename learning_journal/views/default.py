from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel

import os

from pyramid.httpexceptions import HTTPFound

HERE = os.path.dirname(__file__)


@view_config(route_name='list', renderer='../templates/list.jinja2')
def index_page(request):
    try:
        query = request.dbsession.query(MyModel)
        entries = query.all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {"ENTRIES": entries}


@view_config(route_name='detail', renderer='../templates/post_template.jinja2')
def post_page(request):
    the_id = request.matchdict["id"]
    try:
        entry = request.dbsession.query(MyModel).get(the_id)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {"entry": entry}


@view_config(route_name='about', renderer='../templates/about_template.jinja2')
def about_page(request):
    return {}


@view_config(route_name='update', renderer='../templates/update_template.jinja2')
def update_page(request):
    the_id = request.matchdict["id"]
    try:
        entry = request.dbsession.query(MyModel).get(the_id)
        if request.method == "POST":
            entry.title = request.POST["title"]
            entry.title1 = request.POST["title1"]
            entry.creation_date = request.POST["creation_date"]
            entry.body = request.POST["body"]
            request.dbsession.flush()
            # return HTTPFound(request.route_url("list"))

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {"entry": entry}


@view_config(route_name='create', renderer='../templates/new_post_template.jinja2')
def new_post_page(request):
    if request.method == "POST":
        new_title = request.POST["title"]
        new_title1 = request.POST["title1"]
        new_creation_date = request.POST["creation_date"]
        new_body = request.POST["body"]

        model = MyModel(title=new_title, title1=new_title1, creation_date=new_creation_date, body=new_body)
        request.dbsession.add(model)

        request.dbsession.flush()

        # return HTTPFound(request.route_url("list"))
    return {}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
