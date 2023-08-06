bio-pm
======

.. image:: https://img.shields.io/pypi/v/bio-pm.svg
    :target: https://pypi.python.org/pypi/bio-pm
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/ekeyme/bio-pm.png
   :target: https://travis-ci.org/ekeyme/bio-pm
   :alt: Latest Travis CI build status

A point mutation analyzing tool for nucleotide sequence

Installation
------------

Install through pip::

    pip install bio-pm

Or manually (assuming all required modules are installed on your system)::

    python ./setup.py install


Requirements
^^^^^^^^^^^^

* Python >= 3
* biopython

Examples
--------

Analyze point mutation status using ``pm.analyze(seq, stdseq, translate=True)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    >>> import pm
    >>> 
    >>> seq_with_gap = 'ATGGGCG-C'
    >>> pm.analyze(seq_with_gap, stdseq)
    <pm.status.NA object with: gaps=1, nt_pm=1, aa_pm=0, stdseq='ATGGGCGC'>
    >>> 

Quickly compare between ``pm.status`` objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``p.status`` objects with same stdseqs have their internal order. That is ``Y > Conserved >
PM > NA``.

.. code-block:: python

    >>> import pm
    >>>
    >>> stdseq = "ATGGGCGCT"
    >>> seq_without_pm = 'ATGGGCGCT'
    >>> seq_conserved = "ATGGGCGCC"
    >>> seq_with_pm = 'ATGGGCGAT'
    >>> status_Y = pm.analyze(seq_without_pm, stdseq)
    >>> status_Conserved = pm.analyze(seq_conserved, stdseq)
    >>> status_PM = pm.analyze(seq_with_pm, stdseq)
    >>>
    >>> status_Y > status_Conserved > status_PM
    True
    >>>

Help generate HGVS-like mutation format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Codes continues from* ``Quickly compare the point mutation status objects``

.. code-block:: python

    >>> from pm.pattern import mutant_to_str
    >>>
    >>> status_PM.pattern
    <pm.pattern.TranslatedPattern object at 0x2b03c9cfdc18>
    >>>
    >>> for nt_pm, aa_pm in status_PM.pattern.list():
    ...     print(mutant_to_str(*nt_pm) + '|' + mutant_to_str(*aa_pm))
    ...
    8C>A|3A>D

Licence
-------

MIT licensed. See the bundled `LICENSE <https://github.com/ekeyme/bio-pm/blob/master/LICENSE>`_ file for more details.

Authors
-------

`bio-pm` was written by `Ekeyme Mo <ekeyme@gmail.com>`_.
