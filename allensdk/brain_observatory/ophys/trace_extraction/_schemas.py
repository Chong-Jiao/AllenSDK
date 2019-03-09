from marshmallow import RAISE, ValidationError

from argschema import ArgSchema, ArgSchemaParser
from argschema.schemas import DefaultSchema
from argschema.fields import LogLevel, String, Nested, Boolean, Float, List, Integer

from allensdk.brain_observatory.argschema_utilities import check_read_access, check_write_access, RaisingSchema


class MotionBorder(RaisingSchema):
    x0 = Float(default=0.0, description='') # TODO: be really certain about how these relate to physical space and then write it here
    x1 = Float(default=0.0, description='')
    y0 = Float(default=0.0, description='')
    y1 = Float(default=0.0, description='')


class Roi(RaisingSchema):
    mask = List(List(Boolean), required=True, description='raster mask')
    y = Integer(required=True, description='y position (pixels) of mask\'s bounding box')
    x = Integer(required=True, description='x position (pixels) of mask\'s bounding box')
    width = Integer(required=True, description='width (pixels)of mask\'s bounding box')
    height = Integer(required=True, description='height (pixels) of mask\'s bounding box')
    valid = Boolean(default=True, description='Is this Roi known to be valid?')
    id = Integer(required=True, description='unique integer identifier for this Roi')
    mask_page = Integer(default=-1, description='') # TODO: this isn't in the examples I'm looking at. What is it?


# TODO this is in the example input json's I'm looking at, but does not seem to be used
class Image(RaisingSchema):
    width = Integer(required=True, description='width (pixels) of the whole field of view')
    height = Integer(required=True, description='height (pixels) of the whole field of view')


class InputSchema(ArgSchema):
    class Meta:
        unknown=RAISE
    log_level = LogLevel(default='INFO', description='set the logging level of the module')
    motion_border = Nested(MotionBorder, required=True, description='border widths - pixels outside the border are considered invalid')
    storage_directory = String(required=True, description='used to set output directory')
    motion_corrected_stack = String(required=True, description='path to h5 file containing motion corrected image stack')
    rois = Nested(Roi, many=True, description='specifications of individual regions of interest')
    image = Nested(Image, required=True, description='parameters describing the field of view')
    log_0 = String(required=True, description='path to motion correction output csv') # TODO: is this redundant with motion border?


class OutputSchema(RaisingSchema):
    neuropil_trace_file = String(required=True, description='path to output h5 file containing neuropil traces') # TODO rename these to _path
    roi_trace_file = String(required=True, description='path to output h5 file containing roi traces')
    
    