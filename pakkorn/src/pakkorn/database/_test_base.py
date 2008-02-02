import os

from pakkorn.data import Package
from pakkorn.data import Catalog
from pakkorn.data import MultiFilters

from pakkorn.test.testutils import get_test_full_path
from pakkorn.test.testutils import TestCase

from pakkorn.data._test_package import get_test_package

class TestDatabase(TestCase) :
    DatabaseClass = None
    class_dir_prefix = [__module__]

    def test_search_1(self) :
        self.set_test_path('test-search-1',use_dir=True,clean=True)

        package1 = get_test_package()
        package2 = get_test_package()
        package3 = get_test_package()
        package4 = get_test_package()
        
        package1.set_idproj('spam')
        package2.set_idproj('egg')
        package3.set_idproj('bacon')
        package4.set_idproj('egg')
        
        package1.set_version('3.6.8')
        package2.set_version('5.2rc3')
        package3.set_version('1.9')
        package4.set_version('5.1')

        package1.set_fullname('Lovely Spam')
        package2.set_fullname('With Egg')
        package3.set_fullname('And Bacon')
        package4.set_fullname('And Egg')

        catalog = Catalog(packages=[package1,package2,package3,package4])

        database = self.DatabaseClass(self.get_full_test_path())
        database.update(catalog)

        self.assertEqual(len(list(database.search(version='1.9'))),1)
        self.assertEqual(len(list(database.search(substring='egg'))),2)
        self.assertEqual(len(list(database.search(substring='And'))),2)
        self.assertEqual(len(list(database.search(substring='with'))),1)
        self.assertEqual(len(list(database.search(fullname='With Eg'))),1)
        self.assertEqual(len(list(database.search(fullname='With Egg'))),1)
        self.assertEqual(len(list(database.search(idproj='eg'))),0)
        self.assertEqual(len(list(database.search(idproj='egg'))),2)
        self.assertEqual(len(list(database.search(idproj='spam'))),1)
        self.assertEqual(len(list(database.search(idproj='bacon'))),1)
        self.assertEqual(len(list(database.search(idproj='egg',version='5.1'))),1)
        self.assertEqual(len(list(database.search(_idproj='non-existant-idproj'))),4)
        self.assertEqual(len(list(database.search(_idproj='bacon'))),3)
        self.assertEqual(len(list(database.search(_idproj='egg'))),2)

        multifilters = MultiFilters(idproj='egg',version='5.1')
        self.assertEqual(len(list(database.search(multifilters))),1)

        multifilters = MultiFilters(idproj='egg',version='5.1')
        multifilters.define_new_set(idproj='bacon')
        self.assertEqual(len(list(database.search(multifilters))),2)

        multifilters = MultiFilters(idproj='egg')
        multifilters.define_new_set(version='1.9')
        self.assertEqual(len(list(database.search(multifilters))),3)

        multifilters = MultiFilters(idproj='egg')
        multifilters.define_new_set(version='5.1')
        self.assertEqual(len(list(database.search(multifilters))),2)

        multifilters = MultiFilters(substring='with')
        multifilters.define_new_set(_substring='bacon')
        self.assertEqual(len(list(database.search(multifilters))),3)
        self.assertEqual(len(list(database.search())),4)

    def test_search_2(self) :
        self.set_test_path('test_search_2',use_dir=True,clean=True)

        package1 = get_test_package()
        package2 = get_test_package()
        package3 = get_test_package()
        package4 = get_test_package()
        package5 = get_test_package()

        package1.set_idproj('spam')
        package2.set_idproj('egg')
        package3.set_idproj('bacon')
        package4.set_idproj('egg')
        package5.set_idproj('egg')

        package1.set_version('3.6.8')
        package2.set_version('5.2rc3')
        package3.set_version('1.9')
        package4.set_version('5.1')
        package5.set_version('5.2rc3')

        package1.set_fullname('Lovely Spam')
        package2.set_fullname('With Egg')
        package3.set_fullname('And Bacon')
        package4.set_fullname('And Egg')
        package5.set_fullname('Tim')

        catalog = Catalog(packages=[package1,package2,package3,package4,package5])
       
        database = self.DatabaseClass(self.get_full_test_path())
        database.update(catalog)

        self.assertEqual(len(list(database.search(fullname='With Egg'))),0)
        self.assertEqual(len(list(database.search(idproj='egg',version='5.2rc3'))),1)




