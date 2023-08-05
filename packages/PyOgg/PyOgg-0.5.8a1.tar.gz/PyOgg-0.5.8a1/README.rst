=====
PyOgg
=====

PyOgg provides bindings for Xiph.org's OGG Vorbis and OGG Opus audio file formats.

It requires the OGG library (e.g. libogg.dll) and at least either OGG Opus' libraries (e.g. libopus.dll, libopusfile.dll) and / or OGG Vorbis' libraries (e.g. libvorbis.dll, libvorbisfile.dll) 
to support Opus and Vorbis respectively, or the FLAC C library (e.g. libFLAC.dll) for FLAC support.

All the functions, structures and datatypes are the same as in the C++ implementation, except for some that couldn't be translated.
If you want to use them natively you will have to use ctypes' data types.
Please refer to the official documentation and the C++ headers.

You can import the various functions from pyogg.ogg, pyogg.vorbis, pyogg.opus and pyogg.flac or use the predefined classes and functions from pyogg.

PyOgg is not capable of playing files, however, you can use OpenAL for normal or even 3D playback with `PyOpenAL <https://pypi.org/project/PyOpenAL>`_.

Currently FLAC is available purely in form of bindings, because I haven't managed to load a file yet myself (o )~(o ) ...

You can find a reference on `GitHub <https://github.com/Zuzu-Typ/PyOgg>`_
