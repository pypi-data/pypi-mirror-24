=========
pychoice
=========

An utility adds code readability to your application and/or API, Code is documentation!


Install
-------

::

    pip install pychoice


Example
-------

::

    from pychoice import Choice

    Status = Choice(
        (0, 'item0'),
        (1, 'item1'),
        (2, 'item2')
    )

    assert Status('item0') == 0
    assert Status('item0', 'item1') == [0, 1]

    assert Status[0] == 'item0'
    assert Status[0, 1] == ['item0', 'item1']
    assert Status[...] == ['item0', 'item1', 'item2']

    assert Status.exclude('item0') == [1, 2]
    assert Status.pairs('item0', 'item2') == [(0, 'item0'), (2, 'item2')]


