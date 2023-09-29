import MockDate from "mockdate";
import { countdownMock, deadlineMock, disposerMock } from "../mocks/countdown";
import { cancelMock } from "../mocks/actions";
import { elementMock, jQueryMock } from "../mocks/jQuery";
import { addTooltip, clearHints, addPopover, showHints } from "./hints";

describe("Hints helpers", () => {
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
    deadlineMock.mockClear();
    countdownMock.mockClear();
    disposerMock.mockClear();
    cancelMock.mockClear();
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

  describe("showHints() helper", () => {
    test("should display tooltips", () => {
      showHints({
        navbar: elementMock as unknown as JQuery,
        hints: [
          {
            key: "r1",
            control: elementMock as unknown as JQuery,
            relay: {
              relay_pin: 16,
              inverted_output: false,
              relay_state: true,
              label_text: "Nozzle Light",
              active: true,
              icon_html: "<div>&#128161;</div>",
              confirm_off: false,
              upcoming: null,
            },
          },
          {
            key: "r2",
            control: elementMock as unknown as JQuery,
            relay: {
              relay_pin: 12,
              inverted_output: true,
              relay_state: true,
              label_text: "Printer",
              active: true,
              icon_html:
                '<img src="plugin/dashboard/static/img/printer-icon.png">',
              confirm_off: true,
              upcoming: null,
            },
          },
        ],
      });
      expect(elementMock.popover).not.toHaveBeenCalled();
      expect(elementMock.tooltip).toHaveBeenCalledTimes(2);
      expect(elementMock.tooltip.mock.calls).toMatchSnapshot();
    });

    test("should show popover for a single upcoming task", () => {
      showHints({
        navbar: elementMock as unknown as JQuery,
        hints: [
          {
            control: elementMock as unknown as JQuery,
            key: "r1",
            relay: {
              relay_pin: 16,
              inverted_output: false,
              relay_state: false,
              label_text: "Nozzle Light",
              active: true,
              icon_html: "<div>&#128161;</div>",
              confirm_off: false,
              upcoming: {
                target: true,
                owner: "PRINTING_STOPPED",
                deadline: Date.now() + 60 * 1000,
              },
            },
          },
        ],
      });
      expect(elementMock.tooltip).not.toHaveBeenCalled();
      expect(deadlineMock).toHaveBeenCalledWith(1691965860000);
      expect(elementMock.popover).toHaveBeenCalledTimes(2);
      expect(elementMock.popover.mock.calls).toMatchSnapshot();
      expect(elementMock.on).toHaveBeenCalledTimes(2); // cancel, close
      expect(cancelMock).not.toHaveBeenCalled();
      const cancel = elementMock.on.mock.calls[0][1];
      cancel();
      expect(cancelMock).toHaveBeenCalledWith("r1", {
        deadline: 1691965860000,
        owner: "PRINTING_STOPPED",
        target: true,
      });
    });

    test("should show single popover for multiple upcoming tasks", () => {
      showHints({
        navbar: elementMock as unknown as JQuery,
        hints: [
          {
            control: elementMock as unknown as JQuery,
            key: "r1",
            relay: {
              relay_pin: 16,
              inverted_output: false,
              relay_state: true,
              label_text: "Nozzle Light",
              active: true,
              icon_html: "<div>&#128161;</div>",
              confirm_off: false,
              upcoming: {
                target: false,
                owner: "PRINTING_STOPPED",
                deadline: Date.now() + 120 * 1000,
              },
            },
          },
          {
            control: elementMock as unknown as JQuery,
            key: "r1",
            relay: {
              relay_pin: 12,
              inverted_output: false,
              relay_state: true,
              label_text: "Printer",
              active: true,
              icon_html:
                '<img src="plugin/dashboard/static/img/printer-icon.png">',
              confirm_off: true,
              upcoming: {
                target: false,
                owner: "PRINTING_STOPPED",
                deadline: Date.now() + 300 * 1000,
              },
            },
          },
        ],
      });
      expect(elementMock.tooltip).toHaveBeenCalledTimes(1);
      expect(elementMock.tooltip.mock.calls).toMatchSnapshot();
      expect(deadlineMock).toHaveBeenCalledTimes(2);
      expect(elementMock.popover).toHaveBeenCalledTimes(2);
      expect(elementMock.popover.mock.calls).toMatchSnapshot();
    });
  });
});
