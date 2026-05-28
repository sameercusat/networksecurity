from setuptools import setup,find_packages
from typing import List

'''Setup.py is an important componenet of python project.It helps in making python packange and project distribution'''

def get_requirements() -> List[str]:
    requirement_list:List[str] = []
    try:
        with open('requirements.txt','r') as f:
            lines = f.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
        return requirement_list
    except FileNotFoundError:
        print('Requirements.txt file is not avaialable')


setup(
    name = 'Network_Security',
    version='0.0.1',
    author='Sameer Kumar',
    author_email='sameer.cusat2019@gmail.com',
    install_requires=get_requirements(),
    packages=find_packages()
)
