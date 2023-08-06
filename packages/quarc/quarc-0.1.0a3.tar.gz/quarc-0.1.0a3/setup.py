from setuptools import setup

setup(
    name = "quarc",
    version = "0.1.0-alpha.3",
    author = "Simon Biggs",
    author_email = "mail@simonbiggs.net",
    description = "Open a Quarc Gateway",
    long_description = """This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.""",
    keywords = [],
    py_modules = [
        "quarc"
    ],
    entry_points={
        'console_scripts': [
            'quarc=quarc:main',
        ],
    },
    license='AGPL3+',
    install_requires=[
        'jupyter_kernel_gateway',
        'pyopenssl'
    ],
    classifiers = [],
    url = "https://quarc.services/"
)
