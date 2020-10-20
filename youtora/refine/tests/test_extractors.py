# from django.test import TestCase
from unittest import TestCase
# warning:https://docs.djangoproject.com/en/3.1/topics/testing/overview/
# If your tests rely on database access such as creating or querying models,
# be sure to create your test classes as subclasses of django.test.TestCase rather than unittest.TestCase.


class IdiomExtractorTestCase(TestCase):

    def setUp(self) -> None:
        """
        for setting up
        :return:
        """
        pass