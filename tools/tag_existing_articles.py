#!/usr/bin/env python

"""

    goes through all the articles in the DB 
    by language and associates them with the
    corresponding topics
    

"""

import zeeguu
from zeeguu.model import Article, Language, LocalizedTopic

session = zeeguu.db.session

counter = 0

languages = Language.available_languages()

for language in languages:
    articles = Article.query.filter(Article.language == language).all()
    loc_topics = LocalizedTopic.all_for_language(language)

    for article in articles:
        counter += 1
        for loc_topic in loc_topics:
            if loc_topic.matches_article(article):
                article.add_topic(loc_topic.topic)
                print(f" #{loc_topic.topic_translated}: {article.url.as_string()}")
        session.add(article)
        if counter == 1000:
            print("1k more done. comitting... ")
            session.commit()
            counter = 0
