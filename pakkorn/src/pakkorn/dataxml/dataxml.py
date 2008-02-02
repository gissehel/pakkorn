
from xml.dom import minidom

from pakkorn.data import Catalog
from pakkorn.data import Package
from pakkorn.data import Commands
from pakkorn.data import ReferencableString

SCHEMA_VERSION = '0.3'
PAKKORN_URI_PREFIXE = 'http://action.giss.ath.cx/schema/pakkorn/'
PAKKORN_URL_PREFIXE = 'http://action.giss.ath.cx/schema/pakkorn/'
PAKKORN_SCHEMA = 'pakkorn.xsd'

PAKKORN_NS_URI = PAKKORN_URI_PREFIXE+SCHEMA_VERSION
PAKKORN_URL = PAKKORN_URL_PREFIXE+SCHEMA_VERSION
PAKKORN_SCHEMA_URL = PAKKORN_URL+'/'+PAKKORN_SCHEMA
PAKKORN_SCHEMA_LOCATION = PAKKORN_NS_URI+' '+PAKKORN_SCHEMA_URL


def filterout_textnode(nodes) :
    return filter(lambda node:node.nodeType!=node.TEXT_NODE,nodes)

def filterout_node(nodes,nodename) :
    return filter(lambda node:node.nodeName==nodename,nodes)


class ParsingError(Exception) :
    pass

