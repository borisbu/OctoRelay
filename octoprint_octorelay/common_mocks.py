import sys

GPIO_mock = Mock()
GPIO_mock.BCM = "MockedBCM"
GPIO_mock.OUT = "MockedOUT"
sys.modules["RPi.GPIO"] = GPIO_mock

timerMock = Mock()
utilMock = Mock(
    RepeatedTimer = Mock(return_value=timerMock),
    ResettableTimer = Mock(return_value=timerMock)
)
sys.modules["octoprint.util"] = utilMock

permissionsMock = Mock()
sys.modules["octoprint.access.permissions"] = Mock(
    Permissions=permissionsMock
)
