import numpy as np
import logging
from pathlib import Path
from tempfile import mkdtemp
from unittest import TestCase

from log_utils.data_logger import DataLogger

from log_utils.data_logger.contrib.plotly_converter import PlotlyConverter, PlotlyFigure
from log_utils.data_logger.handlers import SaveToDirHandler


class TestPlotlyConverter(TestCase):
    @classmethod
    def get_default_grid_settings(cls, title):
        axis = dict(showbackground=True,
                    backgroundcolor="rgb(230, 230,230)",
                    gridcolor="rgb(255, 255, 255)",
                    zerolinecolor="rgb(255, 255, 255)")

        layout = dict(
            title=title,
            font=dict(family='Balto'),
            showlegend=False,
            width=800,
            height=800,
            scene=dict(
                xaxis=axis,
                yaxis=axis,
                zaxis=axis,
                aspectratio=dict(
                    x=1,
                    y=1,
                    z=1
                )
            )
        )

        return layout

    def test_save_ones_volume(self):
        """
            Note: For nosetest: Run with --nocapture
        """

        path_dir_logs = Path(mkdtemp())
        logger = DataLogger('TestLogger', logging.DEBUG)
        logger.setLevel(logging.INFO)
        data_handler = SaveToDirHandler(path_dir_logs)
        data_handler.addConverter(PlotlyConverter())
        logger.addHandler(data_handler)

        meshes = {'i': np.array([2, 2]), 'showscale': False, 'opacity': 0.3, 'k': np.array([0, 1]),
                  'z': np.array([1., 1., 1., 1.], dtype=np.float32), 'name': '',
                  'y': np.array([0., 0., 1., 1.], dtype=np.float32),
                  'colorscale': [[0, 'rgb(6, 236, 35)'], [1.0, 'rgb(6, 236, 35)']],
                  'x': np.array([0., 1., 0., 1.], dtype=np.float32), 'type': 'mesh3d', 'j': np.array([1, 3]),
                  'reversescale': False,
                  'intensity': np.array([-0., -0.13533528, -0., -0.04978707], dtype=np.float32)
                  }
        logger.info('Temp Message', data=PlotlyFigure(data=[meshes], layout=self.get_default_grid_settings("test")))
        file_found = False
        for file in path_dir_logs.iterdir():
            if "html" in file.name:
                file_found = True
        self.assertTrue(file_found)


if __name__ == '__main__':
    TestPlotlyConverter().test_save_ones_volume()
