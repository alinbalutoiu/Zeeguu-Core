import random

import zeeguu
from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from tests_core_zeeguu.rules.exercise_rule import ExerciseRule
from tests_core_zeeguu.rules.outcome_rule import OutcomeRule
from tests_core_zeeguu.rules.user_rule import UserRule
from tests_core_zeeguu.rules.user_word_rule import UserWordRule
from zeeguu.algos.algo_service import AlgoService

db = zeeguu.db
from zeeguu.model.knowledge_estimator import SimpleKnowledgeEstimator


class FeedTest(ModelTestMixIn):
    def setUp(self):
        super().setUp()
        self.user_rule = UserRule()
        self.user = self.user_rule.user

    def test_words_being_learned(self):
        """Tests whether user bookmarks with exercises in their logs are
        flagged as 'learned'
        """
        length_should_be = random.randint(2, 5)
        self.user_rule.add_bookmarks(length_should_be)

        # Add a random number of exercises to all bookmarks
        user_bookmarks = self.user.all_bookmarks()
        for b in user_bookmarks:
            for _ in range(1, random.randint(2, 5)):
                random_exercise = ExerciseRule().exercise
                b.add_new_exercise(random_exercise)

        # Check whether exercises are flagged as 'learned'
        est = SimpleKnowledgeEstimator(self.user)
        length_to_check = len(est.words_being_learned())

        assert length_should_be == length_should_be, (
            str(length_to_check) + " should be " + str(length_should_be)
        )

    def test_get_known_bookmarks(self):
        """Tests whether bookmarks with exercises are flagged as 'known'
        when their Outcome was 'too easy'
        """
        # Add a random number of bookmarks with the same learned language id
        # as the user to the user
        count_bookmarks = random.randint(2, 5)
        origin_word = UserWordRule(self.faker.word(), self.user.learned_language).user_word
        self.user_rule.add_bookmarks(count_bookmarks, origin=origin_word)
        est = SimpleKnowledgeEstimator(self.user)

        # Get how many bookmarks are 'known'. Should be 0.
        before = est.get_known_bookmarks()

        # Add an exercise with Outcome TOO_EASY to random number of bookmarks
        user_bookmarks = self.user.all_bookmarks()
        for i in range(1, random.randint(1, count_bookmarks)):
            bookmark = user_bookmarks[i]
            random_exercise = ExerciseRule().exercise
            random_exercise.outcome = OutcomeRule().too_easy
            bookmark.add_new_exercise(random_exercise)

        after = est.get_known_bookmarks()

        assert len(after) > len(before), (
            str(len(after))
            + " should be larger than "
            + str(len(before))
        )
