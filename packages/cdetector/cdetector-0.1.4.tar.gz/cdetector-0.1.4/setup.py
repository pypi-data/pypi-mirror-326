from setuptools import setup, find_packages

setup(
    name='cdetector',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'easyocr',
        'ultralytics',
        'pytesseract',
        'requests',
    ],
    author='Mahdi Huseine',
    author_email='madihuseine001@gmail.com',
    description='A Python library for license plate recognition using YOLO and OCR',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://pypi.org/project/cdetector/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
