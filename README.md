# process-tensorboard-logs

* read all files from a folder
* filter them down to tensorboard log event files
* read these files and turn them into pandas data frames
* smooth the data with exponential moving average (as tensorboard would)
* turn multiple seeds of experiments into an IQR
* plot the IQR with errorbands in matplotlib
