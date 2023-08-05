TestDocker Changelog
~~~~~~~~~~~~~~~~~~

0.2.6
-----

Aug 3, 2017
* :class:`Command` returns command using :func:`__repr__ instead of :func:`__str__
* Added `file` kwarg to :meth:`CurlCommand.__init__` which accepts a file path
* :class:`CurlCommand` `file` support attempts to detect content type and set `Content-type` header
* :class:`CurlCommand` `file` support also attempts to detect character set on certain content-types
* Added `location(-L)` option to :attr:`CurlCommand.defaults`
* Fixed a race condition where :class:`Container` would crash during initialization if the container was still being started
* :meth:`Compose.up` now parses the service names from the docker-compose files instead of stdout
* Fixed :func:`util.set_defaults` to properly process scalar values while iterating dictionary key, values
* Added a few new utility methods to :mod:`util`
* Finished the basic documention of public classes, functions, and methods
* Added basic usage documentation
* Added cli command: `testdocker init` for initializing the tests folder inside
  of the current project folder.


0.2.5
-----

Feb 11, 2016
* :class:`Compose` object now allows multiple compose files to be passed
* Mixins in :mod:`mixins` now waits for all containers
* Various optimizations for speed


0.2.1
-----

Feb 11, 2016
* Small changes to the class names in :mod:`mixins`.
* Added a hook in :meth:`ContainerTestMixinBase.setUpClass` that looks for a method called :meth:`container_ready` on all subclasses. This method should block until the container is ready to be tested, then return `True`


0.2.0
-----

Feb 2, 2016

* Initial commit
