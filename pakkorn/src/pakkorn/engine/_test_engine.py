import unittest
from pakkorn.engine import Engine

class TestEngine(unittest.TestCase) :
    def test_creation(self) :
        # TODO : Don't put "None" as argument of Engine (config)
        engine = Engine(None)
        self.assertNotEqual(engine,None)
