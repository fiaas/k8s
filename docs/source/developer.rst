..
  Copyright 2017-2019 The FIAAS Authors

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

Developer guide
===============

Contributing
------------

There are large parts of the Kubernetes API that are not covered by this library yet, but we welcome anyone who wishes to help us make it more complete.

If you want to contribute, read the rest of this guide, open an issue to discuss the changes you want to do (if you feel it is needed), and finally send us a Pull Request with your changes.

We strive to have good test coverage, and PRs with failing or ignored tests will not be accepted. We also encourage you to add at least a minimal set of tests for the new code you write. Since some parts of the library are harder to test than others, look at other, similar, parts of the library to see the level of testing wanted.

We use Prospector_ for code quality/style checking, and PRs failing this check might be required to fix any issues before being merged. The code style in the project is close to PEP8, so should not present any big problems.

.. _Prospector: https://prospector.landscape.io/


.. _adding-support-for-new-object-types:

Adding support for new object types
-----------------------------------

If you want to create support for a new type of object in the Kubernetes API, the best thing to start with is the `Kubernetes API reference`_ documentation. The first thing you need to do, is find the "top most" type, ie. the type you operate on through the API. We can call this an API type. Examples are :py:class:`~k8s.models.pod.Pod`, :py:class:`~k8s.models.service.Service` or :py:class:`~k8s.models.ingress.Ingress`.

Create a new module under :py:mod:`k8s.models` if your type doesn't belong in any of the existing ones, then start by creating a class inheriting from :py:class:`~k8s.base.Model` named the same as the type is named in the Kubernetes documentation. Use the same casing as the Kubernetes documentation uses.

For your API type, inside the class you should declare an inner class called ``Meta``, which has a single field ``url_template``. This should be the URL template used when getting, creating or updating objects of this type (see the above mentioned examples).

For each field in the Kubernetes documentation, add a field to the class named exactly the same (including case). If the name is an invalid python identifier, add a ``_`` suffix (so ``exec`` becomes ``exec_``). The value of the field should be an instance of a subclass of :py:class:`~k8s.fields.Field`, depending on the semantics of the field.

====================================== ========================================
Use this class...                      ...when
====================================== ========================================
:py:class:`~k8s.fields.ListField`      the field is a list (aka array)
:py:class:`~k8s.fields.OnceField`      the field can only be set on new objects
:py:class:`~k8s.fields.RequiredField`  the field is required
:py:class:`~k8s.fields.ReadOnlyField`  the field is set by the API server
:py:class:`~k8s.fields.Field`          none of the above applies
====================================== ========================================

The :py:class:`~k8s.fields.Field` class takes three parameters:

type
    The type of value this field contains. Can be simple types (int, bool etc), :py:class:`datetime.datetime` or subclasses of :py:class:`~k8s.base.Model`.

default_value
    The field is set to this value when an instance of the class is created. The default default is ``None``.

alt_type
    The Kubernetes API will in some cases accept two types for a field (usually integer and string). This is the less common of the two, otherwise it has the same meaning as ``type``.

    This parameter is not available for the :py:class:`~k8s.fields.ListField`, but so far we have not come across any case where it is needed.

Once you have created a class for your API type, some of the fields will refer to new types which have yet to be defined. Make sure to use existing types defined elsewhere (possibly moving them to :py:mod:`k8s.models.common` if they are used in multiple places. Continue defining new subclasses of :py:class:`~k8s.base.Model` for each type needed, until you have created all the types required for your API type to be completely specified.

.. note::

    If the Kubernetes documentation says the type is ``object``, the python type should be ``dict``. If the Kubernetes documentation says the type is ``string``, we use ``six.text_type`` to maintain compatibility with both Python 2 and 3. Most other simple types are obvious.


.. literalinclude:: ../../k8s/models/autoscaler.py
    :caption: How the :py:class:`~k8s.models.autoscaler.HorizontalPodAutoscaler` type is implemented
    :language: python
    :lines: 12-
    :linenos:


.. _`Kubernetes API reference`: https://kubernetes.io/docs/api-reference/v1.6/

Releasing a new version
-----------------------

To make a new release there are a couple steps to follow. Ideally, we want to release from master, as often as possible. Version numbers should adhere to SemVer_. When you have a passing build that you want to make a release from, do the following steps:

- Create an annotated tag for the commit in question, naming it ``v<major>.<minor>.<bugfix>``. For instance::

    $ git tag -a v0.0.2 a1b2c3d4

- Push the new tag to github::

    $ git push origin v0.0.2

- A new release with the version you selected as a tag should now be built and uploaded to PyPI_ and Github_

.. _SemVer: http://semver.org/
.. _SemaphoreCI: https://semaphoreci.com/fiaas/k8s
.. _PyPI: https://pypi.python.org/pypi/k8s
.. _Github: https://github.com/fiaas/k8s/releases
