gogo
====

gogo - Go everywhere you want to go, never get lost in Go world (again).

Why
---

Because we always remember the package name, not its author's GitHub account.

Usage
-----

Print out full path of given go package::

  $ gogo yaml.v2
  /Users/hvn/golang/src/gopkg.in/yaml.v2
  $ gogo logrus
  /Users/hvn/golang/src/github.com/Sirupsen/logrus

Print out quoted import path of given go package::

  $ gogo -i yaml.v2
  "gopkg.in/yaml.v2"
  $ gogo -i logrus
  "github.com/Sirupsen/logrus"

Find and cd to directory of a package::

  cd `gogo docker`

Add import path from inside vim::

  :r ! gogo logrus

Of course, the package must already on your disk, and the ``$GOPATH`` is
correctly set.

Installtion
-----------

Use pip::

  pip install gogo

Or run ``setup.py`` file::

  python setup.py install

TODO
----

- support Py3
- port to Golang
