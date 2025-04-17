import collections
import math

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

import ipywidgets as widgets
from ipywidgets import interact

PlotComponents = collections.namedtuple(
    "PlotComponents", ["ax", "pcd_text", "pfa_text"]
)

def plot_continuous_geq_threshold(x, f0, f1, get_threshold, get_pcd, interactive):
    def plot_pdfs(ax, alpha=None):
        if alpha is None:
            ax.set_title("Neyman-Pearson")
        else:
            ax.set_title(f"Neyman-Pearson, alpha={np.around(alpha, decimals=3)}")
            
        ax.plot(x, f0, color="red", label="H0")
        ax.plot(x, f1, color="blue", label="H1")
        
        ax.set_xlabel("x")
        ax.xaxis.set_label_coords(0.5, -0.02)
        ax.set_ylabel("P(X = x)")
        
        pcd_text = ax.text(-4, 0.37, "PCA: ")
        pfa_text = ax.text(-4, 0.34, "PFA: ")
        
        ax.legend()
        return PlotComponents(ax, pcd_text, pfa_text)

    def color_acceptance_regions(plot_components, alpha):
        threshold = get_threshold(alpha)
        pcd = get_pcd(threshold)
        plot_components.ax.fill_between(
            x, 0, f0, where = ([True] * 100), color = "white", alpha = 1
        )
        plot_components.ax.fill_between(
            x, 0, f1, where = ([True] * 100), color = "white", alpha = 1
        )
        plot_components.ax.fill_between(
            x, 0, f0, where = (x > threshold), color = "red", alpha = 0.3
        )
        plot_components.ax.fill_between(
            x, 0, f1, where = (x > threshold), color = "blue", alpha = 0.3
        )
        plot_components.pcd_text.set_text("PCD: {}".format(np.around(pcd, decimals = 4)))
        plot_components.pfa_text.set_text("PFA: {}".format(np.around(alpha, decimals = 4)))

    if interactive:
        fig, (ax1) = plt.subplots(1)
        plot_components = plot_pdfs(ax1)
        plt.show()

        @interact(alpha = widgets.FloatSlider(
            min = 0, max = 1, step = 0.025, value = 0.05, readout_format = '.3f'
        ))
        def update_figure(alpha):
            color_acceptance_regions(plot_components, alpha)
            plt.draw()

    else:
        nrows = 7
        ncols = 3
        fig, axs = plt.subplots(nrows = nrows, ncols = ncols)
        fig.set_size_inches(6 * ncols, 4 * nrows, forward=True)

        for i in range(nrows * ncols):
            r, c = i // ncols, i % ncols
            alpha = i / (nrows * ncols - 1)
            plot_components = plot_pdfs(axs[r, c], alpha=alpha)
            color_acceptance_regions(plot_components, alpha)
        plt.tight_layout()
        plt.show()

BarChartComponents = collections.namedtuple(
    "BarChartComponents", ["ax", "bars0", "bars1", "pcd_text", "pfa_text"]
)

def plot_discrete(x, p0, p1, get_rejection_probs, interactive):

    def plot_bar_charts(ax, alpha = None):
        bar_width = 0.3
        background_bars0 = ax.bar(
            x - bar_width / 2,
            p0,
            bar_width,
            color="#FFE9E9",
            edgecolor="black",
        )
        background_bars1 = ax.bar(
            x + bar_width / 2,
            p1,
            bar_width,
            color="#E9FFFE",
            edgecolor="black",
        )
        bars0 = ax.bar(
            x - bar_width / 2,
            0.0,
            bar_width,
            color="red",
            label="H0",
        )
        bars1 = ax.bar(
            x + bar_width / 2,
            0.0,
            bar_width,
            color="blue",
            linestyle="-",
            label="H1",
        )
        
        if alpha is None:
            ax.set_title("Neyman-Pearson")
        else:
            ax.set_title(f"Neyman-Pearson, alpha={np.around(alpha, decimals=3)}")
            
        ax.set_xticks(x)
        ax.set_xlabel("x")
        ax.xaxis.set_label_coords(0.45, -0.02)
        ax.set_ylabel("P(X = x)")
        
        height = max(max(p0), max(p1))
        pcd_text = ax.text(x[0]-0.3, height * 0.95, "PCD: ")
        pfa_text = ax.text(x[0]-0.3, height * 0.9, "PFA: ")
        
        ax.legend()
        return BarChartComponents(ax, bars0, bars1, pcd_text, pfa_text)

    def color_acceptance_regions(alpha, chart_components):
        rejection_probs = get_rejection_probs(alpha)
        # List of PCD, given each possible data value.
        pcd = p1 * rejection_probs
        # List of PFA, given each possible data value.
        pfa = p0 * rejection_probs

        # Updates total PCD and PFA.
        chart_components.pcd_text.set_text(
            "PCD: {}".format(np.around(sum(pcd), decimals=4))
        )
        chart_components.pfa_text.set_text(
            "PFA: {}".format(np.around(sum(pfa), decimals=4))
        )

        # Updates the bars.
        for i in range(len(x)):
            chart_components.bars0[i].set_height(pfa[i])
            chart_components.bars1[i].set_height(pcd[i])

    if interactive:
        fig, (ax1) = plt.subplots(1)
        chart = plot_bar_charts(ax1)
        plt.show()

        @interact(alpha = widgets.FloatSlider(
            min = 0, max = 1, step = 0.025, value = 0.05, readout_format = '.3f'
        ))
        def update_figure(alpha):
            color_acceptance_regions(alpha, chart)
            plt.draw()

    else:
        nrows = 7
        ncols = 3
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols)
        fig.set_size_inches(6 * ncols, 4 * nrows, forward=True)

        for i in range(nrows * ncols):
            r, c = i // ncols, i % ncols
            alpha = i / (nrows * ncols - 1)
            chart_components = plot_bar_charts(axs[r, c], alpha)
            color_acceptance_regions(alpha, chart_components)
        plt.tight_layout()
        plt.show()
