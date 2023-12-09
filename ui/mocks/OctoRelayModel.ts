export const modelMock = jest.fn();

jest.mock("../model/OctoRelayModel", () => ({ OctoRelayViewModel: modelMock }));
