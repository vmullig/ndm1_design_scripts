# This script should be run from your Rosetta/main/source/ directory.  Replace <number_of_processes> with
# the number of parallel processes to use for compilation (typically, the number of cores on the node on
# which you are compiling).  Rosetta takes several core-hours to compile from scratch, so splitting this
# over many cores will speed things up considerably.
./scons.py -j <number_of_processes> mode=release extras=mpi,serialization simple_cycpep_predict 
