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

__all__ = ["CptIsrTask", "CptIsrTaskConfig"]

import lsst.pex.config as pexConfig
import lsst.pipe.base as pipeBase
import lsst.pipe.base.connectionTypes as cT

from lsst.ip.isr import IsrTask, IsrTaskConfig
from lsst.ip.isr.isrTask import IsrTaskConnections


class CptIsrTaskConnections(IsrTaskConnections,
                            dimensions=("instrument", "exposure", "detector")):
    ccdExposure = cT.Input(
        name="raw",
        doc="Input exposure to process.",
        storageClass="Exposure",
        dimensions=["instrument", "exposure", "detector"],
    )
    camera = cT.PrerequisiteInput(
        name="camera",
        storageClass="Camera",
        doc="Input camera to construct complete exposures.",
        dimensions=["instrument"],
        isCalibration=True,
    )

    crosstalk = cT.Input(
        name="crosstalk",
        doc="Input crosstalk object",
        storageClass="CrosstalkCalib",
        dimensions=["instrument", "detector"],
        isCalibration=True,
    )
    crosstalkSources = cT.Input(
        # This has had the lookupFunction disabled, and will not function.
        name="isrOverscanCorrected",
        doc="Overscan corrected input images.",
        storageClass="Exposure",
        dimensions=["instrument", "exposure", "detector"],
        deferLoad=True,
        multiple=True,
    )
    bias = cT.Input(
        name="bias",
        doc="Input bias calibration.",
        storageClass="ExposureF",
        dimensions=["instrument", "detector"],
        isCalibration=True,
    )
    dark = cT.Input(
        name='dark',
        doc="Input dark calibration.",
        storageClass="ExposureF",
        dimensions=["instrument", "detector"],
        isCalibration=True,
    )
    flat = cT.Input(
        name="flat",
        doc="Input flat calibration.",
        storageClass="ExposureF",
        dimensions=["instrument", "physical_filter", "detector"],
        isCalibration=True,
    )
    ptc = cT.Input(
        name="ptc",
        doc="Input Photon Transfer Curve dataset",
        storageClass="PhotonTransferCurveDataset",
        dimensions=["instrument", "detector"],
        isCalibration=True,
    )
    fringes = cT.Input(
        name="fringe",
        doc="Input fringe calibration.",
        storageClass="ExposureF",
        dimensions=["instrument", "physical_filter", "detector"],
        isCalibration=True,
    )
    strayLightData = cT.Input(
        name='yBackground',
        doc="Input stray light calibration.",
        storageClass="StrayLightData",
        dimensions=["instrument", "physical_filter", "detector"],
        deferLoad=True,
        isCalibration=True,
    )
    bfKernel = cT.Input(
        name='bfKernel',
        doc="Input brighter-fatter kernel.",
        storageClass="NumpyArray",
        dimensions=["instrument"],
        isCalibration=True,
    )
    newBFKernel = cT.Input(
        name='brighterFatterKernel',
        doc="Newer complete kernel + gain solutions.",
        storageClass="BrighterFatterKernel",
        dimensions=["instrument", "detector"],
        isCalibration=True,
    )
    defects = cT.Input(
        name='defects',
        doc="Input defect tables.",
        storageClass="Defects",
        dimensions=["instrument", "detector"],
        isCalibration=True,
    )
    linearizer = cT.Input(
        name='linearizer',
        storageClass="Linearizer",
        doc="Linearity correction calibration.",
        dimensions=["instrument", "detector"],
        isCalibration=True,
    )
    opticsTransmission = cT.Input(
        name="transmission_optics",
        storageClass="TransmissionCurve",
        doc="Transmission curve due to the optics.",
        dimensions=["instrument"],
        isCalibration=True,
    )
    filterTransmission = cT.Input(
        name="transmission_filter",
        storageClass="TransmissionCurve",
        doc="Transmission curve due to the filter.",
        dimensions=["instrument", "physical_filter"],
        isCalibration=True,
    )
    sensorTransmission = cT.Input(
        name="transmission_sensor",
        storageClass="TransmissionCurve",
        doc="Transmission curve due to the sensor.",
        dimensions=["instrument", "detector"],
        isCalibration=True,
    )
    atmosphereTransmission = cT.Input(
        name="transmission_atmosphere",
        storageClass="TransmissionCurve",
        doc="Transmission curve due to the atmosphere.",
        dimensions=["instrument"],
        isCalibration=True,
    )
    illumMaskedImage = cT.Input(
        name="illum",
        doc="Input illumination correction.",
        storageClass="MaskedImageF",
        dimensions=["instrument", "physical_filter", "detector"],
        isCalibration=True,
    )

    outputExposure = cT.Output(
        name='postISRCCD',
        doc="Output ISR processed exposure.",
        storageClass="Exposure",
        dimensions=["instrument", "exposure", "detector"],
    )
    preInterpExposure = cT.Output(
        name='preInterpISRCCD',
        doc="Output ISR processed exposure, with pixels left uninterpolated.",
        storageClass="ExposureF",
        dimensions=["instrument", "exposure", "detector"],
    )
    outputOssThumbnail = cT.Output(
        name="OssThumb",
        doc="Output Overscan-subtracted thumbnail image.",
        storageClass="Thumbnail",
        dimensions=["instrument", "exposure", "detector"],
    )
    outputFlattenedThumbnail = cT.Output(
        name="FlattenedThumb",
        doc="Output flat-corrected thumbnail image.",
        storageClass="Thumbnail",
        dimensions=["instrument", "exposure", "detector"],
    )

    def __init__(self, *, config=None):
        super().__init__(config=config)

        if config.doBias is not True:
            self.inputs.remove("bias")
        if config.doLinearize is not True:
            self.inputs.remove("linearizer")
        if config.doCrosstalk is not True:
            self.inputs.remove("crosstalkSources")
            self.inputs.remove("crosstalk")
        if config.doBrighterFatter is not True:
            self.inputs.remove("bfKernel")
            self.inputs.remove("newBFKernel")
        if config.doDefect is not True:
            self.inputs.remove("defects")
        if config.doDark is not True:
            self.inputs.remove("dark")
        if config.doFlat is not True:
            self.inputs.remove("flat")
        if config.doFringe is not True:
            self.inputs.remove("fringes")
        if config.doStrayLight is not True:
            self.inputs.remove("strayLightData")
        if config.usePtcGains is not True and config.usePtcReadNoise is not True:
            self.inputs.remove("ptc")
        if config.doAttachTransmissionCurve is not True:
            self.inputs.remove("opticsTransmission")
            self.inputs.remove("filterTransmission")
            self.inputs.remove("sensorTransmission")
            self.inputs.remove("atmosphereTransmission")
        else:
            if config.doUseOpticsTransmission is not True:
                self.inputs.remove("opticsTransmission")
            if config.doUseFilterTransmission is not True:
                self.inputs.remove("filterTransmission")
            if config.doUseSensorTransmission is not True:
                self.inputs.remove("sensorTransmission")
            if config.doUseAtmosphereTransmission is not True:
                self.inputs.remove("atmosphereTransmission")
        if config.doIlluminationCorrection is not True:
            self.inputs.remove("illumMaskedImage")

        if config.doWrite is not True:
            self.outputs.remove("outputExposure")
            self.outputs.remove("preInterpExposure")
            self.outputs.remove("outputFlattenedThumbnail")
            self.outputs.remove("outputOssThumbnail")
        if config.doSaveInterpPixels is not True:
            if "preInterpExposure" in self.outputs:
                self.outputs.remove("preInterpExposure")
        if config.qa.doThumbnailOss is not True:
            if "outputOssThumbnail" in self.outputs:
                self.outputs.remove("outputOssThumbnail")
        if config.qa.doThumbnailFlattened is not True:
            if "outputFlattenedThumbnail" in self.outputs:
                self.outputs.remove("outputFlattenedThumbnail")


class CptIsrTaskConfig(IsrTaskConfig,
                       pipelineConnections=CptIsrTaskConnections):
    """Alternate no-prerequisite input ISR Config.

    Regular processing should not use this task.
    """

    expectedExposureType = pexConfig.Field(
        dtype=str,
        doc="Type of exposures that should be processed.",
        default="",
    )


class CptIsrTask(IsrTask):
    """Alternate no-prerequisite input ISR Task.

    Regular processing should not use this task.
    """

    ConfigClass = CptIsrTaskConfig
    _DefaultName = "cptIsrTask"

    def runQuantum(self, butlerQC, inputRefs, outputRefs):
        if self.config.expectedExposureType != "":
            inputExp = butlerQC.get(inputRefs['ccdExposure'])

            if inputExp.getMetadata().get('IMGTYPE', 'UNKNOWN') != self.config.expectedExposureType:
                raise pipeBase.NoWorkFound("Input exposure is not requested type.")

        super().runQuantum(butlerQC, inputRefs, outputRefs)
