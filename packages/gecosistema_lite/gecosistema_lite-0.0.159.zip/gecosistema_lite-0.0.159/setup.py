from distutils.core import setup

setup(name='gecosistema_lite',
      version='0.0.159',
      description='A simple python package',
      author='Valerio Luzzi',
      author_email='valerio.luzzi@gecosistema.it',
      url='https://github.com/valluzzi/libcore/',
      license='MIT',
      packages=['gecosistema_lite'],
      data_files=[('Lib/site-packages/gecosistema_lite',['gecosistema_lite/qkrige_v3.r'])],
      install_requires=['pyproj', 'rarfile', 'xlrd', 'xlwt', 'xlutils', 'jinja2', 'xmljson', 'openpyxl', 'pycrypto',
                        'pyodbc'],
      python_requires='>=2.7'
      )
