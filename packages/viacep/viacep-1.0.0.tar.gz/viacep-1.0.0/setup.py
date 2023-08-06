from distutils.core import setup

setup(
    name='viacep',
    version='1.0.0',
    author='Leonardo Gregianin',
    author_email='leogregianin@gmail.com',
    scripts=['viacep.py', 'test_viacep.py', 'sample.py'],
    url='https://github.com/leogregianin/viacep-python',
    license='LICENSE',
    description='Consulta CEP pelo webservice do ViaCEP.com.br',
    long_description=open('README.md').read(),
)