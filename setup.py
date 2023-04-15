## build and use application as package

from setuptools import find_packages, setup
from typing import List

#to get this file automatically trigerred we have added -e . in requirements.txt but it shouldnot read that so fofr this
#init files in every folder to call that 
hyphen_e_dot = "-e ."

def get_requirements(file_path:str)->List[str]:
    '''
        this function will return list of requirements
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n','') for req in requirements]
        #to get this file automatically trigerred we have added -e . in requirements.txt but it shouldnot read that so fofr this
        if hyphen_e_dot in requirements:
            requirements.remove(hyphen_e_dot)
    
    return requirements

#it is metadata for the project
setup(

    name = "test project",
    version = '0.0.1',
    author = "Pranay",
    author_email = "pmohadikar.94@gmail.com",
    packages = find_packages(), #if find package is running it will check how many folders init file have. so it will diretly 
    #consider folder as package and you can build and import where ever you want. 
    #install_requires = ['pandas','numpy', 'seaborn'] # if too many packages here to install then we create get requirement func
    install_requires = get_requirements('requirements.txt')
)