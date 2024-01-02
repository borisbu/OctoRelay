import { vi } from "vitest";

export const modelMock = vi.fn();

vi.mock("../model/OctoRelayModel", () => ({ OctoRelayViewModel: modelMock }));
