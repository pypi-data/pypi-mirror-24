import tempfile
import unittest
import os

import shutil
import zipfile


class TestCheckForRadiationInputInDemandScript(unittest.TestCase):
    """
    Tests to make sure the demand script raises a `ValueError` if applied to a reference case that does not have
    the radiation script output.

    This fixes the issue #222
    """

    @classmethod
    def setUpClass(cls):
        """
        Create a copy of the ninecubes reference case in the temp folder. The ninecubes reference case is
        in the `../examples` folder as a zip file (`ninecubes.zip`) and has to be extracted first.
        """
        ninecubes_src = os.path.join(os.path.dirname(__file__), '..', 'examples', 'ninecubes.zip')
        ninecubes_dst = os.path.join(tempfile.gettempdir(), 'ninecubes.zip')
        shutil.copyfile(ninecubes_src, ninecubes_dst)
        archive = zipfile.ZipFile(ninecubes_dst)
        archive.extractall(os.path.join(tempfile.gettempdir(), 'ninecubes'))

    @classmethod
    def tearDownClass(cls):
        """delete the ninecubes stuff from the temp directory"""
        os.remove(os.path.join(tempfile.gettempdir(), 'ninecubes.zip'))
        shutil.rmtree(os.path.join(tempfile.gettempdir(), 'ninecubes'))

    def test_ninecubes_copied(self):
        """sanity check on `setUpClass`"""
        self.assertTrue(os.path.exists(os.path.join(tempfile.gettempdir(), 'ninecubes.zip')))
        self.assertTrue(os.path.exists(os.path.join(tempfile.gettempdir(), 'ninecubes')))

    def test_demand_checks_radiation_script(self):
        import cea.inputlocator
        import cea.demand.demand_main
        import cea.globalvar

        locator = cea.inputlocator.InputLocator(os.path.join(tempfile.gettempdir(), 'ninecubes', 'nine cubes'))
        if os.path.exists(locator.get_radiation()):
            # scenario contains radiation.csv, remove it for test
            os.remove(locator.get_radiation())
        if os.path.exists(locator.get_surface_properties()):
            # scenario contains properties_surfaces.csv, remove it for test
            os.remove(locator.get_surface_properties())
        gv = cea.globalvar.GlobalVariables()
        weather_path = locator.get_weather('Zug')
        self.assertRaises(ValueError, cea.demand.demand_main.demand_calculation, locator=locator,
                          weather_path=weather_path, gv=gv)
