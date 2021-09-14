# [pyhandmouse](https://github.com/heewinkim/pyhandmouse)
![](https://img.shields.io/badge/python-3.7.10-blue)

    저의 게으름을 한층 업그레이드 하기 위한 프로젝트입니다. 
    카메라를 통해 손을 인식후 마우스를 컨트롤하는 프로젝트입니다. 
    이동/클릭이 구현되어있습니다. 



PyAutoGUI
### 사용된 패키지

![](https://img.shields.io/badge/mediapipe-blue?style=for-the-badge&logo=appveyor)

![](https://img.shields.io/badge/PyAutoGUI-orange?style=for-the-badge&logo=appveyor)


## 설치 & 사용법

### 설치
````shell
pip3 install pyautomouse
````

````python
from pyhandmouse import PyHandMouse

# 엄지 검지를 붙이면 클릭
# 종료는 q
PyHandMouse()


````


---

TODO LIST

- [ ] move more smoothy
- [ ] click without false positive
- [ ] make region of control which minimap of whole screen
- [ ] transform window to transparently and pretty
- [ ] code to app or pypi or docker .. etc..
- [ ] write readme.... 
- [ ] make time..................