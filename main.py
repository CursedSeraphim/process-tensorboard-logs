from iqr_plotter import create_plots


paths = []
base_paths = []
tags = []
legend_labels = []
save_dirs = []
colours = []

paths.append(['colab_PPO_infinite_horizon_JBW-continuous-1e5-v4', 'colab_PPO_infinite_horizon_JBW-v2'])
paths.append(['colab_DQN_infinite_horizon_JBW-continuous-1e5-v4', 'colab_PPO_infinite_horizon_JBW-v2'])

base_paths = ['logs'] * 2

tags = [ ['rollout/ep_rew_mean'] * len(paths) ] * 2

legend_labels.append(["PPO","PPO Baseline"])
legend_labels.append(["DQN","PPO Baseline"])

save_dirs.append('plot_1.png')
save_dirs.append('plot_2.png')

colours.append(['cyan', 'magenta'])
colours.append(None)

create_plots(paths, legend_labels, tags, save_dirs, base_paths, colours)