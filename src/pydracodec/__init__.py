from . import dracodec_unity
import contextlib
import ctypes


@contextlib.contextmanager
def DecodeMesh(data: bytes):
    p = ctypes.POINTER(dracodec_unity.DracoMesh)()
    ret = dracodec_unity.DecodeDracoMesh(
        data, len(data), ctypes.pointer(p))
    if ret <= 0:
        raise Exception()
    mesh = p[0]
    try:
        yield mesh
    finally:
        dracodec_unity.ReleaseDracoMesh(ctypes.pointer(p))
