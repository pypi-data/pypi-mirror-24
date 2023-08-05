import pytest

import traitlets as T
from .. import jstraitlets as jst
from ..jstraitlets import undefined


def test_undefined_singleton():
    assert jst.UndefinedType() is undefined


def generate_test_cases():
    """yield tuples of (trait, failcases, passcases)"""
    # Anys
    yield (jst.JSONAny(), [], [1, "hello", {'a':2}, [1, 2, 3], None, undefined])

    # Nulls
    yield (jst.JSONNull(), [0, "None"], [None, undefined])
    yield (jst.JSONNull(allow_undefined=False), [undefined], [])

    # Booleans
    yield (jst.JSONBoolean(), [0, 2, 'abc'], [True, False])
    yield (jst.JSONBoolean(allow_undefined=False), [undefined], [])

    # Numbers
    yield (jst.JSONNumber(), [None, '123'], [-10.5, 42, 3.14, undefined])
    yield (jst.JSONNumber(allow_undefined=False), [undefined], [])
    yield (jst.JSONNumber(minimum=0, maximum=100, multipleOf=0.5),
           [-10, 110, 33.3], [0, 50, 60.5, 100])
    yield (jst.JSONNumber(minimum=0, maximum=100,
                          exclusiveMinimum=True, exclusiveMaximum=True),
           [0, 100], [0.01, 0.99])

    # Integers
    yield (jst.JSONInteger(minimum=0, maximum=100, multipleOf=2),
           [-10, 110, 29], [0, 50, 62, 100])
    yield (jst.JSONInteger(allow_undefined=False), [undefined], [])
    yield (jst.JSONInteger(minimum=0, maximum=100,
                          exclusiveMinimum=True, exclusiveMaximum=True),
           [0, 100], [1, 99])
    yield (jst.JSONInteger(), [None, '123', 3.14], [-10, 0, 42])

    # Strings
    yield (jst.JSONString(), [50, None, True], ['abc', undefined])
    yield (jst.JSONString(allow_undefined=False), [undefined], [])
    yield (jst.JSONString(minLength=2, maxLength=4), ['', 'a', 'abcde'],
           ['ab', 'abc', 'abcd'])

    # Arrays
    yield (jst.JSONArray(jst.JSONString()),
           ["a", [1, 'b']], [["a", "a"], ['a'], undefined])
    yield (jst.JSONArray(jst.JSONString(), allow_undefined=False),
           [undefined], [])
    yield (jst.JSONArray(jst.JSONInteger(), minItems=1, maxItems=2),
           [[], [1, 2, 3]], [[1], [1, 1]])
    yield(jst.JSONArray(jst.JSONInteger(), uniqueItems=True),
          [[1, 1], [1, 2, 1]], [[], [1], [1, 2]])
    yield(jst.JSONArray(jst.JSONInstance(list), uniqueItems=True),
          [[[], []], [[1], [1]]], [[[], [1]], [[1], [2], [3]]])

    # Enums
    yield (jst.JSONEnum([1, "2", None]), ["1", 2, [1]],
                        [1, "2", None, undefined])
    yield (jst.JSONEnum([1, "2", None], allow_undefined=False), [undefined], [])

    # Instances
    yield (jst.JSONInstance(dict), [{1}, (1,), [1]], [{1:2}, undefined])
    yield (jst.JSONInstance(dict, allow_undefined=False), [undefined], [])

    # Unions and other collections
    yield (jst.JSONUnion([jst.JSONInteger(), jst.JSONString()]),
           [3.14, None], [42, "42", undefined])
    yield (jst.JSONAnyOf([jst.JSONInteger(), jst.JSONString()]),
           [3.14, None], [42, "42"])
    yield (jst.JSONOneOf([jst.JSONInteger(), jst.JSONNumber()]),
           [None, 3], [3.14])
    yield (jst.JSONAllOf([jst.JSONInteger(), jst.JSONNumber()]),
           [None, 3.14], [3])
    yield (jst.JSONNot(jst.JSONString()), ['a', 'abc'], [1, False, None])


@pytest.mark.parametrize('trait,failcases,passcases', generate_test_cases())
def test_traits(trait, failcases, passcases):
    obj = T.HasTraits()  # needed to pass to validate()

    for passcase in passcases:
        trait._validate(obj, passcase)

    for failcase in failcases:
        with pytest.raises(T.TraitError) as err:
            trait._validate(obj, failcase)


def test_hastraits_defaults():
    class Foo(jst.JSONHasTraits):
        _additional_traits = [T.Integer()]
        name = T.Unicode()

    f = Foo(name="Bob", age=40)
    f.set_trait('year', 2000)
    assert set(f.trait_names()) == {'name', 'age', 'year'}

    with pytest.raises(T.TraitError) as err:
        f.set_trait('foo', 'abc')

    with pytest.raises(T.TraitError) as err:
        f.set_trait('age', 'blah')


