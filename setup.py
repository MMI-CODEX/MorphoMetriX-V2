from setuptools import setup, find_packages

setup(
    name = "morphometrix",
    version = "2.0.0",
    description="A GUI for photogrammetry",
    author = "Walter Torres",
    author_email = "walter.torres@duke.edu",
    license='MIT',
    url = "https://github.com/ZappyMan/MorphoMetriX",
    entry_points={
        'gui_scripts': [
            'morphometrix = morphometrix.__main__:main'
        ]
    },
#    scripts=['morphometrix/morphometrix.py'],
    packages = ['morphometrix']
#    packages= find_packages()
)
