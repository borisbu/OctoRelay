$(function () {
  function OctoRelayViewModel(
    this: typeof OctoRelayViewModel & {
      settingsViewModel: object,
      loginState: object,
      onDataUpdaterPluginMessage: (plugin: string, data: object) => void
    },
    [settingsViewModel, loginStateViewModel]: object[]
  ) {
    const self = this;
    self.settingsViewModel = settingsViewModel;
    self.loginState = loginStateViewModel;

    self.onDataUpdaterPluginMessage = (plugin: string, data: object)=> {
      if (plugin !== "octorelay") {
        return;
      }
      // console.log("onDataUpdaterPluginMessage: " + JSON.stringify(data));
      for (const [key, value] of Object.entries(data)) {
        // console.log(JSON.stringify(key));
        // console.log(JSON.stringify(value));
        const btn = $("#relais" + key);
        if (value.active !== undefined) {
          if (value.active === 1) {
            btn.show();
          } else {
            btn.hide();
          }
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
