``subtoml``: Sed for TOML
=========================

``subtoml`` is a small CLI utility that substitutes parts of a TOML file.

.. code-block:: console

   $ cat sample.toml
   [database]
   url = "postgresql://localhost/sample"
   [web]
   debug = true
   $ subtoml database.url 'postgresql://localhost/test' < sample.toml
   [database]
   url = "postgresql://localhost/test"
   [web]
   debug = true

Please read ``subtoml --help`` for more details.

Distributed under GPLv3_ or later.

.. _GPLv3: http://www.gnu.org/licenses/gpl-3.0.html


Changelog
---------

Version 0.3.0
`````````````

Released on August 29, 2017.

- Added ``-d``/``--delete``/``--delete-key`` option.
- Added ``--version`` option.


Version 0.2.0
`````````````

Released on July 7, 2017.

- Added ``-i``/``--input-file`` option.
- Added ``-o``/``--output-file`` option.


Version 0.1.1
`````````````

Released on April 17, 2017.

- Fixed ``TypeError`` with the recent versions of pytoml_.

.. _pytoml: https://github.com/avakar/pytoml


Version 0.1.0
`````````````

Released on September 9, 2017. Initial release.
