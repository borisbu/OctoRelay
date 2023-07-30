/**
 * WARNING: This is a stub for those who installs the plugin from sources
 *
 * PLEASE NOTE the new URL for installing the distributed package:
 * @link https://github.com/borisbu/OctoRelay/releases/download/latest/release.zip
 *
 * The actual JavaScript is compiled from TypeScript during the execution of release workflow.
 */

$(() => {
  const handleClick = () => {
    const dialog = $("#octorelay-confirmation-dialog");
    dialog.find(".modal-title").text("OctoRelay needs one more update");
    dialog
      .find("#octorelay-confirmation-text")
      .css({
        "font-weight": "normal",
        "font-size": "1rem",
        "word-wrap": "break-word",
      })
      .text(
        "We switched to distributing the plugin in the form of a specially prepared installation " +
          "package instead of offering the installation from sources. " +
          "The URL for fetching updates has changed because of this. " +
          'However, there is no cause for concern: please proceed to the "Software update" section of the ' +
          "OctoPrint settings and update OctoRelay one more time. Sorry for the inconvenience. " +
          "As a last resort, you can always install it manually using the following URL: " +
          "https://github.com/borisbu/OctoRelay/releases/download/latest/release.zip"
      );
    dialog
      .find(".btn-cancel")
      .text("Close")
      .off("click")
      .on("click", () => {
        dialog.modal("hide");
      });
    dialog.find(".btn-confirm").hide();
    dialog.modal("show");
  };
  $("#relaisr1")
    .css({
      display: "flex",
      float: "left",
      width: "40px",
      height: "40px",
      padding: "unset",
      cursor: "pointer",
      "font-size": "1.25rem",
      "text-decoration": "none",
      "align-items": "center",
      "justify-content": "center",
    })
    .html('<i class="fa fa-warning"></i>')
    .attr("title", "OctoRelay: important notice")
    .off("click")
    .on("click", handleClick)
    .show();
});
