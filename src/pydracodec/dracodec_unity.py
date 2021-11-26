'''
https://github.com/google/draco/blob/e5eb9cd3f7e77f5c9a5dbbbb45a1f44a7db41e9d/unity/DracoMeshLoader.cs
'''
import ctypes
from enum import IntEnum


class DataType(IntEnum):
    '''
    These values must be exactly the same as the values in draco_types.h.
    Attribute data type.
    '''
    DT_INVALID = 0
    DT_INT8 = 1
    DT_UINT8 = 2
    DT_INT16 = 3
    DT_UINT16 = 4
    DT_INT32 = 5
    DT_UINT32 = 6
    DT_INT64 = 7
    DT_UINT64 = 8
    DT_FLOAT32 = 9
    DT_FLOAT64 = 10
    DT_BOOL = 11


class AttributeType(IntEnum):
    '''
    These values must be exactly the same as the values in
    geometry_attribute.h.
    Attribute type.
    '''
    INVALID = -1
    POSITION = 0
    NORMAL = 1
    COLOR = 2
    TEX_COORD = 3
    # A special id used to mark attributes that are not assigned to any known
    # predefined use case. Such attributes are often used for a shader specific
    # data.
    GENERIC = 4


class DracoData(ctypes.Structure):
    '''
    The order must be consistent with C++ interface.
    '''
    _fields_ = [
        ('dataType', ctypes.c_int),
        ('data', ctypes.c_void_p),
    ]


class DracoAttribute(ctypes.Structure):
    _fields_ = [
        ('attributeType', ctypes.c_int),
        ('dataType', ctypes.c_int),
        ('numComponents', ctypes.c_int),
        ('uniqueId', ctypes.c_int),
    ]


class DracoMesh(ctypes.Structure):
    _fields_ = [
        ('numFaces', ctypes.c_int),
        ('numVertices', ctypes.c_int),
        ('numAttributes', ctypes.c_int),
    ]


DLL = ctypes.cdll.dracodec_unity

# Release data associated with DracoMesh.
ReleaseDracoMesh = DLL.ReleaseDracoMesh
ReleaseDracoMesh.argtypes = [ctypes.POINTER(ctypes.POINTER(DracoMesh))]

# Release data associated with DracoAttribute.
ReleaseDracoAttribute = DLL.ReleaseDracoAttribute
ReleaseDracoAttribute.argtypes = [
    ctypes.POINTER(ctypes.POINTER(DracoAttribute))]

# Release attribute data.
ReleaseDracoData = DLL.ReleaseDracoData
ReleaseDracoData.argtypes = [ctypes.POINTER(ctypes.POINTER(DracoData))]

# Decodes compressed Draco::Mesh in buffer to mesh. On input, mesh
DecodeDracoMesh = DLL.DecodeDracoMesh
DecodeDracoMesh.restype = ctypes.c_int
DecodeDracoMesh.argtypes = [ctypes.c_void_p,
                            ctypes.c_int, ctypes.POINTER(ctypes.POINTER(DracoMesh))]

# Returns the DracoAttribute at index in mesh. On input, attribute must be
# null. The returned attr must be released with ReleaseDracoAttribute.
GetAttribute = DLL.GetAttribute
GetAttribute.restype = ctypes.c_bool
GetAttribute.argtypes = [ctypes.POINTER(
    DracoMesh), ctypes.c_int, ctypes.POINTER(ctypes.POINTER(DracoAttribute))]

# Returns the DracoAttribute of type at index in mesh. On input, attribute
# must be null. E.g. If the mesh has two texture coordinates then
# GetAttributeByType(mesh, AttributeType.TEX_COORD, 1, & attr) will return
# the second TEX_COORD attribute. The returned attr must be released with
# ReleaseDracoAttribute.
GetAttributeByType = DLL.GetAttributeByType
GetAttributeByType.restype = ctypes.c_bool
GetAttributeByType.argtypes = [ctypes.POINTER(
    DracoMesh), ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(DracoAttribute))]

# Returns the DracoAttribute with unique_id in mesh. On input, attribute
# must be null.The returned attr must be released with
# ReleaseDracoAttribute.
GetAttributeByUniqueId = DLL.GetAttributeByUniqueId
GetAttributeByUniqueId.restype = ctypes.c_bool
GetAttributeByUniqueId.argtypes = [ctypes.POINTER(
    DracoMesh), ctypes.c_int, ctypes.POINTER(ctypes.POINTER(DracoAttribute))]

# Returns an array of indices as well as the type of data in data_type. On
# input, indices must be null. The returned indices must be released with
# ReleaseDracoData.
GetMeshIndices = DLL.GetMeshIndices
GetMeshIndices.restype = ctypes.c_bool
GetMeshIndices.argtypes = [ctypes.POINTER(
    DracoMesh), ctypes.POINTER(ctypes.POINTER(DracoData))]

# Returns an array of attribute data as well as the type of data in
# data_type. On input, data must be null. The returned data must be
# released with ReleaseDracoData.
GetAttributeData = DLL.GetAttributeData
GetAttributeData.restype = ctypes.c_bool
GetAttributeData.argtypes = [ctypes.POINTER(DracoMesh), ctypes.POINTER(
    DracoAttribute), ctypes.POINTER(ctypes.POINTER(DracoData))]
