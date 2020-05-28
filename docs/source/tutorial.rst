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

Tutorial
========

k8s is a Python client library for the `Kubernetes API <https://kubernetes.io/docs/reference/api-overview/>`_.

Configure client
----------------

k8s uses a singleton config object to configure how the client should connect to the Kubernetes apiserver.::

  >>> from k8s import config
  >>> config.api_server = 'https://kubernetes.example.com:8443'

If the Kubernetes apiserver is using a self-signed SSL certificate, specify the CA certificate to verify against::

  >>> config.verify_ssl = 'path/to/ca.crt'

You can use client certificate based authentication::

  >>> config.cert = ('path/to/apiserver.crt', 'path/to/apiserver.key')

Or::

  >>> config.api_token = 'a3ViZXJuZXRlczogY29tbWFuZCBub3QgZm91bmQK'

We can verify that the client is configured correctly by reading the Service object for the Kubernetes apiserver::

  >>> from k8s.models.service import Service
  >>> Service.get('kubernetes')
  Service(spec=ServiceSpec(
      loadBalancerIP=None,
      loadBalancerSourceRanges=[],
      selector=None,
      clusterIP=10.0.0.1,
      sessionAffinity=ClientIP,
      type=ClusterIP,
      ports=[ServicePort(
          targetPort=8443,
          name=https,
          nodePort=None,
          protocol=TCP,
          port=443)]),
      metadata=ObjectMeta(
          name=kubernetes,
          labels={u'component': u'apiserver', u'provider': u'kubernetes'},
          namespace=default,
          resourceVersion=8,
          annotations=None)
  )


Create resources
----------------
To create a resource, like for example a Deployment, first import the required types::


    >>> from k8s.models.common import ObjectMeta
    >>> from k8s.models.pod import PodSpec, Container, ContainerPort, Probe, \
            HTTPGetAction, PodTemplateSpec
    >>> from k8s.models.deployment import Deployment, DeploymentSpec, \
            LabelSelector

Build the object graph representing the resource::

    >>> objectmeta = ObjectMeta(
            name='nginx',
            namespace='default',
            labels={'app': 'nginx'})
    >>> pod_spec = PodSpec(containers=[Container(
            name='nginx',
            image='nginx:1.13',
            ports=[ContainerPort(containerPort=80)],
            readinessProbe=Probe(HTTPGetAction(path='/', port=80)))])
    >>> pod_template_spec = PodTemplateSpec(metadata=objectmeta, spec=pod_spec)
    >>> deployment = Deployment(
            metadata=objectmeta,
            spec=DeploymentSpec(
                replicas=1,
                template=pod_template_spec,
                selector=LabelSelector(matchLabels={'app':'nginx'})))

Call the instance method `save` to post the request to create the resource to the Kubernetes apiserver::

    >>> deployment.save()


List and get resources
----------------------

We can now list Deployments to check that the resource was created::

  >>> Deployment.list()
  >>> [Deployment(
          status=DeploymentStatus(replicas=1,
          observedGeneration=1, updatedReplicas=1,
          ... # omitted for brevity
       )]

Or we can get the actual deployment directly, since we know the name::

  >>> Deployment.get('nginx')
  Deployment(status=DeploymentStatus(replicas=1, ... # omitted for brevity


Update resources
----------------

To update the resource we first get the current state of the resource::

  >>> deployment = Deployment.get('nginx')

If you want to update a resource with some state, but you don't know if it exists, it is possible to use the
`get_or_create` method rather than trying to `get` and then catching `NotFound` to handle the case where the resource
doesn't exist::

  >>> deployment = Deployment.get_or_create('nginx')

Either case, we can then modify the resource, and call `save` again to propagate the changes; let's say that we want
to scale up to two instances::

  >>> deployment.spec.replicas = 2
  >>> deployment.save()


Delete resources
----------------

To delete a resource, use the `delete` function. Note that for Deployments and for other objects that have dependent
objects, you need to pass a `DeleteOptions` object with a `propagationPolicy` to delete the dependent objects as well::

  >>> delete_options = {
      'kind': 'DeleteOptions',
      'apiVersion': 'v1',
      'propagationPolicy': 'Foreground'
  }
  >>> Deployment.delete('nginx', body=delete_options)

To delete multiple resources in a single call, use the `delete_list` function. You can use label-selectors to
filter what will be deleted, and you can pass `DeleteOptions` as explained above::

  >>> delete_options = DeleteOptions(propagationPolicy='Foreground')
  >>> label_selectors = {"foo": Equality("bar"), "dog": Inequality("cat")}
  >>> Ingress.delete_list(labels=label_selectors, delete_options=delete_options)


Watch resources
---------------

In order to watch resources for changes, there are two options. A low-level `watch_list` function, or the higher level :py:class:`~k8s.watcher.Watcher`, which handles some quirks of the watch process for you.

Watching is simple in both cases, but there are some differences in behavior::

  >>> watcher = Watcher(Pod)
  >>> for event in watcher.watch(namespace="production"):
  ...   _handle_watch_event(event)

Or::

  >>> for event in Pod.watch_list(namespace="production"):
  ...   _handle_watch_event_event)

The events yielded from the watch are objects of type :py:class:`~k8s.base.WatchEvent`, which has a type `ADDED`, `MODIFIED` or `DELETED` and the actual object the event relates to.

The API server has a configurable timeout for how long the watch can be in effect, and once that timeout happens, the watch will be closed. Similary, in order to detect situations where the connection is dead, there is a timeout on the client side, which will cause the connection to be closed if there has been no activity. The stream timeout is configured in :py:mod:`~k8s.config` and defaults to one hour.

When using `watch_list`, you are responsible for reconnecting the watch again. The `Watcher` takes care of reconnecting for you.

When starting a watch (even when reconnecting), the API server will send all known objects marking them as `ADDED`. The `Watcher` has a cache of the last 1000 objects seen (use `capacity` parameter to override). This avoids the case where you reconnect and then reprocess all objects even if you have already processed them.