class Xml(object) :
    def __init__(self,filename=None,internals=False) :
        self._filename = filename
        self._internals = internals

    def get_filename(self) :
        return self._filename

    def set_filename(self,filename) :
        self._filename = filename

    def read(self,content=None,filename=None) :
        if filename is None :
            filename = self._filename

        document = None
        if content is not None :
            # here is content parsing
            document = minidom.parseString(content)
        elif filename is not None :
            # here is file parsing
            document = minidom.parse(filename)
        else :
            raise ParsingError('You must either read a content, or a filename')

        rootname = document.childNodes[0].nodeName

        if rootname != 'pakkorn' :
            raise ParsingError('this xml is not a pakkorn xml')

        package_or_catalog_roots = filterout_textnode(document.childNodes[0].childNodes)

        if (len(package_or_catalog_roots) != 1) or (package_or_catalog_roots[0].nodeName not in ('package','catalog')) :
            raise ParsingError('pakkorn xml file should contain either one and only one catalog, either one and only one package')

        package_or_catalog_rootname = package_or_catalog_roots[0].nodeName

        if package_or_catalog_rootname == 'package' :
            return self._read_package(package_or_catalog_roots[0])

        if package_or_catalog_rootname == 'catalog' :
            return self._read_catalog(package_or_catalog_roots[0])

        ParsingError('Logical error : We should never see that error')

    def _read_referencablestring(self,node,value_attribute=None) :
        result = None
        for subnode in filterout_node(node.childNodes,'regexp') :
            result = ReferencableString(url=subnode.getAttribute('href'),pattern=subnode.getAttribute('pattern'))
            container = subnode.getAttribute('container')
            if container != '' :
                result.set_reference_container(container)
        if result is None :
            result_string = ''
            if value_attribute is None :
                for subnode in node.childNodes :
                    if subnode.nodeType == subnode.TEXT_NODE :
                        result_string += subnode.data.strip(' \t\r\n')
            else :
                result_string = node.getAttribute(value_attribute)
            result = ReferencableString(string=result_string)
        return result

    def _read_package(self,package_node) :
        idproj = None
        if package_node.hasAttribute('idproj') :
            idproj = package_node.getAttribute('idproj')

        package = Package(idproj=idproj)

        for node in filterout_textnode(package_node.childNodes) :
            if node.nodeName == 'pakkorn-base' :
                package.set_base_url(node.getAttribute('href'))
            elif node.nodeName == 'version' :
                package.set_version(self._read_referencablestring(node))
            elif node.nodeName == 'fullname' :
                package.set_fullname(self._read_referencablestring(node))
            elif node.nodeName == 'description' :
                package.set_description(self._read_referencablestring(node))
            elif node.nodeName == 'items' :
                for item_node in filterout_node(node.childNodes,'item') :
                    package.set_item(itemname=item_node.getAttribute('name'),item=self._read_referencablestring(item_node,value_attribute='href'))
            elif node.nodeName == 'commands-set' :
                for commands_node in filterout_node(node.childNodes,'commands') :
                    commands = Commands()
                    for command_node in filterout_node(commands_node.childNodes,'command') :
                        uninstall_winname = command_node.getAttribute('uninstall-winname')
                        if uninstall_winname == '' :
                            commands.add_command(line=command_node.getAttribute('line'))
                        else :
                            commands.add_command(uninstall_winname=uninstall_winname)
                    commands_type = commands_node.getAttribute('commands-type')
                    package.set_commands(commands_type,commands)

            elif node.nodeName == 'categories' :
                for category_node in filterout_node(node.childNodes,'category') :
                    category = ''
                    for subnode in category_node.childNodes :
                        if subnode.nodeType == subnode.TEXT_NODE :
                            category = subnode.data.strip(' \t\r\n')
                    package.add_category(category)

            elif node.nodeName == 'icons' :
                for icon_node in filterout_node(node.childNodes,'icon') :
                    href = icon_node.getAttribute('href')
                    size = icon_node.getAttribute('size')
                    package.set_icon(size,href)

            elif node.nodeName == 'properties' :
                for property_node in filterout_node(node.childNodes,'property') :
                    name = property_node.getAttribute('name')
                    value = property_node.getAttribute('value')
                    package.set_property(name,value)

            elif self._internals and (node.nodeName == 'internals') :
                for internal_node in filterout_node(node.childNodes,'internal') :
                    name = internal_node.getAttribute('name')
                    value = internal_node.getAttribute('value')
                    package.set_internal(name=name,value=value)
                # internal data. For local database only
                pass

            else :
                # ParsingError ? Or ignore ? "Be strict in what you send, but generous in what you receive", so let's be generous...
                # ... for this time.
                pass

        return package

    def _read_catalog(self,catalog_node) :
        catalog = Catalog()
        for package_node in filterout_textnode(catalog_node.childNodes) :
            if package_node.nodeName == 'package' :
                catalog.add_package(self._read_package(package_node))
        return catalog


    def write(self,pakkorn) :

        if not(isinstance(pakkorn,Package)) or not(isinstance(pakkorn,Catalog))  :
            ValueError('pakkorn should be a package or a catalog')

        if self._filename is None :
            ValueError('A filename should be provided for the pakkorn XML file')

        document = minidom.Document()

        pakkorn_node = document.createElement('pakkorn')
        document.appendChild(pakkorn_node)

        if not(self._internals) :
            pakkorn_node.setAttribute('xmlns',PAKKORN_NS_URI)
            pakkorn_node.setAttribute('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
            pakkorn_node.setAttribute('xsi:schemaLocation',PAKKORN_SCHEMA_LOCATION)
            pakkorn_node.setAttribute('version',SCHEMA_VERSION)

        if isinstance(pakkorn,Package) :
            self._write_package(package=pakkorn,node=pakkorn_node)

        if isinstance(pakkorn,Catalog) :
            self._write_catalog(catalog=pakkorn,node=pakkorn_node)

        handle = open(self._filename,'wt')
        handle.write(document.toprettyxml())
        handle.close()

    def _write_referencablestring( self, node, nodename, referencablestring, value_attribute = None ) :
        document = node.ownerDocument

        if referencablestring is None :
            return

        subnode = document.createElement(nodename)

        if referencablestring.is_string() :
            if value_attribute is None :
                textnode = document.createTextNode(referencablestring.get_string())
                subnode.appendChild(textnode)
            else :
                subnode.setAttribute(value_attribute,referencablestring.get_string())
            subnode.setAttribute('type','value')

        elif referencablestring.is_reference() :
            url,pattern = referencablestring.get_reference()
            regexp_node = document.createElement('regexp')
            regexp_node.setAttribute('href',url)
            regexp_node.setAttribute('pattern',pattern)
            if referencablestring.get_reference_container() is not None :
                regexp_node.setAttribute('container',referencablestring.get_reference_container())
            subnode.appendChild(regexp_node)
            subnode.setAttribute('type','reference')
        else :
            ValueError('referencablestring should be either a string, either a reference to a string')

        node.appendChild(subnode)
        return subnode

    def _write_package(self, package, node) :
        document = node.ownerDocument

        node_package = document.createElement('package')
        node.appendChild(node_package)

        idproj = package.get_idproj()
        if idproj is not None :
            node_package.setAttribute('idproj',idproj)

        base_url = package.get_base_url()
        if base_url is not None :
            node_base_url = document.createElement('pakkorn-base')
            node_base_url.setAttribute('href',base_url)
            node_package.appendChild(node_base_url)

        version = package.get_version()
        if version is not None :
            self._write_referencablestring(node_package,'version',version)

        fullname = package.get_fullname()
        if fullname is not None :
            self._write_referencablestring(node_package,'fullname',fullname)

        description = package.get_description()
        if description is not None :
            self._write_referencablestring(node_package,'description',description)

        node_items = document.createElement('items')
        for itemname in package.iter_itemnames() :
            item = package.get_item(itemname)
            node_item = self._write_referencablestring(node_items,'item',item,value_attribute='href')
            node_item.setAttribute('name',itemname)
        if len(node_items.childNodes)>0 :
            node_package.appendChild(node_items)

        node_commands_set = document.createElement('commands-set')
        for commands_name in package.iter_commands_names() :
            node_commands = document.createElement('commands')
            node_commands.setAttribute('commands-type',commands_name)
            for command in package.get_commands(commands_name) :
                node_command = document.createElement('command')
                if command.is_uninstall_winname() :
                    node_command.setAttribute('uninstall-winname',command.get_uninstall_winname())
                else :
                    node_command.setAttribute('line',str(command))
                node_commands.appendChild(node_command)
            node_commands_set.appendChild(node_commands)
        if len(node_commands_set.childNodes)>0 :
            node_package.appendChild(node_commands_set)

        node_categories = document.createElement('categories')
        for category in package.iter_categories() :
            node_category = document.createElement('category')
            textnode = document.createTextNode(category)
            node_category.appendChild(textnode)
            node_categories.appendChild(node_category)

        if len(node_categories.childNodes)>0 :
            node_package.appendChild(node_categories)

        node_icons = document.createElement('icons')
        for size in package.iter_iconsizes() :
            node_icon = document.createElement('icon')
            node_icon.setAttribute('size',size)
            node_icon.setAttribute('href',package.get_icon(size))
            node_icons.appendChild(node_icon)

        if len(node_icons.childNodes)>0 :
            node_package.appendChild(node_icons)

        node_properties = document.createElement('properties')
        for property in package.iter_properties() :
            node_property = document.createElement('property')
            node_property.setAttribute('name',property)
            node_property.setAttribute('value',package.get_property(property))
            node_properties.appendChild(node_property)

        if len(node_properties.childNodes)>0 :
            node_package.appendChild(node_properties)

        if self._internals :
            node_internals = document.createElement('internals')
            for internal in package.iter_internals() :
                node_internal = document.createElement('internal')
                node_internal.setAttribute('name',internal)
                node_internal.setAttribute('value',package.get_internal(internal))
                node_internals.appendChild(node_internal)
            node_package.appendChild(node_internals)


    def _write_catalog(self, catalog, node) :
        document = node.ownerDocument

        node_catalog = document.createElement('catalog')
        node.appendChild(node_catalog)

        for package in catalog :
            self._write_package(package, node_catalog)
