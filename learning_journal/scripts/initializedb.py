import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import MyModel

ENTRIES = [
    {"title": "Learning Journal - Day 12", "title1": "Slowly Getting Better", "creation_date": "Dec 20, 2016", "body": "<p>Today was a good day. I started off asking questions right away and was more attentive than I am most days. This felt really good. I'm going to try to ask as many questions as I can. I'm also going to volunteer for code review tomorrow. Today we also formed our groups for project week. Looks like Pysearch is happening after all! I have a good group going, with Marc, Casey, and Sera. This should be a lot of fun. My thoughts are that we should start small, and get a working implementation of a search engine going quickly, and design it in such a way that we can add features easily. Will said something about a simple search engine tutorial on Udacity. I will definitely ask him about this. The number one take away today would be that I should participate as much as I can, even if I don't feel like it, especially in the mornings. Another thing I realized is that a lot of computer science is actually getting good with getting a bunch of different things to work together -- different files, file systems, frameworks, functions that must speak to each other, having an account with the service you are using, and really taking all of these sort of things one step at a time. Overall, I can't wait to start working on Pysearch!</p>"},
    {"title": "Learning Journal - Day 11", "title1": "Pitches and Tools", "creation_date": "Dec 19, 2016", "body": "<p>Today I learned a good deal about my classmates. Each of us took turns pitching ideas for project week projects. I was very impressed with the creativity of my classmates. Several of their ideas seem like very good ones. I wish I could help out with all of them. Alas, decisions must be made, and we will eventually come to each work on one of a handful of projects. Such is life. We must choose decisively, and live with our choices for the rest of our days.</p><p>Avery and Patrick had awesome presentations. I learned about Itertools from Patrick, and can't wait for the chance to practice. Avery presented on an enhancement for Visual Studio that allows you to see documentation for functions as you are writing them. How cool is that!</p>"},
    {"title": "DNA Transcription", "title1": "ATGCATGCATGCATGCATGCATGC", "creation_date": "Dec 20, 2016", "body": "I learned some stuff about some other stuff."},
    {"title": "Itertools", "title1": "New stuff learned", "creation_date": "Dec 20, 2016", "body": "I learned some stuff about some other stuff."},
    {"title": "Lambda", "title1": "x = lambda x, y: x+ y", "creation_date": "Dec 20, 2016", "body": "I learned some stuff about some other stuff."},
    {"title": "Learning from our Mistakes: Journey of a Computer Scientist", "title1": "How to iterate on improvement in the learning of programming.", "creation_date": "Dec 20, 2016", "body": "I learned some stuff about some other stuff."},
]

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        for each in ENTRIES:
            model = MyModel(title=each["title"], title1=each["title1"], creation_date=each["creation_date"], body=each["body"])
            dbsession.add(model)
