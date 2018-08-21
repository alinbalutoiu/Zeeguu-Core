import zeeguu
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from zeeguu.model.language import Language

db = zeeguu.db


class Cohort(zeeguu.db.Model):
    __table_args__ = {'mysql_collate': 'utf8_bin'}

    id = db.Column(db.Integer, primary_key=True)
    inv_code = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    language_id = db.Column(db.Integer, db.ForeignKey(Language.id))
    max_students = db.Column(db.Integer)
    language = relationship(Language, foreign_keys=[language_id])
    declared_level = Column(Integer)

    def __init__(self, inv_code, name, language, max_students, level=None):
        self.inv_code = inv_code
        self.name = name
        self.language = language
        self.max_students = max_students
        self.level = None

    @classmethod
    def find(cls, id):
        return cls.query.filter_by(id=id).one()

    @classmethod
    def get_id(cls, inv):
        c = cls.query.filter_by(inv_code=inv).one()
        return c.id

    def get_current_student_count(self):
        from zeeguu.model.user import User
        users_in_cohort = User.query.filter_by(cohort_id=self.id).all()
        return len(users_in_cohort)

    def cohort_still_has_capacity(self):
        if (self.get_current_student_count() < self.max_students):
            return True
        return False

    def get_students(self):
        from zeeguu.model.user import User

        # compatibility reasons: if there is an associated invitation code
        # use it; otherwise fallback on the cohort that's associated with the User
        if self.inv_code and len(self.inv_code) > 1:
            zeeguu.log("we have an invitation code...")
            return User.query.filter_by(invitation_code=self.inv_code).all()

        zeeguu.log("falling back on filtering based on cohort")
        return User.query.filter(User.cohort == self).all()

    def get_teachers(self):
        from zeeguu.model.teacher_cohort_map import TeacherCohortMap
        return TeacherCohortMap.get_teachers_for(self)

    @classmethod
    def exists_with_invite_code(cls, code: str):
        all_matching = cls.query.filter_by(inv_code=code).all()
        return len(all_matching) > 0
