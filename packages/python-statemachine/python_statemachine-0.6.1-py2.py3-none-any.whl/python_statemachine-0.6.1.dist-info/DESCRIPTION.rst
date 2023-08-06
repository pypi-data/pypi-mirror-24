===============================
Python State Machine
===============================


.. image:: https://img.shields.io/pypi/v/python-statemachine.svg
        :target: https://pypi.python.org/pypi/python-statemachine

.. image:: https://img.shields.io/travis/fgmacedo/python-statemachine.svg?branch=master
        :target: https://travis-ci.org/fgmacedo/python-statemachine
        :alt: Build status

.. image:: https://codecov.io/gh/fgmacedo/python-statemachine/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/fgmacedo/python-statemachine
        :alt: Coverage report

.. image:: https://readthedocs.org/projects/python-statemachine/badge/?version=latest
        :target: https://python-statemachine.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/fgmacedo/python-statemachine/shield.svg
     :target: https://pyup.io/repos/github/fgmacedo/python-statemachine/
     :alt: Updates


Python `finite-state machines <https://en.wikipedia.org/wiki/Finite-state_machine>`_ made easy.


* Free software: MIT license
* Documentation: https://python-statemachine.readthedocs.io.


Getting started
===============

To install Python State Machine, run this command in your terminal:

.. code-block:: console

    $ pip install python-statemachine


Define your state machine::

    from statemachine import StateMachine, State

    class TrafficLightMachine(StateMachine):
        green = State('Green', initial=True)
        yellow = State('Yellow')
        red = State('Red')

        slowdown = green.to(yellow)
        stop = yellow.to(red)
        go = red.to(green)


You can now create an instance:

>>> traffic_light = TrafficLightMachine()

And inspect about the current state:

>>> traffic_light.current_state
State('Green', identifier='green', value='green', initial=True)
>>> traffic_light.current_state == TrafficLightMachine.green == traffic_light.green
True

For each state, there's a dinamically created property in the form ``is_<state.identifier>``, that
returns ``True`` if the current status matches the query:

>>> traffic_light.is_green
True
>>> traffic_light.is_yellow
False
>>> traffic_light.is_red
False

Query about metadata:

>>> [s.identifier for s in m.states]
['green', 'red', 'yellow']
>>> [t.identifier for t in m.transitions]
['go', 'slowdown', 'stop']

Call a transition:

>>> traffic_light.slowdown()

And check for the current status:

>>> traffic_light.current_state
State('Yellow', identifier='yellow', value='yellow', initial=False)
>>> traffic_light.is_yellow
True

You can't run a transition from an invalid state:

>>> traffic_light.is_yellow
True
>>> traffic_light.slowdown()
Traceback (most recent call last):
...
LookupError: Can't slowdown when in Yellow.

You can also trigger events in an alternative way, calling the ``run(<transition.identificer>)`` method:

>>> traffic_light.is_yellow
True
>>> traffic_light.run('stop')
>>> traffic_light.is_red
True

A state machine can be instantiated with an initial value:

>>> machine = TrafficLightMachine(start_value='red')
>>> traffic_light.is_red
True


Models
------

If you need to persist the current state on another object, or you're using the
state machine to control the flow of another object, you can pass this object
to the ``StateMachine`` constructor:

>>> class MyModel(object):
...     def __init__(self, state):
...         self.state = state
...
>>> obj = MyModel(state='red')
>>> traffic_light = TrafficLightMachine(obj)
>>> traffic_light.is_red
True
>>> obj.state
'red'
>>> obj.state = 'green'
>>> traffic_light.is_green
True
>>> traffic_light.slowdown()
>>> obj.state
'yellow'
>>> traffic_light.is_yellow
True


Events
------

Docs needed.


Mixins
------

Docs needed.


History
=======

0.6.1 (2017-08-25)
------------------

* Fix deploy issues.


0.6.0 (2017-08-25)
------------------

* Auto-discovering `statemachine`/`statemachines` under a Django project when
they are requested using the mixin/registry feature.

0.5.1 (2017-07-24)
------------------

* Fix bug on ``CombinedTransition._can_run`` not allowing transitions to run if there are more than
  two transitions combined.

0.5.0 (2017-07-13)
------------------

* Custom exceptions.
* Duplicated definition of ``on_execute`` callback is not allowed.
* Fix bug on ``StateMachine.on_<transition.identifier>`` being called with extra ``self`` param.

0.4.2 (2017-07-10)
------------------

* Python 3.6 support.
* Drop official support for Python 3.3.
* `Transition` can be used as decorator for `on_execute` callback definition.
* `Transition` can point to multiple destination states.


0.3.0 (2017-03-22)
------------------

* README getting started section.
* Tests to state machine without model.


0.2.0 (2017-03-22)
------------------

* ``State`` can hold a value that will be assigned to the model as the state value.
* Travis-CI integration.
* RTD integration.


0.1.0 (2017-03-21)
------------------

* First release on PyPI.


