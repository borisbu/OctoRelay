$(function () {
    var OctoRelayViewModel = function (_a) {
        var settingsViewModel = _a[0], loginStateViewModel = _a[1];
        var self = this;
        self.settingsViewModel = settingsViewModel;
        self.loginState = loginStateViewModel;
        self.onDataUpdaterPluginMessage = function (plugin, data) {
            if (plugin !== "octorelay") {
                return;
            }
            for (var _i = 0, _a = Object.entries(data); _i < _a.length; _i++) {
                var _b = _a[_i], key = _b[0], value = _b[1];
                var btn = $("#relais" + key);
                if (value.active !== undefined) {
                    btn.toggle(value.active === 1);
                }
                var icon = $("#ralayIcon" + key);
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
    };
    OCTOPRINT_VIEWMODELS.push({
        construct: OctoRelayViewModel,
        dependencies: ["settingsViewModel", "loginStateViewModel"],
    });
});
