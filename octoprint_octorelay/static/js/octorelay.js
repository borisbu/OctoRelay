$(function() {
    function OctoRelayViewModel(parameters) {
        var self = this;
        self.settingsViewModel = parameters[0]
        self.loginState = parameters[1];

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin !== "octorelay") {
                return;
            }
            // console.log("onDataUpdaterPluginMessage: " + JSON.stringify(data));
            for (const [key, value] of Object.entries(data)) {
                // console.log(JSON.stringify(key));
                // console.log(JSON.stringify(value));
                if (value.active !== undefined) {
                    if (value.active === 1) {
                        $("#relais" + key).show();
                    } else {
                        $("#relais" + key).hide();
                    }
                }
                if (value.iconText !== undefined) {
                    $("#ralayIcon" + key).html(value.iconText);
                }
                if (value.labelText !== undefined) {
                    $("#ralayIcon" + key).attr("title", value.labelText);
                }
                if (value.confirmOff !== undefined) {
                    $("#ralayIcon" + key).attr("data-confirm", parseInt(value.confirmOff, 10));
                }
            }
        };
    }

    function OctoRelayConfirmClick(pin, title, confirmOff) {
        // console.log("confirmOff " + confirmOff);
        if (confirmOff === 0) {
            return OctoPrint.simpleApiCommand("octorelay", "update", pin);
        }
        $("#octorelay-confirmation-dialog .modal-title").text("Turning " + title + " off");
        $("#octorelay-confirmation-text").text("Are you sure you want to turn the " + title + " off?")
        $("#octorelay-confirmation-dialog .btn-cancel").off("click").on("click", function() {
            $("#octorelay-confirmation-dialog").modal("hide");
        });
        $("#octorelay-confirmation-dialog .btn-confirm").off("click").on("click", function() {
            OctoPrint.simpleApiCommand("octorelay", "update", pin);
        });
        $("#octorelay-confirmation-dialog").modal("show");
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: OctoRelayViewModel,
        dependencies: ["settingsViewModel", "loginStateViewModel"],
    });
});
