import unittest
import os
import pathlib
import json
import pydracodec
import pydracodec.dracodec_unity
import ctypes


def get_bufferview_bytes(gltf_path: pathlib.Path, gltf, bufferview_index: int) -> bytes:
    match gltf['bufferViews'][bufferview_index]:
        case {
            'buffer': buffer_index,
            'byteOffset': offset,
            'byteLength': length,

        }:
            match gltf['buffers'][buffer_index]:
                case {'uri': uri}:
                    path = gltf_path.parent / uri
                    data = path.read_bytes()
                    return data[offset:offset+length]

    raise Exception()


class TestDraco(unittest.TestCase):

    def test_upper(self):
        dir = os.environ['GLTF_SAMPLE_MODELS']
        path = pathlib.Path(dir) / '2.0/Avocado/glTF-Draco/Avocado.gltf'
        self.assertTrue(path.exists())
        gltf = json.loads(path.read_bytes())

        mesh0 = gltf['meshes'][0]
        prim0_0 = mesh0['primitives'][0]

        match prim0_0:
            case {'extensions': {'KHR_draco_mesh_compression': {'bufferView': bufferview_index, 'attributes': attributes}}}:
                data = get_bufferview_bytes(path, gltf, bufferview_index)
                with pydracodec.DecodeMesh(data) as mesh:
                    # print(f'{mesh.numFaces}')
                    indices = pydracodec.GetIndices(mesh, mesh.numFaces)
                    self.assertEqual(ctypes.c_uint, indices.element_type)

                    # print(f'{mesh.numVertices}')
                    # print(f'{mesh.numAttributes}')
                    for k, v in attributes.items():
                        match k:
                            case 'POSITION':
                                positions = pydracodec.GetAttribute(
                                    mesh, pydracodec.dracodec_unity.AttributeType.POSITION, mesh.numVertices)
                                self.assertEqual(3, positions.element_count)

                            case 'NORMAL':
                                normals = pydracodec.GetAttribute(
                                    mesh, pydracodec.dracodec_unity.AttributeType.NORMAL, mesh.numVertices)
                                self.assertEqual(3, normals.element_count)

                            case 'TEXCOORD_0':
                                uv = pydracodec.GetAttribute(
                                    mesh, pydracodec.dracodec_unity.AttributeType.TEX_COORD, mesh.numVertices)
                                self.assertEqual(2, uv.element_count)

                            case 'TANGENT':
                                pass

                            case _:
                                raise Exception()

            case _:
                raise Exception()


if __name__ == '__main__':
    unittest.main()
