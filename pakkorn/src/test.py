#!/usr/bin/env python

import unittest
from pakkorn.data._test_package import TestPackage
from pakkorn.data._test_catalog import TestCatalog
from pakkorn.data._test_multifilters import TestMultiFilters
from pakkorn.dataxml._test_dataxml import TestXml
from pakkorn.database._test_asxml import TestDatabase as TestDatabaseAsXml
import pakkorn.engine
from pakkorn.engine._test_engine import TestEngine
from pakkorn.engine._test_webdownloader import TestWebDownloader
from clean import clean

if __name__ == '__main__':
    clean()
    unittest.main()
