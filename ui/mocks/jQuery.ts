export const elementMock: Record<
  | "toggle"
  | "html"
  | "off"
  | "on"
  | "find"
  | "text"
  | "modal"
  | "is"
  | "popover"
  | "tooltip",
  jest.Mock
> = {
  toggle: jest.fn(() => elementMock),
  html: jest.fn(() => elementMock),
  off: jest.fn(() => elementMock),
  on: jest.fn(() => elementMock),
  find: jest.fn(() => elementMock),
  text: jest.fn(() => elementMock),
  modal: jest.fn(() => elementMock),
  is: jest.fn(() => elementMock),
  tooltip: jest.fn(() => elementMock),
  popover: jest.fn(() => elementMock),
};

export const jQueryMock = jest.fn((subject: string | (() => void)) => {
  if (typeof subject === "function") {
    return subject();
  }
  return elementMock;
});
