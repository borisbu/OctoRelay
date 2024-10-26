import MockDate from "mockdate";
import assert from "node:assert/strict";
import { elementMock, jQueryMock } from "../mocks/jQuery";
import { lodashMock } from "../mocks/lodash";

describe("Countdown helpers", async () => {
  const warnSpy = vi.spyOn(console, "warn").mockImplementation(() => {});
  const setIntervalMock = vi.fn<(handler: () => void, delay: number) => void>(
    () => "mockedInterval",
  );
  const clearIntervalMock = vi.fn();

  Object.assign(global, {
    LOCALE: "en",
    $: jQueryMock,
    _: lodashMock,
    setInterval: setIntervalMock,
    clearInterval: clearIntervalMock,
  });

  const { formatDeadline, getCountdownDelay, setCountdown } = await import(
    "./countdown"
  );

  beforeAll(() => {
    MockDate.set("2023-08-13T22:30:00");
  });

  afterEach(() => {
    Object.assign(global, {
      LOCALE: "en",
    });
    warnSpy.mockClear();
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
        expect(warnSpy).not.toHaveBeenCalled();
      },
    );

    test("should handle invalid locales", () => {
      Object.assign(global, {
        LOCALE: "invalid_locale_id",
      });
      expect(formatDeadline(Date.now() + 10000)).toBe(`in 10 seconds`);
      expect(warnSpy).toHaveBeenCalledTimes(2);
      expect(warnSpy.mock.calls).toEqual([
        [
          "Failed to format time using invalid_locale_id locale",
          expect.any(Error),
        ],
        [
          "Failed to format time using invalid-locale-id locale",
          expect.any(Error),
        ],
      ]);
    });

    test.each([
      [1000, "1 second"],
      [10000, "10 seconds"],
    ])("should handle complete Intl malfunction", (offset, expected) => {
      vi.spyOn(Intl, "NumberFormat").mockImplementation(() =>
        assert.fail("Can not do this"),
      );
      expect(formatDeadline(Date.now() + offset)).toBe(`in ${expected}`);
      expect(warnSpy).toHaveBeenCalledTimes(2);
      expect(warnSpy.mock.calls).toEqual([
        ["Failed to format time using en locale", expect.any(Error)],
        ["Failed to format time using undefined locale", expect.any(Error)],
      ]);
    });
  });

  describe("getCountdownDelay() helper", () => {
    test.each([60, 120, 121])(
      "should return refresh interval for supplied timestamp having offset %s seconds",
      (offset) => {
        expect(getCountdownDelay(Date.now() + offset * 1000)).toMatchSnapshot();
      },
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
          1000,
        );
        // coverage branch for the case nextDelay === delay
        const nextIntervalFn = setIntervalMock.mock.calls[1][0];
        MockDate.set(Date.now() + 1000); // same delay branch this time
        nextIntervalFn();
        expect(setIntervalMock).toHaveBeenCalledTimes(2); // not called again this time
      } else {
        expect(elementMock.text).not.toHaveBeenCalled();
        expect(clearIntervalMock).toHaveBeenCalledWith("mockedInterval");
      }
    });
  });
});
