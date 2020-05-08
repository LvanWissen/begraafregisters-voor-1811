from setuptools import setup

setup(name='begraafregisters',
      packages=['begraafregisters'],
      include_package_data=True,
      install_requires=[
          'flask', 'sqlalchemy', 'flask-admin', 'flask_migrate', 'lxml',
          'psycopg2'
      ])
