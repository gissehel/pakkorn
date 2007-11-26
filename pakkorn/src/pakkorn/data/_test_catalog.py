import unittest
from pakkorn.data import Package
from pakkorn.data import Catalog
from pakkorn.data._test_package import get_test_package

class TestCatalog(unittest.TestCase) :
    def test_creation(self) :
        catalog = Catalog()
        self.assertNotEqual(catalog,None)

    def test_empty(self) :
        catalog = Catalog()

        self.assertEqual(len(catalog),0)
        
        
    def test_simple(self) :
        catalog = Catalog()
        package = get_test_package()

        self.assertEqual(len(catalog),0)
        self.assertEqual('poide' in catalog,False)

        catalog.add_package(package)
        self.assertEqual(len(catalog),1)
        self.assertEqual('poide' in catalog,True)
        
        self.assertEqual(catalog[0],package)
        
    def test_multi(self) :
        catalog = Catalog()
        package1 = get_test_package()
        package2 = get_test_package()

        package1.set_idproj('rubu')
        package2.set_idproj('ognak')

        self.assertEqual(len(catalog),0)
        self.assertEqual('rubu' in catalog,False)
        self.assertEqual('ognak' in catalog,False)

        catalog.add_package(package1)
        catalog.add_package(package2)
        self.assertEqual(len(catalog),2)
        self.assertEqual('rubu' in catalog,True)
        self.assertEqual('ognak' in catalog,True)
        self.assertEqual(catalog[0],package1)
        self.assertEqual(catalog[1],package2)
        self.assertNotEqual(catalog[0],package2)
        self.assertNotEqual(catalog[1],package1)

    def test_concat(self) :
        catalog1 = Catalog()
        package11 = get_test_package()
        package12 = get_test_package()

        catalog2 = Catalog()
        package21 = get_test_package()
        package22 = get_test_package()

        package11.set_idproj('rubu')
        package12.set_idproj('ognak')

        package21.set_idproj('shra')
        package22.set_idproj('boo')

        catalog1.add_package(package11)
        catalog1.add_package(package12)

        catalog2.add_package(package21)
        catalog2.add_package(package22)

        self.assertEqual('rubu' in catalog1,True)
        self.assertEqual('ognak' in catalog1,True)
        self.assertEqual('shra' in catalog1,False)
        self.assertEqual('boo' in catalog1,False)
        self.assertEqual('meer' in catalog1,False)

        self.assertEqual('rubu' in catalog2,False)
        self.assertEqual('ognak' in catalog2,False)
        self.assertEqual('shra' in catalog2,True)
        self.assertEqual('boo' in catalog2,True)
        self.assertEqual('meer' in catalog2,False)
        
        catalog2 += catalog1

        self.assertEqual('rubu' in catalog1,True)
        self.assertEqual('ognak' in catalog1,True)
        self.assertEqual('shra' in catalog1,False)
        self.assertEqual('boo' in catalog1,False)
        self.assertEqual('meer' in catalog1,False)

        self.assertEqual('rubu' in catalog2,True)
        self.assertEqual('ognak' in catalog2,True)
        self.assertEqual('shra' in catalog2,True)
        self.assertEqual('boo' in catalog2,True)
        self.assertEqual('meer' in catalog2,False)
        
    def test_iter_idproj(self) :
        catalog = Catalog()
        package1 = get_test_package()
        package2 = get_test_package()
        package3 = get_test_package()
        package4 = get_test_package()

        package1.set_idproj('rubu')
        package2.set_idproj('ognak')
        package3.set_idproj('rubu')
        package4.set_idproj('boo')

        package1.set_version('1.2.8')
        package2.set_version('1.2.9')
        package3.set_version('1.2.10')
        package4.set_version('1.2.11')
        
        catalog.add_package(package1)
        catalog.add_package(package2)
        catalog.add_package(package3)
        catalog.add_package(package4)

        self.assertEqual(len(list(catalog.iter_idproj('rubu'))),2)
        self.assertEqual(len(list(catalog.iter_idproj('ognak'))),1)
        self.assertEqual(len(list(catalog.iter_idproj('boo'))),1)
        self.assertEqual(len(list(catalog.iter_idproj('shra'))),0)
        self.assertEqual(len(list(catalog.iter_idproj('meer'))),0)
        
        (package_rubu1,package_rubu2) = catalog.iter_idproj('rubu')
        
        self.assertEqual(package_rubu1.get_version(),'1.2.8')
        self.assertEqual(package_rubu2.get_version(),'1.2.10')
        
        self.assertEqual(list(catalog.iter_idprojs()),['boo','ognak','rubu'])


if __name__ == '__main__':
    unittest.main()

