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

k8s - Python client library for the Kubernetes API
--------------------------------------------------

|Semaphore Build Status Badge| |Codacy Grade Badge| |Codacy Coverage Badge|

.. |Semaphore Build Status Badge| image:: https://fiaas-svc.semaphoreci.com/badges/k8s.svg?style=shields
    :target: https://fiaas-svc.semaphoreci.com/branches/8e8fdc8c-cd55-4ba3-9dcf-38880531e601
.. |Codacy Grade Badge| image:: https://app.codacy.com/project/badge/Grade/4ebbdb3f34b0452fbbf48bb337dc6465
   :target: https://app.codacy.com/gh/fiaas/k8s/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade
.. |Codacy Coverage Badge| image:: https://app.codacy.com/project/badge/Coverage/4ebbdb3f34b0452fbbf48bb337dc6465
   :target: https://app.codacy.com/gh/fiaas/k8s/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage

Documentation
    https://k8s.readthedocs.io
Code
    https://github.com/fiaas/k8s

k8s is a python client library for Kubernetes developed as part of the FiaaS project at FINN.no, Norway's leading classifieds site. The library tries to provide an intuitive developer experience, rather than modelling the REST API directly. Our approach does not allow us to use Swagger to auto-generate a library that covers the entire API, but the parts we have implemented are (in our opinion) easier to work with than the client you get when using Swagger.

Check out the tutorial_ to find out how to use the library, or the `developer guide`_ to learn how to extend the library to cover parts of the API we haven't gotten around to yet.

.. _tutorial: http://k8s.readthedocs.io/en/latest/tutorial.html
.. _developer guide: http://k8s.readthedocs.io/en/latest/developer.html
