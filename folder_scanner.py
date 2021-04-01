import os
from iqr_plotter import create_plots

logs_dir = 'logs/'
save_base_dir = 'plots/'

base = next(os.walk(logs_dir))[1]

paths = []

for i in range(len(base)):
    paths.append([])
    paths[i] = [base[i] + '/' + b for b in next(os.walk(logs_dir+base[i]))[1]]

legend_labels = paths
save_dirs = [save_base_dir+b for b in base]
tags = [ ['rollout/ep_rew_mean' for p in b] for b in paths]
base_paths = [logs_dir for b in base]


create_plots(paths=paths, legend_labels=legend_labels, tags=tags, save_dirs=save_dirs, base_paths=base_paths)