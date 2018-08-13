
from setuptools import setup, find_packages
from lazypage import VERSION

install_requires = []
for line in open('requirements.txt').readlines():
    line = line.strip()
    if line and not line.startswith('#'):
        install_requires.append(line)

setup(
    name='django-lazypage',
    version=VERSION,
    description='django 页面异步加载解决方案',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='tao.py',
    author_email='taojy123@163.com',
    maintainer='tao.py',
    maintainer_email='taojy123@163.com',
    install_requires=install_requires,
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,
    platforms=["all"],
    url='https://github.com/taojy123/django-lazypage',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
)
