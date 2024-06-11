#!/usr/bin/env python

#
# LSST Data Management System
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <https://www.lsstcorp.org/LegalNotices/>.
#
"""Test cases for cp_testing pipelines."""

import os
import unittest

from lsst.pipe.base import Pipeline, PipelineGraph
import lsst.utils

try:
    import lsst.obs.lsst
    has_obs_lsst = True
except ImportError:
    has_obs_lsst = False


class CalibrationPipelinesTestingTestCase(lsst.utils.tests.TestCase):
    """Test case for building the pipelines."""

    def setUp(self):
        self.pipeline_path = os.path.join(lsst.utils.getPackageDir("cp_testing"), "pipelines")

    def _check_pipeline(self, pipeline_file):
        # Confirm that the file is there.
        self.assertTrue(os.path.isfile(pipeline_file), msg=f"Could not find {pipeline_file}")

        # The following loads the pipeline and confirms that it can parse all
        # the configs.
        try:
            pipeline = Pipeline.fromFile(pipeline_file)
            graph = pipeline.to_graph()
        except Exception as e:
            raise RuntimeError(f"Could not process {pipeline_file}") from e

        self.assertIsInstance(graph, PipelineGraph)

    @unittest.skipIf(not has_obs_lsst, reason="Cannot test LSSTCam pipelines without obs_lsst")
    def test_lsstcam_pipelines(self):
        for pipeline in ["protocolB.yaml"]:
            self._check_pipeline(os.path.join(self.pipeline_path, pipeline))


class TestMemory(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
