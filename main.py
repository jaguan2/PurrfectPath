from website import create_app
from setuptools import setup, find_packages
from requirements import install_requirements

app = create_app()

if __name__ == '__main__':
  setup(
    name='MyFlaskApp',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requirements,
  )
  
  app.run(debug=True)