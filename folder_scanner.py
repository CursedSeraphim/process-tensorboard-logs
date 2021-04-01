import os
from iqr_plotter import create_plots
import argparse

###############
# arg parsing #
###############

parser = argparse.ArgumentParser(description='Scan folder and create IQR plots for tb event files')
parser.add_argument('--logs_dir', default='logs',
                    help='each first level subdirectory within this logs_dir is used to create 1 plot consisting of the aggregated logs of all second level subdirectories within')
parser.add_argument('--save_dir', default='plots',
                    help='directory to store matplotlib .png files')

args = parser.parse_args()

# 'plots/' and 'plots' should both be accepted
logs_dir = args.logs_dir+'/'
logs_dir.replace('//','/')
save_dir = args.save_dir+'/'
save_dir.replace('//','/')

#########################################
# process parameters for creating plots #
#########################################

base = next(os.walk(logs_dir))[1]

paths = []

for i in range(len(base)):
    paths.append([])
    paths[i] = [base[i] + '/' + b for b in next(os.walk(logs_dir+base[i]))[1]]

legend_labels = paths
save_dirs = [save_dir+b for b in base]
tags = [ ['rollout/ep_rew_mean' for p in b] for b in paths]
base_paths = [logs_dir for b in base]

################
# create plots #
################

create_plots(paths=paths, legend_labels=legend_labels, tags=tags, save_dirs=save_dirs, base_paths=base_paths)