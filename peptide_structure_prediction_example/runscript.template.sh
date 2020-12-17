# Edit the script below and replace:
# - <processes_to_run> with the number of processes to launch (typically the number of cores on your compute node(s)).
# - <path_to_Rosetta> with the path to your Rosetta installation.
# - .linuxgccrelease with whatever is appropriate for your operating system, compiler, and compilation mode (e.g. .macosclangrelease).
nohup mpirun -np <processes_to_run> <path_to_Rosetta>/Rosetta/main/source/bin/simple_cycpep_predict.mpiserialization.linuxgccrelease @inputs/rosetta.flags >out.log 2>err.log &
