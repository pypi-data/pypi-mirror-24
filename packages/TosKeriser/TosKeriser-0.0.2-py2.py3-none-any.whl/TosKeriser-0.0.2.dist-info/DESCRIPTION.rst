TosKeriser
==========

TosKeriser is a tool to complete
`TosKer <https://github.com/di-unipi-socc/TosKer>`__ applications with
suitable Docker Images. The user can specify the software required by
each component and the tool complete the specification with a suitable
container to run the components.

For instance the following application has a components called
``server`` require a set of software (node>=6.2, ruby>2 and any version
of wget) and Debian as distribution.

::

    ...
    server:
      type: tosker.nodes.Software
      requirements:
      - host:
         node_filter:
           properties:
           - supported_sw:
             - node: 6.2.x
             - ruby: 2.x.x
             - wget: x.x.x
           - os_distribution: debian
    ...

After run tosKeriser on this specification, it creates the component
``server_container`` and connects the ``server`` component to it. It is
possible to see that the ``server_container`` has all the software
required by ``server`` and has also Debian 8 as Linux distribution.

::

    server:
      type: tosker.nodes.Software
      requirements:
      - host:
         node_filter:
           properties:
           - supported_sw:
             - node: 6.2.x
             - ruby: 2.x.x
             - wget: x.x.x
           - os_distribution: debian
           node: server_container

    server_container:
      type: tosker.nodes.Container
      properties:
        supported_sw:
          node: 6.2.1
          ruby: 2.5.0
          wget: 1.16
          perl: 5.20.2
        os_distribution: Debian GNU/Linux 8 (jessie)
      artifacts:
        my_image:
          file: composer/composer:latest
          type: tosker.artifacts.Image
          repository: docker_hub

More examples can be found in the ``examples`` folder.

Installation
------------

In is possible to install TosKeriser by using pip:

::

    # pip install tosker

The minimum Python version supported is 2.7.

Usage
-----

::

    TosKeriser, a tool to complete TosKer application description with suitable Docker Images.

    toskerise FILE [COMPONENT..] [OPTIONS]
    toskerise --help|-h
    toskerise --version|-v

    FILE
      TOSCA YAML file or a CSAR to be completed

    COMPONENT
      a list of component to be completed (by default all component are considered)

    OPTIONS
      --debug                              active debug mode
      -q|--quiet                           active quiet mode
      -i|--interactive                     active interactive mode
      -f|--force                           force the update of all containers
      --constraints=value                  constraint to give to DockerFinder
                                           (e.g. --constraints 'size<=100MB pulls>30 stars>10')
      --policy=top_rated|size|most_used    ordering of the images

License
-------

MIT license


