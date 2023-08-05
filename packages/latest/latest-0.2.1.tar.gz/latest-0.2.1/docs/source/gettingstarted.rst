Getting Started
===============


Basic Syntax
------------

Commands (code islands)
:::::::::::::::::::::::

The simplest thing that you can do with :mod:`latest` is to insert python expressions or **command** or **code island** inside a document. For a command to be evaluated a data context (python dictionary) had to be set up.

By default commands are bracketed between :code:`\latest[options]{$` and :code:`$}`. You can change these in the configuration file (see *code_entry* and *code_exit* options in *lang* section).

A plain text with code islands in between is called **expression**.

For example the expression

.. code::

   If a = \latest{$ a $} and b = \latest{$ b $}, then a + b = \latest{$ a+b $}

with a data context :code:`{a: '1', b: '2'}` evaluates to

.. code::

   If a = 1 and b = 2, then a + b = 3

Namespaces
::::::::::

Namespaces are a powerful concept in :mod:`latest`. A namespace is a branch of a data context (python dictionary). It can be a single data context or a list of data contexts.

A namespace can be useful to simplify variable names within python code with deep nested data contexts.

More interestingly, namespaces allow to creates loops without standard loop syntax.

Environments
::::::::::::

A more advanced concept is that of **environments**. An environment is defined by a namespace and an expression. The namespace define the branch of the data context in which to look for variable names in python code islands. If the namespace selects a list of dictionaries the environment is evaluated for each one of them and the results are joined by a special sequence of characters defined in a configuration file or as the option :code:`join_items`. This is effectively a :code:`for` loop implementation without the standard :code:`for` loop syntax.


Creating a template
-------------------

A template file can be of any type but latest searches in it for **commands** and **enviroments**.


Creating a data file
--------------------

Data formats supported by :mod:`latest` are

* json
* yaml (require optional :mod:`pyyaml`)


The latest cli
--------------

Run `latest` script from the command line

.. code-block:: bash

    $ latest template data


where 

    * **template** is the path to a template file
    * **data** is the path to a *json* or *yaml* formatted data file.


---------------------------------------------------------------------


An example template file can be something like

.. literalinclude:: ../../test/res/template.tmpl
   :language: latex


while the data file can be something like (*yaml*)

.. literalinclude:: ../../test/res/data.yaml
   :language: yaml


The expected output is

.. literalinclude:: ../../test/res/expected.tex
   :language: latex

