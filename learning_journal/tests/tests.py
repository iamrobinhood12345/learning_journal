"""Testing suite for Learning Journal."""


import pytest
import transaction
import datetime

from pyramid import testing

from learning_journal.models import MyModel, get_tm_session
from learning_journal.models.meta import Base


TEST_ENTRIES = [
    {"title": "Learning Journal - Day 11", "title1": "Slowly Getting Better", "creation_date": datetime.datetime(2016, 12, 18, 0, 0), "body": "<p>Today was a good day. I started off asking questions right away and was more attentive than I am most days. This felt really good. I'm going to try to ask as many questions as I can. I'm also going to volunteer for code review tomorrow. Today we also formed our groups for project week. Looks like Pysearch is happening after all! I have a good group going, with Marc, Casey, and Sera. This should be a lot of fun. My thoughts are that we should start small, and get a working implementation of a search engine going quickly, and design it in such a way that we can add features easily. Will said something about a simple search engine tutorial on Udacity. I will definitely ask him about this. The number one take away today would be that I should participate as much as I can, even if I don't feel like it, especially in the mornings. Another thing I realized is that a lot of computer science is actually getting good with getting a bunch of different things to work together -- different files, file systems, frameworks, functions that must speak to each other, having an account with the service you are using, and really taking all of these sort of things one step at a time. Overall, I can't wait to start working on Pysearch!</p>"},
    {"title": "Learning Journal - Day 12", "title1": "Pitches and Tools", "creation_date": datetime.datetime(2016, 12, 19, 0, 0), "body": "<p>Today I learned a good deal about my classmates. Each of us took turns pitching ideas for project week projects. I was very impressed with the creativity of my classmates. Several of their ideas seem like very good ones. I wish I could help out with all of them. Alas, decisions must be made, and we will eventually come to each work on one of a handful of projects. Such is life. We must choose decisively, and live with our choices for the rest of our days.</p><p>Avery and Patrick had awesome presentations. I learned about Itertools from Patrick, and can't wait for the chance to practice. Avery presented on an enhancement for Visual Studio that allows you to see documentation for functions as you are writing them. How cool is that!</p>"},
    {"title": "DNA Transcription", "title1": "ATGCATGCATGCATGCATGCATGC", "creation_date": datetime.datetime(2016, 12, 19, 0, 0), "body": "I learned some stuff about some other stuff."},
    {"title": "Itertools", "title1": "New stuff learned", "creation_date": datetime.datetime(2016, 12, 20, 0, 0), "body": "I learned some stuff about some other stuff."},
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


def test_entry_page_returns_empty_when_empty(dummy_request):
    """Test that the entry view returns no objects when database empty."""
    from learning_journal.views.default import entry_page
    req = dummy_request
    req.matchdict = {"id": "1"}
    result = entry_page(req)
    assert result["entry"] is None


def test_entry_page_returns_correct_number_of_objects_when_exist(dummy_request, add_models):
    """Test that the entry view does return objects when the DB is populated."""
    from learning_journal.views.default import entry_page
    req = dummy_request
    req.matchdict = {"id": "1"}
    result = entry_page(req)
    assert len(result) == 1


def test_entry_page_returns_correct_object_when_exist(dummy_request, add_models):
    """Test that the entry view returns correct objects when the DB is populated."""
    from learning_journal.views.default import entry_page
    req = dummy_request
    req.matchdict = {"id": "1"}
    result = entry_page(req)
    assert result["entry"].title == TEST_ENTRIES[0]["title"]


def test_update_page_returns_empty_when_empty(dummy_request):
    """Test that the update view returns no objects when database empty."""
    from learning_journal.views.default import update_page
    req = dummy_request
    req.matchdict = {"id": "2"}
    result = update_page(req)
    assert result["entry"] is None


def test_update_page_returns_correct_number_of_objects_when_exist(dummy_request, add_models):
    """Test that the update view does return objects when the DB is populated."""
    from learning_journal.views.default import update_page
    req = dummy_request
    req.matchdict = {"id": "2"}
    result = update_page(req)
    assert len(result) == 1


def test_update_page_returns_correct_objects_when_exist(dummy_request, add_models):
    """Test that the update view does return objects when the DB is populated."""
    from learning_journal.views.default import update_page
    req = dummy_request
    req.matchdict = {"id": "2"}
    result = update_page(req)
    assert result["entry"].title == TEST_ENTRIES[1]["title"]


def test_update_page_edits_db_entry(dummy_request, add_models):
    """Test that the update view edits entries in the database."""
    from learning_journal.views.default import update_page
    req = dummy_request
    req.matchdict = {"id": "3"}
    req.method = "POST"
    req.POST["title"] = "a new post"
    req.POST["title1"] = "a new subtitle"
    req.POST["creation_date"] = datetime.datetime(2016, 12, 20, 0, 0)
    req.POST["body"] = "a new body"
    try:
        update_page(req)
    except:
        new_title = dummy_request.dbsession.query(MyModel).get(3).title
        assert new_title == "a new post"


def test_new_post_page_adds_db_entry(dummy_request, add_models):
    """Test that the new post view adds entries to the database."""
    from learning_journal.views.default import new_post_page
    row_count_before_post = dummy_request.dbsession.query(MyModel).count()
    req = dummy_request
    req.method = "POST"
    req.POST["title"] = "a new post"
    req.POST["title1"] = "a new subtitle"
    req.POST["creation_date"] = datetime.datetime(2016, 12, 20, 0, 0)
    req.POST["body"] = "a new body"
    try:
        new_post_page(req)
    except:
        row_count_after_post = dummy_request.dbsession.query(MyModel).count()
        assert row_count_after_post == row_count_before_post + 1


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


def test_index_page_with_data_has_entries(testapp, fill_the_db):
    """When there's data in the database, the index page has entries."""
    response = testapp.get('/', status=200)
    html = response.html
    assert len(html.find_all("h2")) == len(TEST_ENTRIES)


def test_post_page_renders(testapp):
    """The post page has an h1 in the html."""
    response = testapp.get('/journal/1', status=200)
    html = response.html
    assert len(html.find_all("h1")) == 1


def test_post_page_with_data_has_correct_entry(testapp, fill_the_db):
    """When there's data in the database,the post page has an entry."""
    response = testapp.get('/journal/1', status=200)
    html = response.html
    assert TEST_ENTRIES[0]["title"] in str(html)


def test_update_page_renders(testapp):
    """The post page has an h1 in the html."""
    response = testapp.get('/journal/2/edit-entry', status=200)
    html = response.html
    assert len(html.find_all("h1")) == 1


def test_update_page_with_data_has_correct_entry(testapp, fill_the_db):
    """When there's data in the database,the post page has an entry."""
    response = testapp.get('/journal/2', status=200)
    html = response.html
    assert TEST_ENTRIES[1]["title"] in str(html)


def test_new_post_page_renders(testapp):
    """The new post page has an h1 in the html."""
    response = testapp.get('/journal/new-entry', status=200)
    html = response.html
    assert len(html.find_all("h1")) == 1


def test_new_post_page_content(testapp):
    """Test new post page has something specific to the page."""
    response = testapp.get('/journal/new-entry', status=200)
    html = response.html
    assert "Write a new post here!" in str(html)


def test_about_page_renders(testapp):
    """The about page has an h1 in the html."""
    response = testapp.get('/about', status=200)
    html = response.html
    assert len(html.find_all("h1")) == 1


def test_about_page_content(testapp):
    """Test new post page has something specific to the page."""
    response = testapp.get('/about', status=200)
    html = response.html
    print(str(html))
    assert "About Me" in str(html)
