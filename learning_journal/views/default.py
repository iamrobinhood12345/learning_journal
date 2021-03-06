from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel
from ..security import check_credentials
from pyramid.security import remember, forget

from pyramid.httpexceptions import HTTPFound

import datetime


@view_config(route_name='list', renderer='../templates/list.jinja2')
def index_page(request):
    """Handles rendering for client request for the index page."""
    try:
        query = request.dbsession.query(MyModel)
        entries = query.all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {"ENTRIES": entries}


@view_config(route_name='detail', renderer='../templates/post_template.jinja2')
def entry_page(request):
    """Handles rendering for client request for post pages."""
    the_id = request.matchdict["id"]
    try:
        entry = request.dbsession.query(MyModel).get(the_id)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {"entry": entry}


@view_config(route_name='about', renderer='../templates/about_template.jinja2')
def about_page(request):
    """Handles rendering for client request for about page."""
    return {}


@view_config(route_name='update', renderer='../templates/update_template.jinja2', permission='change')
def update_page(request):
    """Handles rendering for client request for update pages."""
    the_id = request.matchdict["id"]
    try:
        entry = request.dbsession.query(MyModel).get(the_id)
        if request.method == "POST":
            entry.title = request.POST["title"]
            entry.title1 = request.POST["title1"]
            entry.creation_date = datetime.date.today()
            entry.body = request.POST["body"]

            request.dbsession.flush()
            return HTTPFound(request.route_url("list"))

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {"entry": entry}


@view_config(route_name='create', renderer='../templates/new_post_template.jinja2', permission='change')
def new_post_page(request):
    """Handles rendering for client request for new post page."""
    if request.method == "POST":
        new_title = request.POST["title"]
        new_title1 = request.POST["title1"]
        new_creation_date = datetime.date.today()
        new_body = request.POST["body"]

        model = MyModel(title=new_title, title1=new_title1, creation_date=new_creation_date, body=new_body)
        request.dbsession.add(model)

        request.dbsession.flush()
        return HTTPFound(request.route_url("list"))

    return {}


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login_view(request):
    """Authenticate the incoming user."""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(username, password):
            auth_head = remember(request, username)
            return HTTPFound(
                request.route_url("list"),
                headers=auth_head
            )
    return {}


@view_config(route_name='logout')
def logout_view(request):
    """Remove authentication from the user."""
    auth_head = forget(request)
    return HTTPFound(request.route_url("list"), headers=auth_head)


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
