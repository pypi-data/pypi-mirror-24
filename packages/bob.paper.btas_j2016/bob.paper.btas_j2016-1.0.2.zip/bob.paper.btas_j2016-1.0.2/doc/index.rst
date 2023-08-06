.. vim: set fileencoding=utf-8 :
.. Pavel Korshunov <pavel.korshunov@idiap.ch>
.. Thu 23 Jun 13:43:22 2016

=====================================================
 Package for paper published in BTAS 2016 on ASV-PAD 
=====================================================


If you use this package, please cite the following paper::

    @inproceedings{KorshunovBtas2016j,
        author = {P. Korshunov AND S. Marcel},
        title = {Joint Operation of Voice Biometrics and Presentation Attack Detection},
        year = {2016},
        month = sep,
        booktitle = {IEEE International Conference on Biometrics: Theory, Applications and Systems (BTAS)},
        address = {Niagara Falls, NY, USA},
    }

This package contains scripts to reproduce part of the results from the paper (other results are available directly online via BEAT_ platform). The package also provides score files for i-vector based automatic speaker verification (ASV) system, LBP-based presentation attack detection (PAD), which are used to produce the error rates and plots presented in the paper.


Reproducing results of the paper
--------------------------------

Scores of ASV and PAD systems can be found in folder `scores`. 

To create a joint ASV-PAD system, the scores can be fused using Logistic Regression classifier (as per the paper), resulting in another set of scores, by running the following:

.. code-block:: sh

    $ ./bin/fuse_asv_pad_scores.py -e scores/asv_scores -p scores/pad_scores - o fused_system

The script will generate fused scores inside the folder `fused_system`. 

To plot histograms distribution for ASV system in `licit` scenario, as presented in Figure 4a of the paper, run the following:

.. code-block:: sh

    $ ./bin/plot_asv_results.py -d scores/asv_scores/scores-dev-real -e scores/asv_scores/scores-eval-real 
        -t scores/asv_scores/scores-dev-attack -f scores/asv_scores/scores-eval-attack --scenario licit

To plot histograms distribution for ASV system in `spoof` scenario, as presented in Figure 4b of the paper, run the following:

.. code-block:: sh

    $ ./bin/plot_asv_results.py -d scores/asv_scores/scores-dev-real -e scores/asv_scores/scores-eval-real 
	-t scores/asv_scores/scores-dev-attack -f scores/asv_scores/scores-eval-attack --scenario spoof 

To plot histograms distribution for PAD system , as presented in Figure 4c of the paper, run the following:

.. code-block:: sh

    $ ./bin/plot_pad_results.py -d scores/pad_system/scores-dev-real -e scores/pad_system/scores-eval-real 
	-t scores/pad_system/scores-dev-attack -f scores/pad_system/scores-eval-attack

The script creates PDF files for DET curves, histogram distributions for dev and eval sets, and writes main statistics such as FAR, FRR, and EER into a text file.



To plot a scatter plot presented in Figure 5a of the paper, run the following:

.. code-block:: sh

    $ ./bin/plot_scatter.py -e scores/asv_scores -p scores/pad_scores

The script will generate PDF scatter plots inside `fused_score` folder for Train, Dev, and Test sets.

To plot Figure 5b and Figure 5c, please run the following

To plot a scatter plot presented in Figure 5a of the paper, run the following:

.. code-block:: sh

    $ ./bin/plot_on_demand.py scores/fused_system/scores-dev-fused-real scores/fused_system/scores-eval-fused-real 
	scores/fused_system/scores-dev-fused-attack scores/fused_system/scores-eval-fused-attack -i 7 -c eer


.. _bob: https://www.idiap.ch/software/bob
.. _BEAT: https://www.beat-eu.org/platform/
.. _AVspoof: https://www.idiap.ch/dataset/avspoof

