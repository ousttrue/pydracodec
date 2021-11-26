import unittest
import os
import pathlib


class TestDraco(unittest.TestCase):

    def test_upper(self):
        dir = os.environ['GLTF_SAMPLE_MODELS']
        path = pathlib.Path(dir) / '2.0/Avocado/glTF-Draco/Avocado.gltf'
        self.assertTrue(path.exists())


if __name__ == '__main__':
    unittest.main()
