export const clearMock = vi.fn();
export const showMock = vi.fn();

vi.mock("../helpers/hints", () => ({
  clearHints: clearMock,
  showHints: showMock,
}));
