
from setuptools import setup


try:
    from lazypage import VERSION
except Exception as e:
    VERSION = ''

try:
    long_description = open('README.md').read()
except Exception as e:
    long_description = ''


setup(
    name='django-lazypage',
    version=VERSION,
    description='django 页面异步加载解决方案',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='tao.py',
    author_email='taojy123@163.com',
    maintainer='tao.py',
    maintainer_email='taojy123@163.com',
    install_requires=open('requirements.txt').read().strip().splitlines(),
    license='MIT License',
    py_modules=['lazypage'],
    include_package_data=True,
    platforms=["all"],
    url='https://github.com/taojy123/django-lazypage',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
)
