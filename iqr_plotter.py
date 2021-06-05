###########
# imports #
###########

from scipy.interpolate import interp1d
import numpy as np
from matplotlib import pyplot as plt
import tensorboard as tb
import tensorflow.compat.v1 as tf
from typing import List
tf.disable_v2_behavior()
import os
from glob import glob


def create_plots(paths, legend_labels, tags, save_dirs, base_paths, colours=None, xmax=int(2e6), n_samples=1000, figsize=(6,4), smoothing=0.6, titles=None):
    if titles:
        if colours:
            for (paths, legend_labels, tags, save_dir, base_path, colours, title) in zip(paths, legend_labels, tags, save_dirs, base_paths, colours, titles):
                create_plot(paths, legend_labels, tags, save_dir, base_path, colours, xmax, n_samples, figsize=figsize, smoothing=smoothing, title=title)
        else:
            for (paths, legend_labels, tags, save_dir, base_path, title) in zip(paths, legend_labels, tags, save_dirs, base_paths, titles):
                create_plot(paths, legend_labels, tags, save_dir, base_path, xmax=xmax, n_samples=n_samples, figsize=figsize, smoothing=smoothing, title=title)
    else:
        if colours:
            for (paths, legend_labels, tags, save_dir, base_path, colours) in zip(paths, legend_labels, tags, save_dirs, base_paths, colours):
                create_plot(paths, legend_labels, tags, save_dir, base_path, colours, xmax, n_samples, figsize=figsize, smoothing=smoothing)
        else:
            for (paths, legend_labels, tags, save_dir, base_path) in zip(paths, legend_labels, tags, save_dirs, base_paths):
                create_plot(paths, legend_labels, tags, save_dir, base_path, xmax=xmax, n_samples=n_samples, figsize=figsize, smoothing=smoothing)


def create_plot(paths, legend_labels, tags, save_dir, base_path="", colours=None, xmax=int(2e6), n_samples=1000, figsize=(6,4), smoothing=0.6, title=None):

    ##################################
    # path definitions and constants #
    ##################################

    paths = [base_path+'/'+p for p in paths]
    # make sure both directory strings like '//' as well as '/' are possible by replacing double by single
    paths = [s.replace('//','/') for s in paths]

    ##############
    # load files #
    ##############

    for i in range(len(paths)):
        paths[i] = [y for x in os.walk(paths[i]) for y in glob(os.path.join(x[0], '*'))]
        # filter files for tb logs
        paths[i] = [x for x in paths[i] if 'tfevents' in x]

    experiments = paths

    for i in experiments:
        for j in i:
            print(j)

    ###########################
    # load tb logs from files #
    ###########################

    ys = []

    i = 0
    for paths, tag in zip(experiments, tags):
        print('experiment',i)
        ys.append([])
        j = 0
        for path in paths:
            ys[i].append([])
            print('seed',j)
            for e in tf.compat.v1.train.summary_iterator(path):
                for v in e.summary.value:
                    if v.tag == tag:
                        ys[i][j] = ys[i][j] + [v.simple_value]
            j = j+1
        i = i+1

    #####################################################
    # filter cancelled experiments with incomplete data #
    #####################################################
    # i.e. seeds that ran for fewer steps than the max length

    # print('before filtering:')
    # for exp in ys:
    #     print([len(i) for i in exp])
    # print()

    for exp in ys:
        m = max([len(i) for i in exp])
        # print(m)
        i = 0
        for seed in exp:
            if len(seed) < m:
                exp.pop(i)
                i -= 1
            i += 1
            
    # print('after filtering:')
    # for exp in ys:
    #     print([len(i) for i in exp])

    ###################################################
    # exponential moving average smoothing definition #
    ###################################################

    def smooth(scalars: List[float], weight: float) -> List[float]:  # Weight between 0 and 1
        last = scalars[0]  # First value in the plot (first timestep)
        smoothed = list()
        for point in scalars:
            smoothed_val = last * weight + (1 - weight) * point  # Calculate smoothed value
            smoothed.append(smoothed_val)                        # Save it
            last = smoothed_val                                  # Anchor the last smoothed value

        return smoothed

    #######################################
    # find log with max num of datapoints #
    #######################################
    # different algorithm experiments might have logs at different amounts of steps, need to unify the x axis for plotting later on best before calculating iqr and applying smoothing

    # ys = [experiments, seeds, values] - use this to find largest nested sub array:
    x = [[len(j) for j in i] for i in ys]
    max_len = max(max(x))
    # print(max_len)

    #################################
    # interpolate / upsample others #
    #################################

    i = 0
    for exp in ys:
        j = 0
        for y in exp:
            if len(y) == max_len:
                continue
            x = list(range(len(y)))
            f = interp1d(x, y)
            f2 = interp1d(x, y, kind='cubic')

            xnew = np.linspace(0, len(y)-1, num=max_len, endpoint=True)

            temp = f(xnew)
            if isinstance(temp, list):
                ys[i][j] = temp
            else:
                ys[i][j] = temp.tolist()
            j = j + 1
        i = i + 1

    # filter length again
    for exp in ys:
        m = max([len(i) for i in exp])
        # print(m)
        i = 0
        for seed in exp:
            if len(seed) < m:
                exp.pop(i)
                i -= 1
            i += 1

    #################################
    # calc IQR, and apply smoothing #
    #################################

    q75s = []
    q50s = []
    q25s = []
    i = 0
    for exp in ys:
        q75s.append([])
        q50s.append([])
        q25s.append([])
        q75s[i], q50s[i], q25s[i] = np.percentile(exp, [75, 50, 25], axis=0)
        q75s[i] = smooth(q75s[i], smoothing)
        q50s[i] = smooth(q50s[i], smoothing)
        q25s[i] = smooth(q25s[i], smoothing)
        
        i = i + 1

    ###############
    # create plot #
    ###############

    plt.figure(figsize=figsize)
    # x = list(range(max_len))
    x = np.linspace(1, xmax, max_len)
    i=1
    if colours:
        for q25, q50, q75, c in zip(q25s, q50s, q75s, colours):
            plt.plot(x, q50, color=c)
            plt.fill_between(x, q25, q75, alpha=0.3, color=c)
            i = i + 1
    else:
        for q25, q50, q75 in zip(q25s, q50s, q75s):
            plt.plot(x, q50)
            plt.fill_between(x, q25, q75, alpha=0.3)
            i = i + 1
        
    plt.legend(legend_labels, loc='upper left')
    # ticks = x[0::len(x)//5]
    # ticks.append(n_samples)
    # print('n_samples:', n_samples)
    # print('TICKS:', ticks)
    # print(xmax//n_samples)
    # labels = [(xmax//n_samples) * i for i in ticks]
    # plt.xticks(ticks=ticks, labels=labels)
    plt.ylabel('Reward')
    plt.xlabel('Steps')
    if title:
        plt.title(title)
    # plt.xticks(np.arange(min(x), max(x)+1, xmax))
    # print(labels)
    plt.grid()
    plt.savefig(save_dir)

