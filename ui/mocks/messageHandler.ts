export const handlerMock = jest.fn();

jest.mock("../model/messageHandler", () => ({
  makeMessageHandler: jest.fn(() => handlerMock),
}));
