from setuptools import setup

try:
    from jupyterpip import cmdclass
except:
    import pip, importlib
    pip.main(['install', 'jupyter-pip']); cmdclass = importlib.import_module('jupyterpip').cmdclass

setup(
    name='drilsdown',
    version='0.20',
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
