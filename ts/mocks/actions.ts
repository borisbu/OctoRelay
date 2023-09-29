export const cancelMock = jest.fn();
export const toggleMock = jest.fn();

jest.mock("../helpers/actions", () => ({
  cancelTask: cancelMock,
  toggleRelay: toggleMock,
}));
