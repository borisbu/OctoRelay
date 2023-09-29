import MockDate from "mockdate";
import { countdownMock, disposerMock } from "../mocks/countdown";
import { addTooltip, clearHints, addPopover } from "./hints";

describe("Hints helpers", () => {
  const elementMock: Record<
    "popover" | "tooltip" | "find" | "on" | "off",
    jest.Mock
  > = {
    popover: jest.fn(() => elementMock),
    tooltip: jest.fn(() => elementMock),
    find: jest.fn(() => elementMock),
    on: jest.fn(() => elementMock),
    off: jest.fn(() => elementMock),
  };
  const jQueryMock = jest.fn((subject: string | (() => void)) => {
    if (typeof subject === "function") {
      return subject();
    }
    return elementMock;
  });

  Object.assign(global, {
    $: jQueryMock,
  });

  beforeAll(() => {
    MockDate.set("2023-08-13T22:30:00");
  });

  afterEach(() => {
    elementMock.popover.mockClear();
    elementMock.tooltip.mockClear();
    elementMock.find.mockClear();
    elementMock.on.mockClear();
    elementMock.off.mockClear();
  });

  afterAll(() => {
    MockDate.reset();
  });

  describe("clearHints() helper", () => {
    test("should remove both tooltip and popover from the target element", () => {
      clearHints(elementMock as unknown as JQuery);
      expect(elementMock.popover).toHaveBeenCalledWith("destroy");
      expect(elementMock.tooltip).toHaveBeenCalledWith("destroy");
    });
  });

  describe("addTooltip() helper", () => {
    test("should add tooltip to the target element", () => {
      addTooltip(elementMock as unknown as JQuery, "test");
      expect(elementMock.tooltip).toHaveBeenCalledWith({
        placement: "bottom",
        title: "test",
      });
    });
  });

  describe("addPopover() helper", () => {
    test("should add a popover to the target element", async () => {
      const cancelMock = jest.fn();
      addPopover({
        target: elementMock as unknown as JQuery,
        title: "Title",
        content: ["line1", "line2"],
        navbar: elementMock as unknown as JQuery,
        originalSubject: "Relay",
        items: [
          {
            cancelId: "cancel-id",
            deadline: Date.now() + 60 * 1000,
            timeTagId: "time-id",
            cancel: cancelMock,
          },
        ],
      });
      expect(elementMock.popover.mock.calls).toMatchSnapshot(".popover()");
      expect(elementMock.find.mock.calls).toMatchSnapshot(".find()");
      expect(countdownMock).toHaveBeenCalledWith(elementMock, 1691965860000);
      expect(elementMock.on).toHaveBeenCalledTimes(2); // cancel, close
      expect(elementMock.on.mock.calls[0][1]).toEqual(cancelMock);
      const close = elementMock.on.mock.calls[1][1];
      expect(elementMock.off).not.toHaveBeenCalled();
      expect(disposerMock).not.toHaveBeenCalled();
      close();
      expect(elementMock.off).toHaveBeenCalledWith("click");
      expect(disposerMock).toHaveBeenCalledTimes(1);
      expect(elementMock.tooltip).toHaveBeenCalledWith({
        placement: "bottom",
        title: "Relay",
      });
    });
  });
});
