import unittest

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt

from sky_map import sky_plot


class SkyPlotLegendTests(unittest.TestCase):
    def test_legend_keeps_hidden_planets(self):
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        labels = ['Earth', 'Jupiter']
        colors = ['lightseagreen', 'peru']
        alt_az = np.array([
            [0.5, 0.2],
            [-0.8, 1.1],
        ])

        sky_plot(
            system=None,
            labels=labels,
            colors=colors,
            legend=True,
            alt_az=alt_az,
            ax=ax,
        )

        legend_labels = [text.get_text() for text in ax.get_legend().get_texts()]
        self.assertIn('Jupiter', legend_labels)


if __name__ == '__main__':
    unittest.main()
