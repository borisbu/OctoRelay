import MockDate from "mockdate";
import { elementMock, jQueryMock } from "../mocks/jQuery";
import { formatDeadline, getCountdownDelay, setCountdown } from "./countdown";

describe("Countdown helpers", () => {
  const setIntervalMock = jest.fn<void, [() => void, number]>(
    () => "mockedInterval"
  );
  const clearIntervalMock = jest.fn();

  Object.assign(global, {
    LOCALE: "en",
    $: jQueryMock,
    setInterval: setIntervalMock,
    clearInterval: clearIntervalMock,
  });

  beforeAll(() => {
    MockDate.set("2023-08-13T22:30:00");
  });

  afterEach(() => {
    setIntervalMock.mockClear();
    clearIntervalMock.mockClear();
    elementMock.text.mockClear();
    elementMock.is.mockClear();
  });

  afterAll(() => {
    MockDate.reset();
  });

  describe("formatDeadline() helper", () => {
    test.each([0, 1, 30, 59, 60, 61, 90, 119, 120, 121, 300, 600, 3600])(
      "Should format the supplied UNIX timestamp having offset %s seconds",
      (offset) => {
        expect(formatDeadline(Date.now() + offset * 1000)).toMatchSnapshot();
      }
    );
  });

  describe("getCountdownDelay() helper", () => {
    test.each([60, 120, 121])(
      "should return refresh interval for supplied timestamp having offset %s seconds",
      (offset) => {
        expect(getCountdownDelay(Date.now() + offset * 1000)).toMatchSnapshot();
      }
    );
  });

  describe("setCountdown() helper", () => {
    test.each([true, false])("should set countdown %#", (isVisible) => {
      setCountdown(elementMock as unknown as JQuery, Date.now() + 121 * 1000);
      expect(setIntervalMock).toHaveBeenCalledWith(expect.any(Function), 60000);
      const intervalFn = setIntervalMock.mock.calls[0][0];
      elementMock.is.mockImplementationOnce(() => isVisible);
      MockDate.set(Date.now() + 1000); // this will trigger the new delay
      intervalFn();
      if (isVisible) {
        expect(elementMock.text).toHaveBeenCalledWith("in 2 minutes");
        expect(setIntervalMock).toHaveBeenCalledTimes(2); // reset with a new delay
        expect(setIntervalMock).toHaveBeenCalledWith(
          expect.any(Function),
          1000
        );
      } else {
        expect(elementMock.text).not.toHaveBeenCalled();
        expect(clearIntervalMock).toHaveBeenCalledWith("mockedInterval");
      }
    });
  });
});
