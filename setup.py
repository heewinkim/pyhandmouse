from setuptools import setup, find_packages

# pip install wheel           # 빌드 툴
# pip install setuptools     # 패키징 툴
# pip install twine            # 패키지 업로드 툴
require_packages=[
    'mediapipe',
    'PyAutoGUI',
    'opencv-python',
    'utilpack'
]

packages = list(open('requirements.txt').readlines())
setup(
    name='pyhandmouse',
    version='1.0.0',
    author='HEESEUNG KIM',
    author_email='heewin.kim@gmail.com',
    description='Hand Mouse using Python',
    long_description="""pyhandmouse\n
    카메라로 손을 포착하여 클릭을 하는 앱 입니다.
    현재는 단순한 단일클릭과 뷰하는 화면만 있습니다. 
    추후 더블클릭,드래그, 정교해진 뷰화면 등 다양하게 개발할 예정입니다.
    """,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/heewinkim/pyhandmouse',
    download_url='https://github.com/heewinkim/pyhandmouse/archive/master.zip',

    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    package_data={'':['*']},
    python_requires='>=3',
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)