import os
from setuptools import setup, find_packages


def read_file_content(filename):
    try:
        dir_path = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(dir_path, filename), encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""


def load_readme_text():
    """Load in README file as a string."""
    return read_file_content("README.md")


def load_requirements():
    """Load in requirements.txt as a list of strings."""
    return [line.strip() for line in read_file_content("requirements.txt").split('\n')]


_VERSION = '0.1'

setup(
    name='FightPandemics-Telegram bot',
    version=_VERSION,
    description='FightPandemics-Telegram bot backend implementation',
    long_description=load_readme_text(),
    classifiers=[
        # TODO: typing.
        "Typing :: Typed"
    ],
    url='https://github.com/FightPandemics/FightPandemics-Telegram/',
    author='FightPandemics',
    author_email='contact@fightpandemics.com',
    packages=find_packages(include=['project*']),
    test_suite="testing",
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    install_requires=load_requirements(),
    include_package_data=True,
    license='MIT',
    keywords='FightPandemics-Telegram'
)
