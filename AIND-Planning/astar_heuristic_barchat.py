"""
========
Barchart
========

A bar plot with errorbars and height labels on individual bars
"""
import numpy as np
import matplotlib.pyplot as plt

N = 6

## Problem 1
#h_Ignore_Precond = (41, 43, 170, 6, 0.0490, 1)
## Problem 2
#h_Ignore_Precond = (1450, 1452, 13303, 9, 5.8320, 1)
#h_Ignore_Precond = (1450, 1452, 1500, 9, 5.8320, 1) ## Use 1500 foir better plotting
## Problem 3
#h_Ignore_Precond = (5040, 5042, 44944, 12, 19.5117 , 1)
h_Ignore_Precond = (5040, 5042, 5000, 12, 19.5117 , 1)
#men_std = (2, 3, 4, 1, 2, 1)

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
#rects1 = ax.bar(ind, h_Ignore_Precond, width, color='r', yerr=men_std)
rects1 = ax.bar(ind, h_Ignore_Precond, width, color='r')

## Problem 1
#h_pg_levelSum = (11, 13, 50, 6, 1.3554, 1)
## Problem 2
#h_pg_levelSum = (86, 88, 841, 9, 217.1781 , 1)
## Problem 3
h_pg_levelSum = (318, 320, 2934, 12, 1382.5094 , 1)
#women_std = (3, 5, 2, 3, 3)

#rects2 = ax.bar(ind + width, h-pg-levelSum, width, color='y', yerr=women_std)
rects2 = ax.bar(ind + width, h_pg_levelSum, width, color='g')

# add some text for labels, title and axes ticks
ax.set_ylabel('Scores')
ax.set_xlabel('Performance Metrics')
#ax.set_title('A* Search Algorithm Heuristics Problem 1')
#ax.set_title('A* Search Algorithm Heuristics Problem 2')
ax.set_title('A* Search Algorithm Heuristics Problem 3')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('Expansions', 'Goal Tests', 'New Nodes', 'Plan Length', 'Time Elapsed(s)', 'Optimal'))

ax.legend((rects1[0], rects2[0]), ('H-Ignore-Precond', 'H_PG_LevelSum'))


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.show()