/// <reference types="jquery" />
/// <reference types="lodash" />

interface JQuery {
  /** @see https://github.com/OctoPrint/OctoPrint/blob/1.9.0/src/octoprint/static/js/lib/bootstrap/bootstrap-modal.js */
  modal(option: "show" | "hide"): JQuery;
  tooltip(
    option:
      | "destroy"
      | "toggle"
      | "hide"
      | "show"
      | {
          placement?: "top" | "bottom" | "left" | "right";
          title?: string;
        },
  ): JQuery;
  popover(
    option:
      | "destroy"
      | "toggle"
      | "hide"
      | "show"
      | {
          html?: boolean;
          animation?: boolean;
          placement?: "top" | "bottom" | "left" | "right";
          trigger?: "click" | "hover" | "focus" | "manual";
          title?: string;
          content?: string;
        },
  ): JQuery;
}

interface ViewModel {
  construct: (params: object[]) => void;
  dependencies: string[];
}

declare const OCTOPRINT_VIEWMODELS: Array<ViewModel>;
/** @see https://github.com/OctoPrint/OctoPrint/blob/1.5.3/src/octoprint/templates/initscript.jinja2#L32 */
declare const LOCALE: string;
/** @see https://github.com/OctoPrint/OctoPrint/blob/1.5.3/src/octoprint/static/js/lib/lodash.js */
declare const _: LoDashStatic;

/** @see https://github.com/OctoPrint/OctoPrint/blob/1.9.0/docs/jsclientlib/base.rst */
declare const OctoPrint: {
  simpleApiCommand: (
    plugin: string,
    command: string,
    payload: object,
    opts?: object,
  ) => JQuery.Promise<unknown>;
};
