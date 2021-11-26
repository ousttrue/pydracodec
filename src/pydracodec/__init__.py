from . import dracodec_unity
import contextlib
import ctypes
from typing import NamedTuple, Type, Optional


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


class BufferReference(NamedTuple):
    pointer: ctypes.c_void_p
    bytelength: int
    element_type: Type[ctypes._SimpleCData]
    element_count: int = 1


def GetIndices(dracoMesh: dracodec_unity.DracoMesh, faceCount: int) -> BufferReference:
    p = ctypes.POINTER(dracodec_unity.DracoData)()
    dracodec_unity.GetMeshIndices(dracoMesh, ctypes.pointer(p))
    try:
        indicesData = p[0]
        match dracodec_unity.DataType(indicesData.dataType):
            case dracodec_unity.DataType.DT_UINT16 | dracodec_unity.DataType.DT_INT16:
                return BufferReference(indicesData.data, faceCount, ctypes.c_ushort)
            case dracodec_unity.DataType.DT_INT32 | dracodec_unity.DataType.DT_INT32:
                return BufferReference(indicesData.data, faceCount, ctypes.c_uint)
            case _:
                raise Exception()
    finally:
        dracodec_unity.ReleaseDracoData(ctypes.pointer(p))


def GetAttribute(dracoMesh: dracodec_unity.DracoMesh, attr_type: dracodec_unity.AttributeType, numVertices: int) -> Optional[BufferReference]:
    ap = ctypes.POINTER(dracodec_unity.DracoAttribute)()
    if dracodec_unity.GetAttributeByType(dracoMesh, attr_type, 0, ctypes.pointer(ap)):
        try:
            attr = ap[0]
            p = ctypes.POINTER(dracodec_unity.DracoData)()

            if dracodec_unity.GetAttributeData(dracoMesh, attr, ctypes.pointer(p)):
                try:
                    posData = p[0]
                    return BufferReference(posData.data, numVertices, dracodec_unity.DataType(posData.dataType).get_type(), attr.numComponents)
                finally:
                    dracodec_unity.ReleaseDracoData(ctypes.pointer(p))
        finally:
            dracodec_unity.ReleaseDracoAttribute(ctypes.pointer(ap))
