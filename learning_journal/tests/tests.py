"""A short testing suite for the expense tracker."""


import pytest
import transaction

from pyramid import testing

from learning_journal.models import MyModel, get_tm_session
from learning_journal.models.meta import Base
# from learning_journal.scripts.initializedb import ENTRIES


TEST_ENTRIES = [
    {"title": "Learning Journal - Day 12", "title1": "Slowly Getting Better", "creation_date": "Dec 20, 2016", "body": "<p>Today was a good day. I started off asking questions right away and was more attentive than I am most days. This felt really good. I'm going to try to ask as many questions as I can. I'm also going to volunteer for code review tomorrow. Today we also formed our groups for project week. Looks like Pysearch is happening after all! I have a good group going, with Marc, Casey, and Sera. This should be a lot of fun. My thoughts are that we should start small, and get a working implementation of a search engine going quickly, and design it in such a way that we can add features easily. Will said something about a simple search engine tutorial on Udacity. I will definitely ask him about this. The number one take away today would be that I should participate as much as I can, even if I don't feel like it, especially in the mornings. Another thing I realized is that a lot of computer science is actually getting good with getting a bunch of different things to work together -- different files, file systems, frameworks, functions that must speak to each other, having an account with the service you are using, and really taking all of these sort of things one step at a time. Overall, I can't wait to start working on Pysearch!</p>"},
    {"title": "Learning Journal - Day 11", "title1": "Pitches and Tools", "creation_date": "Dec 19, 2016", "body": "<p>Today I learned a good deal about my classmates. Each of us took turns pitching ideas for project week projects. I was very impressed with the creativity of my classmates. Several of their ideas seem like very good ones. I wish I could help out with all of them. Alas, decisions must be made, and we will eventually come to each work on one of a handful of projects. Such is life. We must choose decisively, and live with our choices for the rest of our days.</p><p>Avery and Patrick had awesome presentations. I learned about Itertools from Patrick, and can't wait for the chance to practice. Avery presented on an enhancement for Visual Studio that allows you to see documentation for functions as you are writing them. How cool is that!</p>"},
    {"title": "DNA Transcription", "title1": "ATGCATGCATGCATGCATGCATGC", "creation_date": "Dec 20, 2016", "body": "I learned some stuff about some other stuff."},
    {"title": "Itertools", "title1": "New stuff learned", "creation_date": "Dec 20, 2016", "body": "I learned some stuff about some other stuff."},
]


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.
    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.
    This configuration will persist for the entire duration of your PyTest run.
    """
    settings = {
        'sqlalchemy.url': 'sqlite:///:memory:'}  # points to an in-memory database.
    config = testing.setUp(settings=settings)
    config.include('learning_journal.models')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture()
def db_session(configuration, request):
    """Create a session for interacting with the test database.
    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Instantiate a fake HTTP Request, complete with a database session.
    This is a function-level fixture, so every new request will have a
    new database session.
    """
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_models(dummy_request):
    """Add a bunch of model instances to the database.
    Every test that includes this fixture will add new models
     from the ENTRIES list.
    """
    for each in TEST_ENTRIES:
        model = MyModel(title=each["title"], title1=each["title1"], creation_date=each["creation_date"], body=each["body"])
        dummy_request.dbsession.add(model)


# ======== UNIT TESTS ==========

def test_new_models_are_added(db_session, add_models):
    """New entries get added to the database."""
    query = db_session.query(MyModel).all()
    assert len(query) == len(TEST_ENTRIES)


def test_index_page_returns_empty_when_empty(dummy_request):
    """Test that the list view returns no objects in the expenses iterable."""
    from learning_journal.views.default import index_page
    result = index_page(dummy_request)
    assert len(result["ENTRIES"]) == 0


def test_index_page_returns_objects_when_exist(dummy_request, add_models):
    """Test that the list view does return objects when the DB is populated."""
    from learning_journal.views.default import index_page
    result = index_page(dummy_request)
    assert len(result["ENTRIES"]) == len(TEST_ENTRIES)

# ======== FUNCTIONAL TESTS ===========


@pytest.fixture
def testapp():
    """Create an instance of webtests TestApp for testing routes.
    With the alchemy scaffold we need to add to our test application the
    setting for a database to be used for the models.
    We have to then set up the database by starting a database session.
    Finally we have to create all of the necessary tables that our app
    normally uses to function.
    The scope of the fixture is function-level, so every test will get a new
    test application.
    """
    from webtest import TestApp
    from learning_journal import main

    app = main({}, **{"sqlalchemy.url": 'sqlite:///:memory:'})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    return testapp


@pytest.fixture
def fill_the_db(testapp):
    """Fill the database with some model instances.
    Start a database session with the transaction manager and add all of the
    entries. This will be done anew for every test.
    """
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)

        for each in TEST_ENTRIES:
            model = MyModel(title=each["title"], title1=each["title1"], creation_date=each["creation_date"], body=each["body"])
            dbsession.add(model)


def test_index_page_renders(testapp):
    """The home page has an h1 in the html."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("h1")) == 1


def test_home_route_with_data_has_filled_table(testapp, fill_the_db):
    """When there's data in the database, the home page has some rows."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("h2")) == len(TEST_ENTRIES)


# import pytest
# import transaction

# from pyramid import testing

# from learning_journal.models import (
#     MyModel,
#     get_tm_session,
# )
# from learning_journal.models.meta import Base


# @pytest.fixture(scope="session")
# def configuration(request):
#     """Set up a Configurator instance.

#     This Configurator instance sets up a pointer to the location of the
#         database.
#     It also includes the models from your app's model package.
#     Finally it tears everything down, including the in-memory SQLite database.

