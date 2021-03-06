#!/usr/bin/env python

"""

   Script that goes through all the users in a DB
   and renames their names with random ones.

"""
import sqlalchemy

import zeeguu
from faker import Faker
fake = Faker()
from zeeguu.model import User

session = zeeguu.db.session

for user in User.query.all():
    for _ in range(0,13):
        try:
            user.name = fake.name()
            user.email = fake.email()
            user.password = ""
            session.add(user)
            session.commit()
            print (f"added {user.name}")
            break
        except sqlalchemy.exc.IntegrityError as e:
            print (f"retrying...")
            continue
