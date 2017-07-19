"""
  Plotting Bar charts
"""


#
#import matplotlib.pyplot as plt; plt.rcdefaults()
#import numpy as np
#import statistics as stat
#import seaborn as sb
#
#
#objects = ('custom_score_3', 'custom_score_2', 'custom_score')
#
#y_pos = np.arange(len(objects))
#
##Win Rate after 10 runs
#custom_score = [57.1,72.9,62.9,60.0,60.0,75.7,61.4,64.3,58.6]
#custom_score_2 = [51.4,67.1,55.7,70.0,70.0,57.1,61.4,64.3,65.7]
#custom_score_3 = [58.6,62.9,64.3,75.7,62.9,70.0,61.4, 55.7,58.6]
#
#cs_mean = stat.mean(custom_score)
#cs2_mean = stat.mean(custom_score_2)
#cs3_mean = stat.mean(custom_score_3)
##Average win Rate after 10 Tournament Runs
##heuristic_performance = [cs3_mean, cs2_mean, cs_mean]
#
#heuristic_performance = [62.9, 67.1, 72.9]
#
#
#plt.bar(y_pos, heuristic_performance, align='center', alpha=0.5)
#plt.xticks(y_pos, objects)
#plt.ylabel('Average Win Rate(%)')
#plt.title('Heuristics Performance')
#
#plt.show()


#Bar chart with easy comparison

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns # for plotting ans styling


n_groups = 10.0

custom_score = (57.1, 72.9, 62.9, 60.0, 60.0, 75.7, 61.4, 64.3, 58.6, 58.6)
custom_score_2 = (51.4, 67.1, 55.7, 70.0, 70.0, 57.1, 61.4, 64.3, 65.7,67.1)
custom_score_3 = (58.6, 62.9, 64.3, 75.7, 62.9, 70.0, 61.4, 55.7,58.6, 64.3)

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.20

opacity  = 0.1

error_config = {'ecolor' : '0.3'}

sns.set_style("darkgrid")

#plot1 = plt.bar(index + bar_width, 
#                menMean, 
#                bar_width, 
#                alpha=opacity,
#                color = 'b',
#                yerr = menStd,
#                error_kw = error_config,
#                label = 'Men'
#                )
#                
#plot2 = plt.bar(index + bar_width, 
#                womenMean, 
#                bar_width, 
#                alpha=opacity,
#                color = 'b',
#                yerr = womenStd,
#                error_kw = error_config,
#                label = 'Women'
#                )
                
groups = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10']
x = np.array(groups)

p3 = sns.barplot(x, custom_score_2, label = "Custom Score 3",  color= "g" )
p2 = sns.barplot(x, custom_score_2, label = "Custom Score 2", color= "r" )
p1 = sns.barplot(x, custom_score, label = "Custom Score", color="b")



                
                
plt.xlabel('Tournament Rounds')
plt.ylabel('Win Rate(%)')
plt.title('Heuristic Performance Comparison')
plt.xticks(index + bar_width/2., groups)
#plt.legend()
ax.legend(ncol = 1, loc="upper right", frameon=True)
sns.despine(left=True, bottom=True)
plt.tight_layout()
plt.show()