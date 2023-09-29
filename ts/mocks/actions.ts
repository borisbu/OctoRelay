export const cancelMock = jest.fn();

jest.mock("../helpers/actions", () => ({
  cancelTask: cancelMock,
}));
