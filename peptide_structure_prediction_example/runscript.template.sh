# Edit the script below and replace:
# - <processes_to_run> with the number of processes to launch (typically the number of cores on your compute node(s)).
# - <path_to_Rosetta> with the path to your Rosetta installation.
# - .linuxgccrelease with whatever is appropriate for your operating system, compiler, and compilation mode (e.g. .macosclangrelease).
# Note that the nohup command and the ampersand will allow this app to run in the background, with output logs written to out.log and err.log.
# The nohup command, ampersand, and output logs can be omitted for foreground runs with output to the terminal, but closing the terminal will
# terminate execution in this case (whereas it won't with nohup).
nohup mpirun -np <processes_to_run> <path_to_Rosetta>/Rosetta/main/source/bin/simple_cycpep_predict.mpiserialization.linuxgccrelease @inputs/rosetta.flags >out.log 2>err.log &
