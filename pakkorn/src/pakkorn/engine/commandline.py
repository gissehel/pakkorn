from sys import argv

from pakkorn.engine.engine import Engine
from pakkorn.config import config
from pakkorn.config.help import usage
from pakkorn.config.register import register_key

def apt_parse(argv) :
    engine = Engine(config)
    command = argv[0]
    
    if command == 'update' :
        engine.update()
    elif command in ('search','xsearch') :
        pattern = ''
        if len(argv) > 1 :
            pattern = argv[1]
        for package in engine.search(pattern) :
            if command == 'search' :
                print "%s - %s" % (package.get_idproj(),package.get_fullname())
            elif command == 'xsearch' :
                print "%s%s%s %s - %s - %s" % (
                    package.get_internal('installed')=='true' and 'I' or ' ',
                    package.get_internal('downloaded')=='true' and 'D' or ' ',
                    package.get_internal('lastcatalog')=='true' and 'L' or ' ',
                    package.get_idproj(),
                    package.get_fullname(),
                    package.get_version(),
                    )
    elif command == 'show' :
        pattern = ''
        version = None
        if len(argv) > 1 :
            pattern = argv[1]
            if '=' in pattern :
                (pattern,version) = pattern.split('=',1)
        for package in engine.show(pattern,version=version) :
            print "Package: %s" % (package.get_idproj(),)
            status = None
            if package.get_internal('installed')=="true" :
                status = "Installed"
            elif package.get_internal('downloaded')=="true" :
                status = "Downloaded"
            if status is not None :
                print "Status: %s" % (status,)
            print "Version: %s" % (package.get_version(),)
            print "Last Catalog: %s" % (package.get_internal('lastcatalog'),)
            description = package.get_description()
            description = str(description).replace("\n"," \n")
            print "Description: %s" % (description,)
            print ""
    elif command in ('install','uninstall','download_install') :
        if len(argv) > 1 :
            package_params = []
            for arg in argv[1:] :
                package_param = {}
                if '=' in arg :
                    (package_param['idproj'],package_param['version']) = (arg.split('=',1))
                else :
                    package_param['idproj'] = arg
                package_params.append(package_param)
            error = engine.do_commands_name(command,*package_params)
            if error is not None : 
                print "Error : [%s]" % error
        else :
            print "Install take 2 other arguments"
    elif command == 'aggregate' :
        if len(argv) >= 3 :
            url = argv[1]
            output_filename = argv[2]
            engine.aggregate(url,output_filename)
    else :
        print "Don't know how to %s" % (command,)


def parse_command_line(callnext=None) :
    if callnext is None :
        callnext=lambda :usage(True)

    if len(argv) == 0 :
        raise Exception("No executable name ??!!??")
    else :
        config.process_argv(argv[0],argv[1:])

        if config['help'] :
            usage(False)
        elif config['help-expert'] :
            usage(True)
        elif config['save'] :
            del config['save']
            config.save_non_persistant()
        else :
            if len(config['']) <= 0 :
                return callnext()
            else :
                apt_parse(config[''])

register_key('help',bool,doc='Show help on commands')
register_key('help-expert',bool,doc='Show adanced help on commands')
register_key('save',bool,doc='Save the options in command line into configuration file', advanced=True)

if __name__ == '__main__' :
    main(argv)
