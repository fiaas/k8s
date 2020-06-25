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

Working with CRDs
=================

With k8s working with CRDs is very much like the way you would work with Deployment, Service or any of the other
resources provided by Kubernetes. Creating a CRD in the cluster is also quite straight forward.

Defining your CRD in the cluster
--------------------------------

In your application, you can create a :py:class:`~k8s.models.custom_resource_definition.CustomResourceDefinition`.
When you save this to the cluster, your CRD is created. Kubernetes uses some time to make things ready, so you will
need to poll the API to see when it gets ready.

Example::

    name = "%s.%s" % ("applications", "fiaas.schibsted.io")
    metadata = ObjectMeta(name=name)
    names = CustomResourceDefinitionNames(kind="Application", plural="applications", shortNames=("app", "fa"))
    spec = CustomResourceDefinitionSpec(group="fiaas.schibsted.io", names=names, version="v1")
    definition = CustomResourceDefinition.get_or_create(metadata=metadata, spec=spec)
    definition.save()


Defining your CRD in code
-------------------------

When a CRD is defined in the API, it can be used like any other Model, but you need to define it yourself.

This is similar to how we describe the built in models in this library. Check out
:ref:`adding-support-for-new-object-types` for details.

Example::

    class ApplicationSpec(Model):
        application = RequiredField(six.text_type)
        image = RequiredField(six.text_type)
        config = RequiredField(dict)

    class Application(Model):
        class Meta:
            list_url = "/apis/fiaas.schibsted.io/v1/applications"
            url_template = "/apis/fiaas.schibsted.io/v1/namespaces/{namespace}/applications/{name}"
            watch_list_url = "/apis/fiaas.schibsted.io/v1/watch/applications"
            watch_list_url_template = "/apis/fiaas.schibsted.io/v1/watch/namespaces/{namespace}/applications"

        # Workaround for https://github.com/kubernetes/kubernetes/issues/44182
        apiVersion = Field(six.text_type, "fiaas.schibsted.io/v1")  # NOQA
        kind = Field(six.text_type, "Application")

        metadata = Field(ObjectMeta)
        spec = Field(ApplicationSpec)
