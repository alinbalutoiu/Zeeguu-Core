from unittest import TestCase

from zeeguu.content_retriever.parallel_retriever import get_content_for_urls
from zeeguu.tests.model_test_mixin import ModelTestMixIn
from zeeguu.tests.testing_data import *


class TestContentRetrieval(ModelTestMixIn, TestCase):

    def test_simple_parallel_retrieval(self):
        urls = [EASIEST_STORY_URL,
                VERY_EASY_STORY_URL]

        content_and_urls = get_content_for_urls(urls)

        for each in content_and_urls:
            assert each['url']
            assert each['content']