#     This configuration will persist for the entire duration of your PyTest run.
#     """
#     config = testing.setUp(settings={
#         'sqlalchemy.url': 'sqlite:///:memory:'
#     })
#     config.include("..models")

#     def teardown():
#         testing.tearDown()

#     request.addfinalizer(teardown)
#     return config


# @pytest.fixture(scope="function")
# def db_session(configuration, request):
#     """Create a session for interacting with the test database.

#     This uses the dbsession_factory on the configurator instance to create a
#     new database session. It binds that session to the available engine
#     and returns a new session for every call of the dummy_request object.
#     """
#     SessionFactory = configuration.registry["dbsession_factory"]
#     session = SessionFactory()
#     engine = session.bind
#     Base.metadata.create_all(engine)

#     def teardown():
#         session.transaction.rollback()

#     request.addfinalizer(teardown)
#     return session

# import unittest
# import transaction
# import pytest

# from pyramid import testing


# @pytest.fixture
# def req():
#     the_request = testing.DummyRequest()
#     return the_request


# def test_home_page_renders_file_data(req):
#     """My home page view returns some data."""
#     from .views import index_page
#     response = index_page(req)
#     assert "<p>Today I learned a good deal about my classmates. Each of us took turns pitching ideas for project week projects. I was very impressed with the creativity of my classmates. Several of their ideas seem like very good ones. I wish I could help out with all of them. Alas, decisions must be made, and we will eventually come to each work on one of a handful of projects. Such is life. We must choose decisively, and live with our choices for the rest of our days.</p><p>Avery and Patrick had awesome presentations. I learned about Itertools from Patrick, and can't wait for the chance to practice. Avery presented on an enhancement for Visual Studio that allows you to see documentation for functions as you are writing them. How cool is that!</p>" in str(response)


# def dummy_request(dbsession):
#     return testing.DummyRequest(dbsession=dbsession)


# class BaseTest(unittest.TestCase):
#     def setUp(self):
#         self.config = testing.setUp(settings={
#             'sqlalchemy.url': 'sqlite:///:memory:'
#         })
#         self.config.include('.models')
#         settings = self.config.get_settings()

#         from .models import (
#             get_engine,
#             get_session_factory,
#             get_tm_session,
#             )

#         self.engine = get_engine(settings)
#         session_factory = get_session_factory(self.engine)

#         self.session = get_tm_session(session_factory, transaction.manager)

#     def init_database(self):
#         from .models.meta import Base
#         Base.metadata.create_all(self.engine)

#     def tearDown(self):
#         from .models.meta import Base

#         testing.tearDown()
#         transaction.abort()
#         Base.metadata.drop_all(self.engine)


# class TestMyViewSuccessCondition(BaseTest):

#     def setUp(self):
#         super(TestMyViewSuccessCondition, self).setUp()
#         self.init_database()

#         from .models import MyModel

#         model = MyModel(name='one', value=55)
#         self.session.add(model)

#     def test_passing_view(self):
#         from .views.default import my_view
#         info = my_view(dummy_request(self.session))
#         self.assertEqual(info['one'].name, 'one')
#         self.assertEqual(info['project'], 'learning_journal')


# class TestMyViewFailureCondition(BaseTest):

#     def test_failing_view(self):
#         from .views.default import my_view
#         info = my_view(dummy_request(self.session))
#         self.assertEqual(info.status_int, 500)

# import pytest
# from pyramid import testing


# @pytest.fixture
# def req():
#     the_request = testing.DummyRequest()
#     return the_request


# def test_home_page_renders_file_data(req):
#     """My home page view returns some data."""
#     from .views import index_page
#     response = index_page(req)
#     some_html = "<p>Today I"
#     assert some_html in str(response)


# def test_post_view():
#     from .views import post_page
#     req.matchdict = {'id': '11'}
#     info = post_page(req)
#     assert "title" in str(info)


# def test_update_view():
#     from .views import update_page
#     req.matchdict = {'id': '11'}
#     info = update_page(req)
#     assert "title" in str(info)


# def test_new_post_view():
#     from .views import new_post_page
#     info = new_post_page(req)
#     assert "title" in str(info)


# def test_about_view():
#     from .views import about_page
#     info = about_page(req)
#     assert "title" in str(info)


# @pytest.fixture()
# def testapp():
#     """Create an instance of our app for testing."""
#     from learning_journal_basic import main
#     app = main({})
#     from webtest import TestApp
#     return TestApp(app)


# def test_layout_list(testapp):
#     """Test that the contents of the list page contains something specific to this website."""
#     response = testapp.get('/', status=200)
#     html = response.html
#     assert 'Ben Shields' in str(html)


# def test_list_contents(testapp):
#     """Test that the contents of the list page contains as many <h2> tags as journal entries."""
#     from .views import ENTRIES
#     response = testapp.get('/', status=200)
#     html = response.html
#     assert len(ENTRIES) == len(html.findAll('h2'))


# def test_layout_post(testapp):
#     """Test that the contents of the post page contains something specific to this website."""
#     response = testapp.get('/', status=200)
#     html = response.html
#     assert 'Ben Shields' in str(html)


# def test_layout_update(testapp):
#     """Test that the contents of the update page contains something specific to this website."""
#     response = testapp.get('/', status=200)
#     html = response.html
#     assert 'Ben Shields' in str(html)


# def test_layout_new_post(testapp):
#     """Test that the contents of the new post page contains something specific to this website."""
#     response = testapp.get('/', status=200)
#     html = response.html
#     assert 'Ben Shields' in str(html)
