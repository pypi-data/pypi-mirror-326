from setuptools import setup

setup(name='GT_Utils',
      version='1.0.0',
      description='GT_Utils',
      url='https://github.com/BigDataFounder/GT_Utils',
      author='gengch',
      author_email='gengchuanhua@163.com',
      license='MIT',
      packages=[
            'GT_Utils', 
            "GT_Utils/EventTracker", 
            "GT_Utils/FileUtils", 
            "GT_Utils/GUI_Utils", 
            "GT_Utils/GUI_Utils/Group", 
            "GT_Utils/GUI_Utils/GroupElement",
            "GT_Utils/GUI_Utils/Window"
      ])
