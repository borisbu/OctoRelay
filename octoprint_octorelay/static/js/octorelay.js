$(function() {
    function OctoRelayViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0]
        self.loginState = parameters[1];



        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "octorelay") {
                return;
            }
            //console.log("onDataUpdaterPluginMessage: "+JSON.stringify(data));

            for (const [key, value] of Object.entries(data)) {
                //console.log(JSON.stringify(key));
                //console.log(JSON.stringify(value));

                if (value.active !== undefined) {

                    if(value.active == 1) {
                        $("#relais"+key).show();
                    } else {
                        $("#relais"+key).hide();
                    }

                }
                if (value.iconText !== undefined) {
                    $("#isONicon"+key).html(value.iconText);
                }
                if (value.labelText !== undefined) {
                    $("#isONlabel"+key).html(value.labelText);
                }
            }


        };

    }
    OCTOPRINT_VIEWMODELS.push({
        construct: OctoRelayViewModel,
        dependencies: ["settingsViewModel","loginStateViewModel"],
    });
});
