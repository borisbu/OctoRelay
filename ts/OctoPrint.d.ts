interface ViewModel {
  construct: (params: object[]) => void;
  dependencies: string[]
}

declare const OCTOPRINT_VIEWMODELS: Array<ViewModel>