def test_hastraits_required():
    class Foo(jst.JSONHasTraits):
        _required_traits = ['name']
        name = jst.JSONString()
        age = jst.JSONNumber()

    f1 = Foo(name="Sue", age=32)
    f2 = Foo(age=32)

    # contains all required pieces
    D = f1.to_dict()

    with pytest.raises(T.TraitError) as err:
        f2.to_dict()
    assert err.match("Required trait 'name' is undefined")


def test_no_defaults():
    class Foo(jst.JSONHasTraits):
        _additional_traits = False
        name = T.Unicode()

    with pytest.raises(T.TraitError) as err:
        f = Foo(name="Sarah", year=2000)


def test_AnyOfObject():
    class Foo(jst.JSONHasTraits):
        intval = T.Integer()
        flag = T.Bool()

    class Bar(jst.JSONHasTraits):
        strval = T.Unicode()
        flag = T.Bool()

    class FooBar(jst.AnyOfObject):
        _classes = [Foo, Bar]
        pass

    FooBar(strval='hello', flag=True)
    FooBar(intval=5, flag=True)

    with pytest.raises(T.TraitError):
        h = FooBar(strval=666, flag=False)
    with pytest.raises(T.TraitError):
        h = FooBar(strval='hello', flag='bad arg')
    with pytest.raises(T.TraitError):
        h = FooBar(intval='bad arg', flag=False)
    with pytest.raises(T.TraitError):
        h = FooBar(intval=42, flag='bad arg')

    # Test from_dict
    FooBar.from_dict({'strval': 'hello', 'flag': True})
    FooBar.from_dict({'intval': 42, 'flag': False})


class Bar(jst.JSONHasTraits):
    _additional_traits = [T.Unicode()]
    val = T.Unicode()


class Foo(jst.JSONHasTraits):
    _additional_traits = False
    x = T.Integer()
    y = T.Instance(Bar)


def test_to_from_dict():
    dct = {'x': 4, 'y': {'val': 'hello'}}
    obj = Foo.from_dict(dct)
    dct2 = obj.to_dict()
    assert dct == dct2


def test_to_from_dict_with_defaults():
    dct = {'x': 4, 'y': {'val': 'hello', 'other_val': 'hello 2'}}
    obj = Foo.from_dict(dct)
    dct2 = obj.to_dict()
    assert dct == dct2

    dct = {'x': 4, 'z': 'blah', 'y': {'val': 'hello'}}
    with pytest.raises(T.TraitError):
        Foo.from_dict(dct)


def test_to_dict_explicit_null():
    class MyClass(jst.JSONHasTraits):
        bar = jst.JSONString(allow_none=True, allow_undefined=True)

    assert MyClass().to_dict() == {}
    assert MyClass(bar=None).to_dict() == {'bar': None}
    assert MyClass(bar='val').to_dict() == {'bar': 'val'}


def test_defaults():
    class Foo(jst.JSONHasTraits):
        arr = jst.JSONArray(jst.JSONString())
        val = jst.JSONInstance(dict)
    assert Foo().to_dict() == {}


def test_skip():
    class Foo(jst.JSONHasTraits):
        _skip_on_export = ['baz']
        bar = jst.JSONNumber()
        baz = jst.JSONNumber()
    f = Foo(bar=1, baz=2)
    assert f.to_dict() == {'bar': 1}


def test_finalize():
    class Foo(jst.JSONHasTraits):
        bar = jst.JSONNumber()
        bar_times_2 = jst.JSONNumber()
        L = jst.JSONArray(jst.JSONString())
        def _finalize(self):
            self.bar_times_2 = 2 * self.bar
            super(Foo, self)._finalize()
    f = Foo(bar=4, L=['a', 'b', 'c'])
    assert f.to_dict() == {'bar': 4, 'bar_times_2': 8, 'L':['a', 'b', 'c']}


def test_contains():
    class Foo(jst.JSONHasTraits):
        a = jst.JSONNumber()
        b = jst.JSONString()

    f = Foo(a=4)
    assert 'a' in f
    assert 'b' not in f
    assert 'c' not in f


def test_to_python():
    class Foo(jst.JSONHasTraits):
        _required_traits = ['a', 'b']
        a = jst.JSONNumber()
        b = jst.JSONString()

    class Bar(jst.JSONHasTraits):
        c = jst.JSONArray(jst.JSONNumber())
        d = jst.JSONInstance(Foo)
        e = jst.JSONArray(jst.JSONInstance(Foo))

    D = {'c': [1, 2, 3], 'd': {'a': 5, 'b': 'blah'},
         'e':[{'a': 3, 'b': 'foo'}, {'a': 4, 'b': 'bar'}]}
    obj = Bar.from_dict(D)
    obj2 = eval(obj.to_python())
    assert obj2.to_dict() == obj.to_dict() == D

    # Make sure there is an error if required traits are missing
    foo = Foo(a=4)
    with pytest.raises(T.TraitError) as err:
        foo.to_python()
