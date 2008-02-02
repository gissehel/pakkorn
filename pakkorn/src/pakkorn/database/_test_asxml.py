from pakkorn.data import Catalog

from pakkorn.database.asxml import Database
from pakkorn.database.asxml import LOCAL_BASE

from pakkorn.data._test_package import get_test_package
from pakkorn.database._test_base import TestDatabase as TestDatabaseBase

class TestDatabase(TestDatabaseBase) :
    DatabaseClass = Database
    class_dir_prefix = [__module__]

    def test_creation(self) :
        self.set_test_path('test_creation',use_dir=True,clean=True)

        database = self.DatabaseClass(self.get_full_test_path())
        self.assertFileIsReference(LOCAL_BASE)

    def test_update_1(self) :
        self.set_test_path('test_update_1',use_dir=True,clean=True)

        database = self.DatabaseClass(self.get_full_test_path())
        package = get_test_package()
        catalog = Catalog(packages=[package])
        database.update(catalog)

        self.assertFileIsReference(LOCAL_BASE)

        self.set_test_path('test_update_1',use_dir=True,clean=True)

        package = get_test_package()
        catalog = Catalog(packages=[package])
        database.update(catalog)

        self.assertFileIsReference(LOCAL_BASE)

    def test_update_2(self) :
        self.set_test_path('test_update_2',use_dir=True,clean=True)

        database = self.DatabaseClass(self.get_full_test_path())
        package = get_test_package()
        catalog = Catalog(packages=[package])
        database.update(catalog)

        package = get_test_package()
        package.set_version('5.1.2')
        catalog = Catalog(packages=[package])
        database.update(catalog)

        self.assertFileIsReference(LOCAL_BASE)


    def test_update_3(self) :
        self.set_test_path('test_update_3',use_dir=True,clean=True)

        database = self.DatabaseClass(self.get_full_test_path())
        package = get_test_package()
        catalog = Catalog(packages=[package])
        database.update(catalog)

        package = get_test_package()
        package.set_idproj('groin')
        package.set_version('5.1.2')
        catalog = Catalog(packages=[package])
        database.update(catalog)

        self.assertFileIsReference(LOCAL_BASE)

    def test_update_4(self) :
        self.set_test_path('test_update_4',use_dir=True,clean=True)

        database = self.DatabaseClass(self.get_full_test_path())
        package = get_test_package()
        catalog = Catalog(packages=[package])
        database.update(catalog)
        database._catalog[0].set_internal(name='installed',value='true')

        package = get_test_package()
        package.set_idproj('groin')
        package.set_version('5.1.2')
        catalog = Catalog(packages=[package])
        database.update(catalog)

        self.assertFileIsReference(LOCAL_BASE)

    def test_update_5(self) :
        self.set_test_path('test_update_5',use_dir=True,clean=True)

        database = self.DatabaseClass(self.get_full_test_path())
        package = get_test_package()
        catalog = Catalog(packages=[package])
        database.update(catalog)
        database._catalog[0].set_internal(name='installed',value='true')

        package = get_test_package()
        package.set_idproj('groin')
        package.set_version('5.1.2')
        catalog = Catalog(packages=[package])
        database.update(catalog)

        database._catalog[0].set_internal(name='installed',value='false')
        database.update(catalog)

        self.assertFileIsReference(LOCAL_BASE)
