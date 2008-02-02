import unittest
from pakkorn.data import Catalog
from pakkorn.data._test_package import get_test_package
from pakkorn.dataxml import Xml

from pakkorn.test.testutils import TestCase

class TestXml(TestCase) :
    class_dir_prefix = [__module__]
    class_test_prefix = []
    def test_write_package(self) :
        self.set_test_path('test_write_package')
        package = get_test_package()

        xml = Xml(filename=self.get_full_test_path('package.pakkorn'))
        xml.write(package)
        self.assertFileIsReference('package.pakkorn')

    def test_write_catalog(self) :
        self.set_test_path('test_write_catalog')

        package = get_test_package()

        catalog = Catalog()
        catalog.add_package(package)
        package = get_test_package()
        package.set_idproj('grut')
        catalog.add_package(package)
        
        
        xml = Xml(filename=self.get_full_test_path('catalog.pakkorn'))
        xml.write(catalog)
        
        self.assertFileIsReference('catalog.pakkorn')

        
        xml = Xml(filename=self.get_full_test_path('catalog-internals.pakkorn'),internals=True)
        xml.write(catalog)
        
        self.assertFileIsReference('catalog-internals.pakkorn')

        
        xml = Xml(filename=self.get_full_test_path('catalog-internals-bis.pakkorn'),internals=True)
        package.set_internal(name='test',value='grut')
        xml.write(catalog)
        
        self.assertFileIsReference('catalog-internals-bis.pakkorn')

    def test_write_package_change(self) :
        self.set_test_path('test_write_package_change')
        package = get_test_package()

        package.del_icon('32x32')
        xml = Xml(filename=self.get_full_test_path('package.pakkorn'))
        xml.write(package)
        self.assertFileIsReference('package.pakkorn')

    def test_read_package(self) :
        self.set_test_path('test_read_package')

        package = get_test_package()

        xml = Xml(filename=self.get_full_test_path('package.pakkorn',test_prefix='test_write_package'))
        xml.write(package)
        self.assertFileIsReference('package.pakkorn',test_prefix='test_write_package')

        xml = Xml(filename=self.get_full_test_path('package.pakkorn',test_prefix='test_write_package'))
        package = xml.read()

        xml = Xml(filename=self.get_full_test_path('package.pakkorn'))
        xml.write(package)
        self.assertFileIsReference('package.pakkorn')

    def test_read_package_internals(self) :
        self.set_test_path('test_read_package_internals')
        package = get_test_package()
        package.set_internal(name='test',value='grut')

        xml = Xml(filename=self.get_full_test_path('package.pakkorn'),internals=True)
        xml.write(package)
        self.assertFileIsReference('package.pakkorn')

        xml = Xml(filename=self.get_full_test_path('package.pakkorn'),internals=True)
        package = xml.read()
        self.assertEqual(package.has_internals(),True)

        xml = Xml(filename=self.get_full_test_path('package.pakkorn'),internals=False)
        package = xml.read()
        self.assertEqual(package.has_internals(),False)
