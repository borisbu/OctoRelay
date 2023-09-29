export const clearMock = jest.fn();
export const showMock = jest.fn();

jest.mock("../helpers/hints", () => ({
  clearHints: clearMock,
  showHints: showMock,
}));
