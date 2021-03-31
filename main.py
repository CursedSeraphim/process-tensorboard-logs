from create_plots import create_plot

paths = ['colab_DQN_infinite_horizon_JBW-continuous-1e5-v4', 'colab_PPO_infinite_horizon_JBW-continuous-1e5-v4', 'colab_A2C_infinite_horizon_JBW-continuous-1e5-v4', 'colab_PPO_infinite_horizon_JBW-v2']
base_path = 'logs'
legend_labels = ["DQN","PPO","A2C","PPO Baseline"]
tags = ['rollout/ep_rew_mean'] * len(paths)
save_dir = 'plot.png'

create_plot(paths, legend_labels, tags, save_dir, base_path)