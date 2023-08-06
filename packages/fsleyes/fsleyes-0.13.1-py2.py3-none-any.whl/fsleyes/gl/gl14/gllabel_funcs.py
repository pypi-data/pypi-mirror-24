#!/usr/bin/env python
#
# gllabel_funcs.py - OpenGL 1.4 functions used by the GLLabel class.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module provides functions which are used by the :class:`.GLLabel`
class to render :class:`.Image` overlays in an OpenGL 1.4 compatible manner.


Rendering of a ``GLLabel`` is very similar to that of a :class:`.GLVolume`,
with the exception that a different fragment program (``gllabel``) is used.
Therefore, the ``preDraw``, ``draw``, ``drawAll`` and ``postDraw`` functions
defined in the :mod:`.gl14.glvolume_funcs` are re-used by this module.
"""


import numpy              as np

import fsleyes.gl.shaders as shaders
from . import                glvolume_funcs


def init(self):
    """Calls the :func:`compileShaders` and :func:`updateShaderState`
    functions.
    """

    self.shader = None

    compileShaders(   self)
    updateShaderState(self)


def destroy(self):
    """Deletes handles to the vertex/fragment shader programs. """
    self.shader.destroy()
    self.shader = None


def compileShaders(self):
    """Loads vertex and fragment shader program source, and creates an
    :class:`.ARBPShader` instance.
    """
    if self.shader is not None:
        self.shader.destroy()

    vertSrc  = shaders.getVertexShader(  'glvolume')
    fragSrc  = shaders.getFragmentShader('gllabel')
    textures = {
        'imageTexture' : 0,
        'lutTexture'   : 1,
    }

    self.shader = shaders.ARBPShader(vertSrc,
                                     fragSrc,
                                     shaders.getShaderDir(),
                                     textures)


def updateShaderState(self):
    """Updates all shader program variables. """

    if not self.ready():
        return

    opts = self.opts

    self.shader.load()

    voxValXform  = self.imageTexture.voxValXform
    voxValXform  = [voxValXform[0, 0], voxValXform[0, 3], 0, 0]
    offsets      = opts.outlineWidth / \
                   np.array(self.image.shape[:3], dtype=np.float32)
    invNumLabels = 1.0 / (opts.lut.max() + 1)

    minOffset = offsets.min()
    offsets   = np.array([minOffset] * 3)

    if opts.outline: offsets = [1] + list(offsets)
    else:            offsets = [0] + list(offsets)

    self.shader.setFragParam('voxValXform',  voxValXform)
    self.shader.setFragParam('invNumLabels', [invNumLabels, 0, 0, 0])
    self.shader.setFragParam('outline',      offsets)

    self.shader.unload()

    return True


preDraw  = glvolume_funcs.preDraw
draw2D   = glvolume_funcs.draw2D
draw3D   = glvolume_funcs.draw3D
drawAll  = glvolume_funcs.drawAll
postDraw = glvolume_funcs.postDraw
