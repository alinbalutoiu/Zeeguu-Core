import flask_sqlalchemy

import zeeguu
from flask import Flask

from zeeguu.configuration.configuration import load_configuration_or_abort

# If zeeguu.app is already defined we use that object
# as the app for the db_init that we do later. If not,
# we create the app here and load the corresponding configuration
if not hasattr(zeeguu, "app"):
    zeeguu.app = Flask("Zeeguu-Core")
    load_configuration_or_abort(zeeguu.app, 'ZEEGUU_CORE_CONFIG',
                                ['MAX_SESSION',
                                 'SQLALCHEMY_DATABASE_URI',
                                 'SQLALCHEMY_TRACK_MODIFICATIONS'])

# Create the zeeguu.db object, which will be the superclass
# of all the model classes
zeeguu.db = flask_sqlalchemy.SQLAlchemy(zeeguu.app)
# Note, that if we pass the app here, then we don't need later
# to push the app context

# the core model
from .language import Language
from .url import Url
from .domain_name import DomainName
from .article import Article
from .bookmark import Bookmark
from .text import Text
from .user import User
from .user_word import UserWord
from .user_preference import UserPreference
from .session import Session
from .unique_code import UniqueCode
from .word_knowledge.word_interaction_history import WordInteractionHistory

from .user_language import UserLanguage


from .topic import Topic
from .user_article import UserArticle
from .article_word import ArticleWord
from .articles_cache import ArticlesCache

from .feed import RSSFeed
from .feed_registrations import RSSFeedRegistration

from .topic import Topic
from .topic_subscription import TopicSubscription
from .topic_filter import TopicFilter
from .localized_topic import LocalizedTopic

from .search import Search
from .search_filter import SearchFilter
from .search_subscription import SearchSubscription

# exercises
from .exercise import Exercise
from .exercise_outcome import ExerciseOutcome
from .exercise_source import ExerciseSource

# user logging
from .user_activitiy_data import UserActivityData
from .smartwatch.watch_event_type import WatchEventType
from .smartwatch.watch_interaction_event import WatchInteractionEvent

# teachers and cohorts
from .cohort import Cohort
from .teacher_cohort_map import TeacherCohortMap
from .teacher import Teacher

from .user_reading_session import UserReadingSession
from .user_exercise_session import UserExerciseSession

# Creating the DB tables if needed
# Note that this must be called after all the model classes are loaded
zeeguu.db.init_app(zeeguu.app)
zeeguu.db.create_all(app=zeeguu.app)

print(('ZEEGUU: Linked model with: ' + zeeguu.app.config["SQLALCHEMY_DATABASE_URI"]))
