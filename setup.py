from setuptools import setup


setup(
    name='djhacker',
    versioning='dev',
    setup_requires='setupmeta',
    extras_require=dict(
        test=[
            'pytest',
            'pytest-cov',
            'pytest-django',
        ],
    ),
    author='James Pic',
    author_email='jamespic@gmail.com',
    url='https://yourlabs.io/oss/django-djhacker',
    include_package_data=True,
    license='MIT',
    keywords='django forms',
    python_requires='>=3.7',
)
