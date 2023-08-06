=================
Purpose
=================

SPOTPY is a Python tool that enables the use of Computational optimization techniques for calibration, uncertainty 
and sensitivity analysis techniques of almost every (environmental-) model. The package is puplished in the open source journal PLoS One

Houska, T, Kraft, P, Chamorro-Chavez, A and Breuer, L; `SPOTting Model Parameters Using a Ready-Made Python Package`_; PLoS ONE; 2015

The simplicity and flexibility enables the use and test of different 
algorithms without the need of complex codes::

	sampler = spotpy.algorithms.sceua(model_setup())     # Initialize your model with a setup file
	sampler.sample(10000)                                # Run the model
	results = sampler.getdata()                          # Load the results
	spotpy.analyser.plot_parametertrace(results)         # Show the results


=================
Features
=================

Complex algorithms bring complex tasks to link them with a model. 
We want to make this task as easy as possible. 
Some features you can use with the SPOTPY package are:

* Fitting models to evaluation data with different algorithms. 
  Available algorithms are: 
  
  * Monte Carlo (`MC`)
  * Markov-Chain Monte-Carlo (`MCMC`)
  * Maximum Likelihood Estimation (`MLE`)
  * Latin-Hypercube Sampling (`LHS`) 
  * Simulated Annealing (`SA`)
  * Shuffled Complex Evolution Algorithm (`SCE-UA`)
  * Differential Evolution Adaptive Metropolis Algorithm (`DE-MCz`) 
  * RObust Parameter Estimation (`ROPE`).
  * Fourier Amplitude Sensitivity Test (`FAST`)
  * Artificial Bee Colony (`ABC`)
  * Fitness Scaled Chaotic Artificial Bee Colony (`FSCABC`)

* Wide range of objective functions (also known as loss function, fitness function or energy function) to validate the sampled results. Available functions are

  * Bias
  * Procentual Bias (`PBias`)
  * Nash-Sutcliff (`NSE`)
  * logarithmic Nash-Sutcliff (`logNSE`)
  * logarithmic probability (`logp`)
  * Correlation Coefficient (`r`)
  * Coefficient of Determination (`r^2`)
  * Mean Squared Error (`MSE`)
  * Root Mean Squared Error (`RMSE`)
  * Mean Absolute Error (`MAE`)
  * Relative Root Mean Squared Error (`RRMSE`)
  * Agreement Index (`AI`)
  * Covariance, Decomposed MSE (`dMSE`)
  * Kling-Gupta Efficiency (`KGE`).

* Prebuild parameter distribution functions: 

  * Uniform
  * Normal
  * logNormal
  * Chisquare
  * Exponential
  * Gamma
  * Wald
  * Weilbull

* Wide range to adapt algorithms to perform uncertainty-, sensitivity analysis or calibration
  of a model.

* Multi-objective support
 
* MPI support for fast parallel computing

* A progress bar monitoring the sampling loops. Enables you to plan your coffee brakes.

* Use of NumPy functions as often as possible. This makes your coffee brakes short.

* Different databases solutions: `ram` storage for fast sampling a simple , `csv` tables
  the save solution for long duration samplings.

* Automatic best run selecting and plotting

* Parameter trace plotting

* Parameter interaction plot including the Gaussian-kde function

* Regression analysis between simulation and evaluation data

* Posterior distribution plot

* Convergence diagnostics with Gelman-Rubin and the Geweke plot

=================
Install
=================

Installing SPOTPY is easy. Just use:

	pip install spotpy

Or, after downloading the source code and making sure python is in your path:

	python setup.py install
	
=================
Support
=================

* Feel free to contact the authors of this tool for any support questions.

* Please contact the authors in case of any bug.

* If you use this package for a scientific research paper, please cite SPOTPY.

* Patches/enhancements and any other contributions to this package are very welcome!

* GitHub: https://github.com/thouska/spotpy


=================
Getting started
=================

Have a look at https://github.com/thouska/spotpy/tree/master/spotpy/examples and http://fb09-pasig.umwelt.uni-giessen.de/spotpy/Tutorial/2-Rosenbrock/


.. _parameter example tutorial: http://fb09-pasig.umwelt.uni-giessen.de/spotpy/Tutorial/6-Advanced_hints/#sampling-from-a-given-parameter-list
.. _parameter example code: https://github.com/thouska/spotpy/blob/master/spotpy/examples/tutorial_Parameterlist_iterator.py
.. _database example tutorial: http://fb09-pasig.umwelt.uni-giessen.de/spotpy/Tutorial/6-Advanced_hints/#create-a-own-database
.. _database example code: https://github.com/thouska/spotpy/blob/master/spotpy/examples/tutorial_ownDatabase.py
.. _SPOTting Model Parameters Using a Ready-Made Python Package: http://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0145180