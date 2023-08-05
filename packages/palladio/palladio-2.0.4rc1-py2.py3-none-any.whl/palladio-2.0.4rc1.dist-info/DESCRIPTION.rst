# palladio
ParALleL frAmework for moDel selectIOn


### Welcome to PALLADIO.
PALLADIO is a machine learning framework whose purpose is to provide robust and reproducible results when dealing with data where the signal to noise ratio is low; it also provides tools to determine whether the dataset being analyzed contains any signal at all.
PALLADIO works by repeating the same experiment many times, each time resampling the training and the test set so that the outcome is reliable as it is not determined by a single partition of the dataset. Besides, using permutation tests, a measure of how much experiments produce a reliable result is provided.
Since all experiments performed are independent, PALLADIO is designed so that it can exploit a cluster where it is available.

### Dependencies
PALLADIO is developed using Python 2.7 and inherits its main functionalities from:
* numpy
* scipy
* scikit-learn
* mpi4py
* matplotlib
* seaborn

### Authors and Contributors
Current developers: Matteo Barbieri (@matteobarbieri), Samuele Fiorini (@samuelefiorini) and Federico Tomasi (@fdtomasi).


### Support or Contact
Having trouble with PALLADIO? Check out our [documentation](http://slipguru.github.io/palladio/) or contact us:
* matteo [dot] barbieri [at] dibris [dot] unige [dot] it
* samuele [dot] fiorini [at] dibris [dot] unige [dot] it
* federico [dot] tomasi [at] dibris [dot] unige [dot] it


