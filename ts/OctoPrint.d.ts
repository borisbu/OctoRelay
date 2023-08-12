/// <reference types="jquery" />

interface JQuery {
  /** @see https://github.com/OctoPrint/OctoPrint/blob/1.9.0/src/octoprint/static/js/lib/bootstrap/bootstrap-modal.js */
  modal(option: "show" | "hide"): JQuery;
  tooltip(
    option:
      | "destroy"
      | "toggle"
      | "hide"
      | "show"
      | { placement?: "top" | "bottom" | "left" | "right" }
  );
  popover(
    option:
      | "destroy"
      | "toggle"
      | "hide"
      | "show"
      | {
          html?: boolean;
          placement?: "top" | "bottom" | "left" | "right";
          trigger?: "click" | "hover" | "focus" | "manual";
          content?: string;
        }
  );
}

interface ViewModel {
  construct: (params: object[]) => void;
  dependencies: string[];
}

declare const OCTOPRINT_VIEWMODELS: Array<ViewModel>;

/** @see https://github.com/OctoPrint/OctoPrint/blob/1.9.0/docs/jsclientlib/base.rst */
declare const OctoPrint: {
  simpleApiCommand: (
    plugin: string,
    command: string,
    payload: object,
    opts?: object
  ) => JQuery.Promise<any>;
};
