from setuptools import setup
from setuptools.command.install import install
import os

class CustomInstall(install):
    def run(self):
        try:
           idv_path=os.path.join(os.path.expanduser('~'),'.unidata','idv','DefaultIdv')
           with open(os.path.join(idv_path,'idv.properties'),'w') as f:
                f.write('idv.monitorport = 8765')
           print('Wrote idv monitor port 8765 to the file idv.properties in '+idv_path)
        except:
           raise
 
try:
    from jupyterpip import cmdclass
except:
    import pip, importlib
    pip.main(['install', 'jupyter-pip']); cmdclass = importlib.import_module('jupyterpip').cmdclass

setup( 
    name='drilsdown',
    version='0.50',
    url="https://github.com/Unidata/ipython-IDV",
    author='Unidata',
    author_email='drilsdown@unidata.ucar.edu',
    license="MIT",
    install_requires=['jupyter-pip'],
    packages=['drilsdown'],
    cmdclass=cmdclass('drilsdown', 'drilsdown/init'),
    description="Jupyter extension for working with the IDV in a notebook ",
    classifiers=[
    'Development Status :: 4 - Beta',

    'Topic :: Software Development :: Build Tools',
     'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
]
)

setup(cmdclass={'install':CustomInstall},
      name='setting up .unidata paths',packages=[],install_requires=[])
