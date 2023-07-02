type MessageHandler = (plugin: string, data: object) => void;
type PluginViewModel = (this: PluginViewModel & {
  settingsViewModel: object,
  loginState: object,
  onDataUpdaterPluginMessage: MessageHandler
}, dependencies: object[]) => void;

$(function () {
  const OctoRelayViewModel: PluginViewModel = function (
    this,
    [settingsViewModel, loginStateViewModel]
  ) {
    const self = this;
    self.settingsViewModel = settingsViewModel;
    self.loginState = loginStateViewModel;

    self.onDataUpdaterPluginMessage = (plugin, data) => {
      if (plugin !== "octorelay") {
        return;
      }
      for (const [key, value] of Object.entries(data)) {
        const btn = $("#relais" + key);
        if (value.active !== undefined) {
          btn.toggle(value.active === 1)
        }
        const icon = $("#ralayIcon" + key);
        if (value.iconText !== undefined) {
          icon.html(value.iconText);
        }
        if (value.labelText !== undefined) {
          icon.attr("title", value.labelText);
        }
        if (value.confirmOff !== undefined) {
          icon.attr("data-confirm", value.confirmOff);
        }
      }
    };
  }

  OCTOPRINT_VIEWMODELS.push({
    construct: OctoRelayViewModel,
    dependencies: ["settingsViewModel", "loginStateViewModel"],
  });
});
