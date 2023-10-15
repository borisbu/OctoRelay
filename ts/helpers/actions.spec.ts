import { elementMock, jQueryMock } from "../mocks/jQuery";
import { cancelTask, toggleRelay } from "./actions";

describe("Actions", () => {
  const apiMock = jest.fn();

  Object.assign(global, {
    OctoPrint: { simpleApiCommand: apiMock },
    $: jQueryMock,
  });

  afterEach(() => {
    apiMock.mockClear();
    elementMock.text.mockClear();
    elementMock.modal.mockClear();
    elementMock.find.mockClear();
    elementMock.on.mockClear();
  });

  describe("toggleRelay() action", () => {
    test("should toggle the relay", () => {
      toggleRelay("r1", {
        relay_pin: 16,
        inverted_output: false,
        relay_state: true,
        label_text: "Nozzle Light",
        active: true,
        icon_html: "<div>&#128161;</div>",
        confirm_off: false,
        upcoming: null,
      });
      expect(apiMock).toHaveBeenCalledWith("octorelay", "update", {
        pin: "r1",
      });
    });

    test("should open the confirmation dialog", () => {
      toggleRelay("r2", {
        relay_pin: 12,
        inverted_output: true,
        relay_state: true,
        label_text: "Printer",
        active: true,
        icon_html: '<img src="plugin/dashboard/static/img/printer-icon.png">',
        confirm_off: true,
        upcoming: null,
      });
      expect(jQueryMock).toHaveBeenCalledWith("#octorelay-confirmation-dialog");
      expect(elementMock.find.mock.calls).toMatchSnapshot(".find()");
      expect(elementMock.text.mock.calls).toMatchSnapshot(".text()");
      expect(elementMock.modal).toHaveBeenCalledWith("show");
      expect(elementMock.on).toHaveBeenCalledTimes(2);
      elementMock.modal.mockClear();
      elementMock.on.mock.calls[0][1](); // cancel
      expect(elementMock.modal).toHaveBeenCalledWith("hide");
      elementMock.modal.mockClear();
      elementMock.on.mock.calls[1][1](); // confirm
      expect(apiMock).toHaveBeenCalledWith("octorelay", "update", {
        pin: "r2",
      });
      expect(elementMock.modal).toHaveBeenCalledWith("hide");
    });
  });

  describe("cancelTask() action", () => {
    test("should trigger API command", () => {
      cancelTask("r2", {
        owner: "PRINTING_STARTED",
        target: true,
        deadline: 86400,
      });
      expect(apiMock).toHaveBeenCalledWith("octorelay", "cancelTask", {
        owner: "PRINTING_STARTED",
        subject: "r2",
        target: true,
      });
    });
  });
});
