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
