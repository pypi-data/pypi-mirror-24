==========
pyliveleak
==========


.. image:: https://img.shields.io/pypi/v/pyliveleak.svg
        :target: https://pypi.python.org/pypi/pyliveleak

.. image:: https://img.shields.io/travis/mpenkov/pyliveleak.svg
        :target: https://travis-ci.org/mpenkov/pyliveleak

.. image:: https://readthedocs.org/projects/pyliveleak/badge/?version=latest
        :target: https://pyliveleak.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/mpenkov/pyliveleak/shield.svg
     :target: https://pyup.io/repos/github/mpenkov/pyliveleak/
     :alt: Updates


Uploads videos to liveleak.com


* Free software: MIT license
* Documentation: https://pyliveleak.readthedocs.io.


Features
--------

Sample usage::

    $ pyliveleak --path tests/test-data/foreman_cif.mp4 --username "$username" --password "$password"
    https://www.liveleak.com/view?i=7ed_1502358506

For additional options::

    $ pyliveleak --help
    Usage: pyliveleak [OPTIONS]

      Console script for pyliveleak.

    Options:
      --loglevel INTEGER
      --password TEXT     Your liveleak.com password  [required]
      --username TEXT     Your liveleak.com username  [required]
      --path PATH         The video to upload  [required]
      --help              Show this message and exit.

You may also use pyliveleak as a Python library::

    >>> import pyliveleak
    >>> index_page = pyliveleak.login(username, password)
    >>> file_token, item_token = index_page.add_item('tests/test-data/foreman_cif.mp4')
    >>> item_token
    u'b86_1502357642'

Your new video will be available here: https://www.liveleak.com/view?i={item_token}

You may specify optional metadata::

    >>> index_page.add_item('tests/test-data/foreman_cif.mp4', title='my title',
                            body='detailed description', tags='tags', category='World News')

The category must be one of::

    >>> pprint.pprint(sorted(pyliveleak.CATEGORIES))
    ['afghanistan',
     'citizen journalism',
     'conspiracy',
     'creative',
     'history',
     'hobbies',
     'iran',
     'iraq',
     'liveleak challenges',
     'liveleaks',
     'music',
     'nature',
     'other',
     'other entertainment',
     'other items from liveleakers',
     'other middle east',
     'other news',
     'politics',
     'propaganda',
     'regional news',
     'religion',
     'science and technology',
     'sports',
     'syria',
     'ukraine',
     'vehicles',
     'weapons',
     'world news',
     'wtf',
     'yawn',
     'your say']

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
