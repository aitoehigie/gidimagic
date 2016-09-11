# -*- coding: utf-8 -*-


import pytest

from procfile import (
    loads,
    loadfile,
)


def test_valid_procfile():
    lines = loads('\n'.join([
        'web: bundle exec rails server -p $PORT',
        'worker: env QUEUE=* bundle exec rake resque:work',
        'urgentworker: env QUEUE=urgent FOO=meh bundle exec rake resque:work',
    ]))
    assert lines == {
        'web': {'cmd': 'bundle exec rails server -p $PORT', 'env': []},
        'worker': {'cmd': 'bundle exec rake resque:work', 'env': [
            ('QUEUE', '*'),
        ]},
        'urgentworker': {'cmd': 'bundle exec rake resque:work', 'env': [
            ('QUEUE', 'urgent'),
            ('FOO', 'meh'),
        ]},
    }


def test_duplicate_process_types():
    with pytest.raises(ValueError) as error:
        print(loads('\n'.join([
            'web: bundle exec rails server -p $PORT',
            'web: bundle exec rake resque:work',
        ])))
    assert error.value.args[0] == [
        'Line 2: duplicate process type "web": already appears on line 1.',
    ]


def test_duplicate_variable():
    with pytest.raises(ValueError) as error:
        print(loads('\n'.join([
            'web: bundle exec rails server -p $PORT',
            'worker: env QUEUE=* QUEUE=urgent bundle exec rake resque:work',
        ])))
    assert error.value.args[0] == [
        'Line 2: duplicate variable "QUEUE" for process type "worker".',
    ]
