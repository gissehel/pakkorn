import os
import unittest

project_path = '.'

GENERATE_PATH = os.path.join('..','ressources','test','generate')
REFERENCE_PATH = os.path.join('..','ressources','test','reference')

def get_test_generate_path(filename) :
    return os.path.join(project_path,GENERATE_PATH,filename)
    
def get_test_reference_path(filename) :
    return os.path.join(project_path,REFERENCE_PATH,filename)
    
def get_test_full_path(filename) :
    return get_test_generate_path(filename)
    
def apply_assert_on_file(filename,assertCallable) :
    generate_filename = get_test_generate_path(filename)
    reference_filename = get_test_reference_path(filename)
    
    assertCallable(open(generate_filename,'rb').read(),open(reference_filename,'rb').read(),'%s is a different file between generate and reference' % filename)

class TestCase(unittest.TestCase) :
    class_dir_prefix = []
    class_test_prefix = []
    use_dir = False

    def set_test_path(self, *test_dirs, **kwargs) :
        self.class_test_prefix = list(test_dirs)
        self.use_dir = kwargs.get('use_dir',False)
        if self.use_dir :
            clean = kwargs.get('clean',False)
            dirname = self.get_full_test_path()

            if clean and os.path.exists(dirname) :
                if os.path.isdir(dirname) :
                    for dirname,dirnames,filenames in os.walk(dirname) :
                        for filename in filenames :
                            os.remove(os.path.join(dirname,filename))
                    os.removedirs(dirname)
                else :
                    os.remove(dirname)

            if not(os.path.exists(dirname)) :
                os.makedirs(dirname)

    def get_test_path(self,*paths,**kwargs) :
        if 'dir_prefix' in kwargs :
            dir_prefix = [kwargs['dir_prefix']]
        else :
            dir_prefix = self.class_dir_prefix
            
        if 'test_prefix' in kwargs :
            test_prefix = [kwargs['test_prefix']]
        else :
            test_prefix = self.class_test_prefix

        prefixes = dir_prefix + test_prefix

        if not(self.use_dir) :
            prefixes += list(paths)
        filename = "-".join(prefixes)
        if self.use_dir and (len(paths) > 0):
            filename = os.path.join(filename,*paths)
        return filename
        
    def get_full_test_path(self,*paths,**kwargs) :
        return get_test_generate_path(self.get_test_path(*paths,**kwargs))

    def assertFileIsReference(self,*paths,**kwargs) :
        filename = self.get_test_path(*paths,**kwargs)

        return apply_assert_on_file(filename,self.assertEqual)
