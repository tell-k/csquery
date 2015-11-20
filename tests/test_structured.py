# -*- coding: utf-8 -*-
"""
    tests.test_structured
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    unittest for csquery.structured

    :author: tell-k <ffk2005 at gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""
from __future__ import division, print_function, absolute_import, unicode_literals  # NOQA


class TestEscape(object):

    def _get_target(self):
        from csquery.structured import escape
        return escape

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        assert r"test\'test" == self._call_fut("test'test")
        assert r"\'test\'test\'" == self._call_fut("'test'test'")
        assert r"test\\test" == self._call_fut(r"test\test")


class TestFormatOptions(object):

    def _get_target(self):
        from csquery.structured import format_options
        return format_options

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        assert '' == self._call_fut({})
        assert ' test=test' == self._call_fut({'test': 'test'})


class TestFormatRangeValues(object):

    def _get_target(self):
        from csquery.structured import format_range_values
        return format_range_values

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        assert '[1900,2000]' == self._call_fut(start=1900, end=2000)
        assert '[0,2000]' == self._call_fut(start=0, end=2000)
        assert '{,2000]' == self._call_fut(start=None, end=2000)
        assert '{,2000]' == self._call_fut(start='', end=2000)
        assert '[1900,0]' == self._call_fut(start=1900, end=0)
        assert '[1900,}' == self._call_fut(start=1900)
        assert '[1900,}' == self._call_fut(start=1900, end=None)
        assert '[1900,}' == self._call_fut(start=1900, end='')


class TestFormatValue(object):

    def _get_target(self):
        from csquery.structured import format_value
        return format_value

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        from csquery.structured import Expression, field

        assert '[1900,2000]' == self._call_fut([1900, 2000])
        assert "(and title:'star')" == self._call_fut(
            Expression('and', title='star')
        )
        assert '[1900,2000]' == self._call_fut('[1900,2000]')
        assert '{,2000]' == self._call_fut('{,2000]')
        assert '[1900,}' == self._call_fut('[1900,}')
        assert 'field=test' == self._call_fut('field=test')
        assert '1' == self._call_fut(1)
        assert "actors:'Alec Guinness'" == self._call_fut(
            field('Alec Guinness', 'actors')
        )
        assert "'test'" == self._call_fut('test')

    def test_it_for_escape(self):
        from csquery.structured import Expression, field

        assert r"(and title:'st\\ar')" == self._call_fut(
            Expression('and', title=r'st\ar')
        )
        assert r"(and title:'st\'ar')" == self._call_fut(
            Expression('and', title="st'ar")
        )

        assert r"'te\\st'" == self._call_fut(r"te\st")
        assert r"'te\'st'" == self._call_fut("te'st")

        assert r"field=te\\st" == self._call_fut(r"field=te\st")
        assert r"field=te\'st" == self._call_fut("field=te'st")

        assert r"actors:'Alec\\Guinness'" == self._call_fut(
            field(r'Alec\Guinness', 'actors')
        )
        assert r"actors:'Alec\'Guinness'" == self._call_fut(
            field("Alec'Guinness", 'actors')
        )

    def test_it_for_escape__with_range_values(self):
        from csquery.structured import and_

        range_value = "['2000-01-01T00:00:00Z', '2010-01-01T00:00:00Z'}"
        expected = "(and release_date:"
        expected += "[\'2000-01-01T00:00:00Z\', \'2010-01-01T00:00:00Z\'})"
        assert expected == self._call_fut(and_(release_date=range_value))

        expected = "(and (and release_date:"
        expected += "[\'2000-01-01T00:00:00Z\', \'2010-01-01T00:00:00Z\'}))"
        assert expected == self._call_fut(and_(and_(release_date=range_value)))

        assert "(and _id:['tt1000000','tt1005000'])" == self._call_fut(
            and_(_id="['tt1000000','tt1005000']")
        )
        assert "(and _id:['tt\'1000000','tt\'1005000'])" == self._call_fut(
            and_(_id="['tt\'1000000','tt\'1005000']")
        )

    def test_it__with_multi_encoding(self):
        from csquery.structured import Expression
        import six
        binary_value = six.text_type("あ").encode("utf-8")
        text_value = six.text_type("あ")

        self._call_fut(
            Expression('and', title=binary_value)
        )
        self._call_fut(
            Expression('and', title=text_value)
        )


class TestFieldValue(object):

    def _get_target_class(self):
        from csquery.structured import FieldValue
        return FieldValue

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_init(self):

        field = self._make_one('test')
        assert None is field.name
        assert "'test'" == field.value

        field = self._make_one('test', 'name')
        assert 'name' is field.name
        assert "'test'" == field.value

        field = self._make_one({'name': 'test'})
        assert 'name' is field.name
        assert "'test'" == field.value

    def test_to_value(self):

        field = self._make_one('test')
        assert "'test'" == field.to_value()
        assert "'test'" == str(field)

        field = self._make_one('test', 'name')
        assert "name:'test'" == field.to_value()
        assert "name:'test'" == str(field)

        field = self._make_one({'name': 'test'})
        assert "name:'test'" == field.to_value()
        assert "name:'test'" == str(field)

    def test_repr(self):

        field = self._make_one('test')
        assert "<FieldValue: 'test'>" == repr(field)
        field = self._make_one('test', 'name')
        assert "<FieldValue: name:'test'>" == repr(field)
        field = self._make_one({'name': 'test'})
        assert "<FieldValue: name:'test'>" == repr(field)


class TestExpression(object):

    def _get_target_class(self):
        from csquery.structured import Expression
        return Expression

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)

    def test_init(self):
        target = self._make_one('and', {'boost': 3}, *[{'actor': 'test'}],
                                **dict(title='test'))
        assert 'and' == target.operator
        assert {'boost': 3} == target.options
        assert 2 == len(target.fields)

    def test_query(self):
        target = self._make_one('and', {'boost': 3}, *[{'actor': 'test'}],
                                **dict(title='test'))

        assert "(and boost=3 actor:'test' title:'test')" == target.query()
        assert "(and boost=3 actor:'test' title:'test')" == target()
        assert "(and boost=3 actor:'test' title:'test')" == str(target)

    def test_repr(self):
        target = self._make_one('and', {'boost': 3}, *[{'actor': 'test'}],
                                **dict(title='test'))

        expected = "<Expression: (and boost=3 actor:'test' title:'test')>"
        assert expected == repr(target)


class TestField(object):

    def _get_target(self):
        from csquery.structured import field
        return field

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):

        field = self._call_fut('value')
        assert "'value'" == field.to_value()
        assert "'value'" == str(field)

        field = self._call_fut('value', 'name')
        assert "name:'value'" == field.to_value()
        assert "name:'value'" == str(field)

        field = self._call_fut({'name': 'value'})
        assert "name:'value'" == field.to_value()
        assert "name:'value'" == str(field)


class TestAnd_(object):

    def _get_target(self):
        from csquery.structured import and_
        return and_

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        from csquery.structured import field, not_, or_, term

        actual = self._call_fut(title='star',
                                actors='Harrison Ford', year=('', 2000))
        expected = "(and actors:'Harrison Ford' title:'star' year:{,2000])"
        assert expected == actual()

        actual = self._call_fut({'title': 'star'}, {'title': 'star2'})
        assert "(and title:'star' title:'star2')" == actual()

        actual = self._call_fut(field('star', 'title'),
                                field('star2', 'title'))
        assert "(and title:'star' title:'star2')" == actual()

        actual = self._call_fut({'title': 'star'}, {'title': 'star2'}, boost=2)
        assert "(and boost=2 title:'star' title:'star2')" == actual()

        # complex query
        actual = self._call_fut(
            not_('テスト', field='genres'),
            or_(
                term('star', field='title', boost=2),
                term('star', field='plot')
            )
        )
        expected = "(and (not field=genres 'テスト') "
        expected += "(or (term field=title boost=2 'star') "
        expected += "(term field=plot 'star')))"
        assert expected == actual()


class TestOr_(object):

    def _get_target(self):
        from csquery.structured import or_
        return or_

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        from csquery.structured import field

        actual = self._call_fut(title='star',
                                actors='Harrison Ford', year=('', 2000))
        expected = "(or actors:'Harrison Ford' title:'star' year:{,2000])"
        assert expected == actual()

        actual = self._call_fut({'title': 'star'}, {'title': 'star2'})
        assert "(or title:'star' title:'star2')" == actual()

        actual = self._call_fut(field('star', 'title'),
                                field('star2', 'title'))
        assert "(or title:'star' title:'star2')" == actual()

        actual = self._call_fut({'title': 'star'}, {'title': 'star2'}, boost=2)
        assert "(or boost=2 title:'star' title:'star2')" == actual()


class TestNot_(object):

    def _get_target(self):
        from csquery.structured import not_
        return not_

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        from csquery.structured import and_

        actual = self._call_fut(and_(actors='Harrison Ford', year=('', 2010)))
        assert "(not (and actors:'Harrison Ford' year:{,2010]))" == actual()

        actual = self._call_fut(and_(actors='Harrison Ford',
                                     year=('', 2010)), boost=2)
        expected = "(not boost=2 (and actors:'Harrison Ford' year:{,2010]))"
        assert expected == actual()


class TestNear(object):

    def _get_target(self):
        from csquery.structured import near
        return near

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        actual = self._call_fut('teenage vampire')
        assert "(near 'teenage vampire')" == actual()

        actual = self._call_fut('teenage vampire', boost=2,
                                field='plot', distance=2)
        expected = "(near field=plot distance=2 boost=2 'teenage vampire')"
        assert expected == actual()


class TestPhrase(object):

    def _get_target(self):
        from csquery.structured import phrase
        return phrase

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        actual = self._call_fut('teenage girl')
        assert "(phrase 'teenage girl')" == actual()

        actual = self._call_fut('teenage girl', boost=2, field='plot')
        assert "(phrase field=plot boost=2 'teenage girl')" == actual()


class TestPrefix(object):

    def _get_target(self):
        from csquery.structured import prefix
        return prefix

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        actual = self._call_fut('star')
        assert "(prefix 'star')" == actual()

        actual = self._call_fut('star', boost=2, field='title')
        assert "(prefix field=title boost=2 'star')" == actual()


class TestRange_(object):

    def _get_target(self):
        from csquery.structured import range_
        return range_

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        actual = self._call_fut((1990, 2000))
        assert '(range [1990,2000])' == actual()
        actual = self._call_fut('[1990,2000]')
        assert '(range [1990,2000])' == actual()

        actual = self._call_fut((None, 2000))
        assert '(range {,2000])' == actual()
        actual = self._call_fut(('', 2000))
        assert '(range {,2000])' == actual()
        actual = self._call_fut('{,2000]')
        assert '(range {,2000])' == actual()

        actual = self._call_fut((1990,))
        assert '(range [1990,})' == actual()
        actual = self._call_fut((1990, None))
        assert '(range [1990,})' == actual()
        actual = self._call_fut((1990, ''))
        assert '(range [1990,})' == actual()
        actual = self._call_fut('[1990,}')
        assert '(range [1990,})' == actual()

        actual = self._call_fut(('1967-01-31T23:20:50.650Z',
                                 '1967-01-31T23:59:59.999Z'))
        expect = '(range [1967-01-31T23:20:50.650Z,1967-01-31T23:59:59.999Z])'
        assert expect == actual()

        actual = self._call_fut((1990, 2000), field='date', boost=2)
        assert '(range field=date boost=2 [1990,2000])' == actual()


class TestTerm(object):

    def _get_target(self):
        from csquery.structured import term
        return term

    def _call_fut(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        actual = self._call_fut('star')
        assert "(term 'star')" == actual()

        actual = self._call_fut(2000)
        assert '(term 2000)' == actual()

        actual = self._call_fut(2000, field='year', boost=2)
        expected = '(term field=year boost=2 2000)'
        assert expected == actual()
