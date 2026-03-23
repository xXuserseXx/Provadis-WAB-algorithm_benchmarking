Author @Justus Redlin

This is the algorithm benchmarking tool I developed for my WAB in Programming.

Main functionality includes:

Generation of datasets for usage on the algorithms that are to be tested.
Implemented datasets include:
-random permutation of n numbers
-reveresed sorted list of n numbers
-list with n numbers, with varying degrees of presortedness, specifics can be defined. accuracy of presortedness level decreases with higher specification (percentage of swaps is defined)
-list with n entries, limited with m inputs, leading to a potential higher degree of duplicate values.

List data structure, that tracks number of changes to/ operations on the list for benchmarking