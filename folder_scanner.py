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
parser.add_argument('--c', default=None, nargs='+', action='append',
                    help='like --c blue red --c blue')
parser.add_argument('--xmax', default=int(2e6), type=int,
                    help='extent of x axis')
parser.add_argument('--n_samples', default=1000, type=int,
                    help='amount of samples. for each sample in a plot it will move xmax/n_samples along the x-axis')
parser.add_argument('--figsize', default=(6,4), nargs='+',
                    help='maptlotlib figsize as in (18, 12), use --figsize 18 12')
parser.add_argument('--smoothing', default=0.6, type=float,
                    help='tb like smoothing weight')
parser.add_argument('--titles', default=None, type=str, nargs='+',
                    help='plot titles like --titles plot1 plot2')

args = parser.parse_args()

args.figsize = tuple([int(i) for i in args.figsize])
print('figsize',args.figsize)

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

create_plots(paths=paths, legend_labels=legend_labels, tags=tags, save_dirs=save_dirs, base_paths=base_paths, colours=args.c, xmax=args.xmax, figsize=args.figsize, n_samples=args.n_samples, smoothing=args.smoothing, titles=args.titles)