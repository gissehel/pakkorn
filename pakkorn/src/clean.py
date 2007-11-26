
import os

def clean_path(pathtoclean) :
    for dirname,dirnames,filenames in os.walk(pathtoclean,topdown=False) :
        if '.svn' not in dirname :
            if '.svn' in dirnames :
                dirnames.remove('.svn')
            for filename in filenames :
                os.remove(os.path.join(dirname,filename))
            for adirname in dirnames :
                os.removedirs(os.path.join(dirname,adirname))
    #for dirname in os.listdir(pathtoclean) :
    #    if dirname != '.svn' :
    #        os.removedirs(os.path.join(pathtoclean,dirname))
    
def clean() :
    clean_path(os.path.join('..','ressources','test','generate'))
    clean_path(os.path.join('__cache__'))
    clean_path(os.path.join('__workingdir__','download'))
    clean_path(os.path.join('__workingdir__','base'))

if __name__=='__main__' :
    clean()
