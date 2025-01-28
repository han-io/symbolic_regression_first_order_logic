import setuptools

setuptools.setup(
    name='sr_fol',
    version='0.9.0',
    packages=setuptools.find_packages('.'),
    package_dir={
        'sr_fol': 'sr_fol',
    },
    setup_requires=['wheel'],
)