from setuptools import setup

setup(
    name='airscooter_urban_physiology_plugin',
    packages=['airscooter_urban_physiology_plugin'], # this must be the same as the name above
    version='0.0.1',
    py_modules=['airscooter_urban_physiology_plugin'],
    install_requires=[
        'click', 'urban_physiology_toolkit'
    ],
    entry_points='''
        [airscooter.cli_plugins]
        init_catalog=airscooter_urban_physiology_plugin.cli:init_catalog
        finalize_catalog=airscooter_urban_physiology_plugin.cli:finalize_catalog
    ''',
    description='Plugin bringing the Urban Physiology workflow to airscooter.',
    author='Aleksey Bilogur',
    author_email='aleksey.bilogur@gmail.com',
    url='https://github.com/ResidentMario/airscooter-urban-physiology-plugin',
    download_url='https://github.com/ResidentMario/airscooter-urban-physiology-plugin/tarball/0.0.1',
    keywords=['data', 'data analysis', 'open data'],
    classifiers=[],
)
