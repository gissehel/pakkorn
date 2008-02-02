import unittest
from pakkorn.data import Package
from pakkorn.data import Commands
from pakkorn.data import ReferencableString

from itertools import izip

def get_test_package() :
        package = Package(idproj='poide')
        package.set_version(ReferencableString(string='3.3.6'))
        package.set_fullname(ReferencableString(string='The test package'))
        package.set_description(ReferencableString(string='This text contains a full description of the package\nThis is another line for the description.\nLast line.'))
        
        package.set_item('itemname',ReferencableString(string='http://poide.praf/pido/panf'))
        package.set_item('itemnameref',ReferencableString(url='http://poide.praf/pido/pluf',pattern='begin(.*?)end'))

        commands = Commands()
        commands.add_command(line='${itemname} --silent')
        commands.add_command(line='${itemnameref} --next_command_line')
        commands.add_command(line='${itemname} --end_install')
        package.set_commands('install',commands)

        commands = Commands()
        # Here 'poide_registry' is the name used in the windows registry to identify the uninstaller reference
        commands.add_command(uninstall_winname='poide_registry')
        package.set_commands('uninstall',commands)
        
        package.add_category('Test :: Test Item :: Test Catergory')
        package.add_category('Programming Language :: Python')
        package.add_category('Development Status :: 0 - Nothing')
        
        package.set_icon('16x16','http://poide.praf/pido/img/icon16.png')
        package.set_icon('32x32','http://poide.praf/pido/img/icon32.png')
        package.set_icon('64x64','http://poide.praf/pido/img/icon64.png')

        package.set_property('homepage','http://poide.praf/pido/')
        package.set_property('x-random-property','blu')

        return package

class TestPackage(unittest.TestCase) :
    def setUp(self) :
        pass

    def test_creation(self) :
        package = Package()
        self.assertNotEqual(package,None)

    def test_get_idproj(self) :
        package = Package(idproj='poide')
        self.assertEqual(package.get_idproj(),'poide')
        self.assertNotEqual(package.get_idproj(),'praf')

        self.assertEqual(package.get_version(),None)
        self.assertNotEqual(package.get_version(),'3.3.6')
        
    def test_version(self) :
        package = Package('poide')
        self.assertEqual(package.get_version(),None)
        self.assertNotEqual(package.get_version(),'3.3.6')

        package.set_version('3.3.6')

        self.assertNotEqual(package.get_version(),None)
        self.assertEqual(package.get_version(),'3.3.6')
        self.assertNotEqual(package.get_version(),'3.3.7')

    def test_generic_info(self) :
        package = get_test_package()
        
        self.assertEqual(package.get_version(),'3.3.6')
        self.assertEqual(package.get_fullname(),'The test package')
        self.assertEqual(package.get_description(),'This text contains a full description of the package\nThis is another line for the description.\nLast line.')
        
    def test_items(self) :
        package = get_test_package()
        
        self.assertEqual(package.get_item('itemname')=='http://poide.praf/pido/panf',True)
        self.assertEqual(package.get_item('itemnameref'),('http://poide.praf/pido/pluf','begin(.*?)end'))
        
    def test_commands_iter(self) :
        package = get_test_package()

        self.assertEqual(set(package.iter_commands_names()),set(('install','uninstall')))
        
    def test_commands_install(self) :
        package = get_test_package()
        
        install_commands = package.get_commands('install')
        
        for command,command_reference in izip(install_commands,('${itemname} --silent','${itemnameref} --next_command_line','${itemname} --end_install')) :
            self.assertEqual(str(command),command_reference)

    def test_commands_uninstall(self) :
        package = get_test_package()

        uninstall_commands = package.get_commands('uninstall')

        for command,command_reference in izip(uninstall_commands,('!poide_registry',)) :
            self.assertEqual(str(command),command_reference)
        
    def test_category_list(self) :
        package = get_test_package()
        
        categories = set()
        for category in package.iter_categories() :
            categories.add(category)

        self.assertEqual(categories,set(('Test :: Test Item :: Test Catergory','Programming Language :: Python','Development Status :: 0 - Nothing')))
        
    def test_category_del(self) :
        package = get_test_package()
        
        package.del_category('Programming Language :: Python')

        categories = set()
        for category in package.iter_categories() :
            categories.add(category)

        self.assertEqual(categories,set(('Test :: Test Item :: Test Catergory','Development Status :: 0 - Nothing')))

    def test_icon_get(self) :
        package = get_test_package()
        
        self.assertEqual(package.get_icon('16x16'),'http://poide.praf/pido/img/icon16.png')

    def test_icon_list(self) :
        package = get_test_package()
        
        iconsizes = set()
        for iconsize in package.iter_iconsizes() :
            iconsizes.add(iconsize)
        self.assertEqual(iconsizes,set(('16x16','32x32','64x64')))

    def test_icon_del(self) :
        package = get_test_package()
        
        package.del_icon('16x16')

        iconsizes = set()
        for iconsize in package.iter_iconsizes() :
            iconsizes.add(iconsize)
        self.assertEqual(iconsizes,set(('32x32','64x64')))

    def test_properties_get(self) :
        package = get_test_package()
        
        self.assertEqual(package.has_property('x-random-property'),True)
        self.assertEqual(package.has_property('x-non-existant-property'),False)
        self.assertEqual(package.get_property('x-random-property'),'blu')

    def test_properties_iter(self) :
        package = get_test_package()
        
        self.assertEqual(set(package.iter_properties()),set(('homepage','x-random-property')))

    def test_properties_del(self) :
        package = get_test_package()

        package.del_property('x-random-property')
        self.assertEqual(set(package.iter_properties()),set(('homepage',)))

    def test_has_internals_with_no_internal(self) :
        package = get_test_package()
        
        self.assertEqual(package.has_internals(),False)

    def test_has_internals_with_internals(self) :
        package = get_test_package()
        
        package.set_internal('test','glut')
        
        self.assertEqual(package.has_internals(),True)
        
    def test_get_internal(self) :
        package = get_test_package()
        
        package.set_internal('test','glut')
        
        self.assertEqual(package.get_internal('test'),'glut')
        self.assertNotEqual(package.get_internal('test'),'glot')
        
    def test_get_internal_2(self) :
        package = get_test_package()
        
        package.set_internal('test','glut')
        
        self.assertRaises(KeyError,package.get_internal,'tost')
        
    def test_del_internal(self) :
        package = get_test_package()

        self.assertEqual(package.has_internals(),False)
        package.set_internal('test','glut')
        self.assertEqual(package.has_internals(),True)
        self.assertRaises(KeyError,package.get_internal,'tost')
        self.assertEqual(package.has_internals(),True)
        self.assertRaises(KeyError,package.del_internal,'tost')
        self.assertEqual(package.has_internals(),True)
        package.del_internal('test')
        self.assertEqual(package.has_internals(),False)

if __name__ == '__main__':
    unittest.main()

