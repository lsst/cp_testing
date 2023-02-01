# This file is part of cp_testing.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
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
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__all__ = ["CptBrighterFatterKernelSolveTask", "CptBrighterFatterKernelSolveConfig",
           "CptLinearitySolveTask", "CptLinearitySolveConfig",
           "CptPhotodiodeCorrectionTask", "CptPhotodiodeCorrectionConfig",
           ]


import lsst.cp.pipe as cpPipe
import lsst.pipe.base as pipeBase
import lsst.pipe.base.connectionTypes as cT


class CptBrighterFatterKernelSolveConnections(pipeBase.PipelineTaskConnections,
                                              dimensions=("instrument", "detector")):
    dummy = cT.Input(
        name="raw",
        doc="Dummy exposure.",
        storageClass='Exposure',
        dimensions=("instrument", "exposure", "detector"),
        multiple=True,
        deferLoad=True,
    )
    camera = cT.PrerequisiteInput(
        name="camera",
        doc="Camera Geometry definition.",
        storageClass="Camera",
        dimensions=("instrument", ),
        isCalibration=True,
        lookupFunction=cpPipe._lookupStaticCalibration.lookupStaticCalibration,
    )
    inputPtc = cT.Input(
        name="cptPtc",
        doc="Input PTC dataset.",
        storageClass="PhotonTransferCurveDataset",
        dimensions=("instrument", "detector"),
        isCalibration=True,
    )

    outputBFK = cT.Output(
        name="cptBrighterFatterKernel",
        doc="Output measured brighter-fatter kernel.",
        storageClass="BrighterFatterKernel",
        dimensions=("instrument", "detector"),
        isCalibration=True,
    )


class CptBrighterFatterKernelSolveConfig(cpPipe.BrighterFatterKernelSolveConfig,
                                         pipelineConnections=CptBrighterFatterKernelSolveConnections):
    pass


class CptBrighterFatterKernelSolveTask(cpPipe.BrighterFatterKernelSolveTask):

    ConfigClass = CptBrighterFatterKernelSolveConfig
    _DefaultName = "cptBfkTask"

    pass


class CptLinearitySolveConnections(pipeBase.PipelineTaskConnections,
                                   dimensions=("instrument", "detector")):
    dummy = cT.Input(
        name="raw",
        doc="Dummy exposure.",
        storageClass='Exposure',
        dimensions=("instrument", "exposure", "detector"),
        multiple=True,
        deferLoad=True,
    )
    camera = cT.PrerequisiteInput(
        name="camera",
        doc="Camera Geometry definition.",
        storageClass="Camera",
        dimensions=("instrument", ),
        isCalibration=True,
        lookupFunction=cpPipe._lookupStaticCalibration.lookupStaticCalibration,
    )
    inputPtc = cT.Input(
        name="ptc",
        doc="Input PTC dataset.",
        storageClass="PhotonTransferCurveDataset",
        dimensions=("instrument", "detector"),
        isCalibration=True,
    )
    inputPhotodiodeData = cT.PrerequisiteInput(
        name="photodiode",
        doc="Photodiode readings data.",
        storageClass="IsrCalib",
        dimensions=("instrument", "exposure"),
        multiple=True,
        deferLoad=True,
        minimum=0,
    )
    inputPhotodiodeCorrection = cT.Input(
        name="pdCorrection",
        doc="Input photodiode correction.",
        storageClass="IsrCalib",
        dimensions=("instrument", ),
        isCalibration=True,
    )

    outputLinearizer = cT.Output(
        name="cptLinearity",
        doc="Output linearity measurements.",
        storageClass="Linearizer",
        dimensions=("instrument", "detector"),
        isCalibration=True,
    )

    def __init__(self, *, config=None):
        super().__init__(config=config)

        if config.applyPhotodiodeCorrection is not True:
            self.inputs.discard("inputPhotodiodeCorrection")

        if config.usePhotodiode is not True:
            self.inputs.discard("inputPhotodiodeData")


class CptLinearitySolveConfig(cpPipe.LinearitySolveConfig,
                              pipelineConnections=CptLinearitySolveConnections):
    pass


class CptLinearitySolveTask(cpPipe.LinearitySolveTask):

    ConfigClass = CptLinearitySolveConfig
    _DefaultName = "cptLinearityTask"

    pass


class CptPhotodiodeCorrectionConnections(pipeBase.PipelineTaskConnections,
                                         dimensions=("instrument", "detector")):
    inputPtc = cT.Input(
        name="ptc",
        doc="Input PTC dataset.",
        storageClass="PhotonTransferCurveDataset",
        dimensions=("instrument", "detector"),
        isCalibration=True,
    )


class CptPhotodiodeCorrectionConfig(cpPipe.PhotodiodeCorrectionConfig,
                                    pipelineConnections=CptPhotodiodeCorrectionConnections):
    pass


class CptPhotodiodeCorrectionTask(cpPipe.PhotodiodeCorrectionTask):

    ConfigClass = CptPhotodiodeCorrectionConfig
    _DefaultName = "cptPdCorrTask"

    pass
