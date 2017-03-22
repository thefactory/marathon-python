from marathon.util import to_camel_case, to_snake_case


def _apply_on_pairs(f):
    # this strategy is used to have the assertion stack trace
    # point to the right pair of strings in case of test failure
    f('foo', 'foo')
    f('foo42', 'foo42')
    f('fooBar', 'foo_bar')
    f('f0o42Bar', 'f0o42_bar')
    f('fooBarBaz', 'foo_bar_baz')
    f('ignoreHttp1xx', 'ignore_http1xx')
    f('whereAmI', 'where_am_i')
    f('iSee', 'i_see')
    f('doISee', 'do_i_see')


def test_to_camel_case():
    def test(camel, snake):
        assert to_camel_case(snake) == camel

    _apply_on_pairs(test)


def test_to_snake_case():
    def test(camel, snake):
        assert to_snake_case(camel) == snake

    _apply_on_pairs(test)
