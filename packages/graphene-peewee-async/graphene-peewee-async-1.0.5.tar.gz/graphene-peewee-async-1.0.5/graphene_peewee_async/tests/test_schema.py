from py.test import raises

from ..types import PeeweeObjectType
from tests.utils import assert_equal_lists

from .models import Reporter


def test_should_raise_if_no_model():
    with raises(Exception) as excinfo:
        class Character1(PeeweeObjectType):
            pass
    assert 'model in the Meta' in str(excinfo.value)


def test_should_raise_if_model_is_invalid():
    with raises(Exception) as excinfo:
        class Character2(PeeweeObjectType):

            class Meta:
                model = 1
    assert 'not a Peewee model' in str(excinfo.value)


def test_should_map_fields_correctly():
    class ReporterType2(PeeweeObjectType):

        class Meta:
            model = Reporter
    assert_equal_lists(
        ReporterType2._meta.fields_map.keys(),
        ['articles', 'first_name', 'last_name', 'email', 'pets', 'id', 'films',
         'organization']
    )


def test_should_map_only_few_fields():
    class Reporter2(PeeweeObjectType):

        class Meta:
            model = Reporter
            only_fields = ('id', 'email')
    assert_equal_lists(
        Reporter2._meta.fields_map.keys(),
        ['id', 'email']
    )
