
***************************************
Restricted Python Expression Evaluation
***************************************

This is a small experimental project to test if its possible to evaluate Python code,
in a secure restricted mode,
where its not possible for a malicious expression to *break out* of.

This is done by restricting both the name-space and byte codes that can execute.

The module exposes a function called ``safe_eval``, this works like Python's ``eval``,
but checks the resulting code does not...

- Use any named identifiers outside a white-list
  *(made from the namespace and selected built-ins).*
- Use byte-codes that can be used to do malicious commands
  *(imports and _all_ attribute access is disabled for example).*

For general Python scripting this is overly restrictive,
however this can be used to execute math expressions.

.. note::

   Currently we're looking to see if this approach is a reliable way to secure/sand-box Python,
   please check if you can pass strings in a way that can be abused, we'd like to know!


Example use:

.. code-block:: Python

   from safe_eval import safe_eval

   value = safe_eval("1 / 2")

   a, b = 1, 2
   value = safe_eval("a / b", locals=locals())

   import math
   a, b = 10.0, 20.0
   value = safe_eval("sqrt(a ** b)", locals=dict(a=a, b=b, sqrt=math.sqrt))


Where these will fail:

.. code-block:: Python

   value = safe_eval("__import__('os').listdir('.')")

   value = safe_eval("open('test', 'r')")


To check other examples of what does and doesn't work, check ``test.py``.

If you find any workarounds to this module, please report a bug.


Caveats
=======

Running out of memory will raise a ``MemoryError`` and isn't prevented:

.. code-block:: Python

   '0' * (2 ** 60)

Entering an infinite loop isn't prevented:

(note that ``iter`` isn't available, so would need to be passed in).

.. code-block:: Python

   sum(iter(int, 1))

Explicitly passing in functions which can be used maliciously isn't prevented:

.. code-block:: Python

   import os
   value = safe_eval("remove('file')", locals=dict(remove=os.remove))


