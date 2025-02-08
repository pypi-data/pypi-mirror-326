from setuptools import setup, find_packages

setup(
    name="mcfinder",
    version="1.0.0",
    description="MinecraftServerFinder",
    author="MyNamexd",
    author_email="ahah@example.com",
    packages=find_packages(),
    install_requires=[
        "plyer",
        "pillow",
        "tkinter"
    ],
    include_package_data=True,  # Inclure les fichiers non-Python
    package_data={
        "mcfinder": ["*.ico", "*.jpg"],  # Spécifier les fichiers à inclure
    },
    entry_points={
        "console_scripts": [
            "mcfinder=mcfinder.pinger:main",
        ],
    },
)
