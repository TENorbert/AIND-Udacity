# -*- coding: utf-8 -*-
"""
plotly
"""

import matplotlib.pyplot as plt
import numpy as np

import plotly.plotly as py
import plotly.tools as tls
## Set cridentials to use plotly
tls.set_credentials_file(username='dten', api_key='U4BttY055RMmf84dNrFh')

mpl_fig = plt.figure()
ax = mpl_fig.add_subplot(111)

N = 10.0

custom_score = (57.1, 72.9, 62.9, 60.0, 60.0, 75.7, 61.4, 64.3, 58.6, 58.6)
custom_score2 = (51.4, 67.1, 55.7, 70.0, 70.0, 57.1, 61.4, 64.3, 65.7,67.1)
custom_score3 = (58.6, 62.9, 64.3, 75.7, 62.9, 70.0, 61.4, 55.7,58.6, 64.3)



rounds = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10']
x = np.array(rounds)

ind = np.arange(1, N+1)  # the x locations for the groups
width = 0.35    # the width of the bars: can also be len(x) sequence

p1 = ax.bar(ind, custom_score, width, color=(0.2588, 0.4433, 1.0)) # color = "blue" also possible
p2 = ax.bar(ind, custom_score2, width, color=(1.0, 0.5, 0.62))
p3 = ax.bar(ind, custom_score3, width, color=(0.5, 0.35, 0.75))

ax.set_ylabel('Win Rate(%)')
ax.set_xlabel('Tournament Rounds')
ax.set_title('Heuristic Performance Comparison')

#ax.set_xticks(ind  +  width/2.)
ax.set_xticks(ind)
ax.set_xticklabels(('R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10'))
ax.set_yticks(np.arange(0, 90, 5))



plotly_fig = tls.mpl_to_plotly(mpl_fig)

## Legend
plotly_fig["layout"]["showlegend"] = True
plotly_fig["data"][0]["name"] = "Custom Score"
plotly_fig["data"][1]["name"] = "Custrom Score 2"
plotly_fig["data"][2]["name"] = "Custrom Score 3"

plot_url = py.plot(plotly_fig, filename='Heuristic_Performance_Stacked-bar-Chart')


