.. vim: set fileencoding=utf-8 :
.. Fri 3 Feb 11:51:35 CEST 2016

.. image:: http://img.shields.io/badge/docs-v1.0.3-yellow.png
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.paper.btas_j2016/v1.0.3/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.paper.btas_j2016/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.paper.btas_j2016/badges/v1.0.3/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.paper.btas_j2016/commits/v1.0.3
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.paper.btas_j2016
.. image:: http://img.shields.io/pypi/v/bob.paper.btas_j2016.png
   :target: https://pypi.python.org/pypi/bob.paper.btas_j2016


=====================================================
 Reproducing results of paper published in BTAS 2016
=====================================================

This package is part of the Bob_ toolkit and it allows to reproduce the following paper::

    @inproceedings{KorshunovBtas2016j,
        author = {P. Korshunov AND S. Marcel},
        title = {Joint Operation of Voice Biometrics and Presentation Attack Detection},
        year = {2016},
        month = sep,
        booktitle = {IEEE International Conference on Biometrics: Theory, Applications and Systems (BTAS)},
        address = {Niagara Falls, NY, USA},
    }

If you use this package and/or its results, please cite the paper.


Installation
------------

The installation instructions are based on conda_ and works on **Linux** and **Mac OS** systems
only `Install conda`_ before continuing.

Once you have installed conda_, download the source code of this paper and
unpack it.  Then, you can create a conda environment with the following
command::

    $ cd bob.paper.btas_j2016
    $ conda env create -f environment.yml
    $ source activate bob.paper.btas_j2016  # activate the environment
    $ python -c "import bob.bio.base"  # test the installation
    $ buildout

This will install all the required software to reproduce this paper.


Documentation
-------------
For further documentation on this package, please read the `Documentation <https://www.idiap.ch/software/bob/docs/bob/bob.paper.btas_j2016/v1.0.3/index.html>`_.
For a list of tutorials on this or the other packages of Bob_, or information on submitting issues, asking questions and starting discussions, please visit its website.

.. _bob: http://www.idiap.ch/software/bob
.. _conda: https://conda.io
.. _install conda: https://conda.io/docs/install/quick.html#linux-miniconda-install
.. _bob.bio: https://pypi.python.org/pypi/bob.bio.base