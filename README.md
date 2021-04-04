# process-tensorboard-logs

* read all files from a folder
* filter them down to tensorboard log event files
* read these files and turn them into pandas data frames
* smooth the data with exponential moving average (as tensorboard would)
* turn multiple seeds of experiments into an IQR
* plot the IQR with errorbands in matplotlib

## folder_scanner.py
Takes a top-level directory such as logs/. It is assumed that logs/ contains subfolders for each figure that should be created. Each figure directory contains potentially multiple different experiments that should be collected in the same figure. Each experiment contains multiple seeds, which are combined via IQR.

logs
—DQN
——Baseline
———Seed 1
———Seed ...
——Eps Scheduling
———Seed 1
———Seed ...
—PPO
——Baseline
———Seed 1
———Seed ..,
——Non-Stationary
———Seed 1
———Seed ...
