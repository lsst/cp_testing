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


class CptIsrTaskConnections(pipeBase.PipelineTaskConnections,
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

        if not config.doBias:
            del self.bias
        if not config.doLinearize:
            del self.linearizer
        if not config.doCrosstalk:
            del self.crosstalkSources
            del self.crosstalk
        if not config.doBrighterFatter:
            del self.bfKernel
            del self.newBFKernel
        if not config.doDefect:
            del self.defects
        if not config.doDark:
            del self.dark
        if not config.doFlat:
            del self.flat
        if not config.doFringe:
            del self.fringes
        if not config.doStrayLight:
            del self.strayLightData
        if not config.usePtcGains and not config.usePtcReadNoise:
            del self.ptc
        if not config.doAttachTransmissionCurve:
            del self.opticsTransmission
            del self.filterTransmission
            del self.sensorTransmission
            del self.atmosphereTransmission
        else:
            if not config.doUseOpticsTransmission:
                del self.opticsTransmission
            if not config.doUseFilterTransmission:
                del self.filterTransmission
            if not config.doUseSensorTransmission:
                del self.sensorTransmission
            if not config.doUseAtmosphereTransmission:
                del self.atmosphereTransmission
        if not config.doIlluminationCorrection:
            del self.illumMaskedImage

        if not config.doWrite:
            del self.outputExposure
            del self.preInterpExposure
            del self.outputFlattenedThumbnail
            del self.outputOssThumbnail
        if not config.doSaveInterpPixels:
            if "preInterpExposure" in self.outputs:
                del self.preInterpExposure
        if not config.qa.doThumbnailOss:
            if "outputOssThumbnail" in self.outputs:
                del self.outputOssThumbnail
        if not config.qa.doThumbnailFlattened:
            if "outputFlattenedThumbnail" in self.outputs:
                del self.outputFlattenedThumbnail

    def adjustQuantum(self, inputs, outputs, label, data_id):
        """Adjust quantum to drop task execution depending on the input data.

        Parameters
        ----------
        inputs : `dict`
            Dictionary of input connections.
        outputs : `Mapping`
            Mapping of output datasets.
        label : `str`
            Task label.
        data_id : `lsst.daf.butler.DataCoordinate`
            Data id for this task execution.

        Returns
        -------
        adjustedInputs : `Mapping`
            Adjusted set of inputs.
        adjustedOutputs : `Mapping`
            Adjusted set of outputs.

        Raises
        ------
        NoWorkFound
            Raised if the task execution should be skipped.
        """
        inputConnection, inputExpRefs = inputs['ccdExposure']
        inputExpRef = inputExpRefs[0]
        doWork = True

        if self.config.expectedExposureType != "":
            expected = self.config.expectedExposureType.lower()
            observationType = inputExpRef.dataId.exposure.observation_type
            if observationType != expected:
                doWork = False

        if self.config.expectedObservationReason != "":
            expected = self.config.expectedObservationReason.lower()
            observationReason = inputExpRef.dataId.exposure.observation_reason
            if observationReason != expected:
                doWork = False

        if not doWork:
            raise pipeBase.NoWorkFound("Input exposure is not requested type.")
        else:
            return super().adjustQuantum(inputs, outputs, label, data_id)


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
    expectedObservationReason = pexConfig.Field(
        dtype=str,
        doc="Further restrict processed exposures by observation_reason.",
        default="",
    )


class CptIsrTask(IsrTask):
    """Alternate no-prerequisite input ISR Task.

    Regular processing should not use this task.
    """

    ConfigClass = CptIsrTaskConfig
    _DefaultName = "cptIsrTask"

    pass
