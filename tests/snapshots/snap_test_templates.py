# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestTemplates::test_templates octorelay_navbar.jinja2'] = '''
    <a id="relaisr1" title="relay 1" role="button" style="display: none">
        R1
    </a>

    <a id="relaisr2" title="relay 2" role="button" style="display: none">
        R2
    </a>

    <a id="relaisr3" title="relay 3" role="button" style="display: none">
        R3
    </a>

    <a id="relaisr4" title="relay 4" role="button" style="display: none">
        R4
    </a>

    <a id="relaisr5" title="relay 5" role="button" style="display: none">
        R5
    </a>

    <a id="relaisr6" title="relay 6" role="button" style="display: none">
        R6
    </a>

    <a id="relaisr7" title="relay 7" role="button" style="display: none">
        R7
    </a>

    <a id="relaisr8" title="relay 8" role="button" style="display: none">
        R8
    </a>


<div id="octorelay-confirmation-dialog" class="modal hide fade">
    <div class="modal-header">
        <a href="#" class="close" data-dismiss="modal" aria-hidden="true">&times;</a>
        <h3 class="modal-title">Turning the relay off</h3>
    </div>
    <div class="modal-body">
        <h4 id="octorelay-confirmation-text">Are you sure?</h4>
    </div>
    <div class="modal-footer">
        <button class="btn btn-cancel" data-dismiss="modal" aria-hidden="true">Cancel</button>
        <button class="btn btn-danger btn-confirm">Confirm</button>
    </div>
</div>'''

snapshots['TestTemplates::test_templates octorelay_settings.jinja2'] = '''<form class="form-horizontal">
    <h3>OctoRelay Settings</h3>
    
    <div class="control-group">
        <label class="control-label">Relay 1</label>
        <div class="controls">
            <label class="checkbox">
                <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r1.active">
                Active
                <span
                    class="help-inline"
                    data-bind="hidden: settings.plugins.octorelay.r1.active, text: settings.plugins.octorelay.r1.label_text"
                    style="line-height: initial; vertical-align: unset;"
                ></span>
            </label>
        </div>
        <div data-bind="visible: settings.plugins.octorelay.r1.active">
            <label class="control-label">Label</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-small" data-bind="value: settings.plugins.octorelay.r1.label_text">
                </label>
            </div>
            <label class="control-label">GPIO Number</label>
            <div class="controls">
                <input id="relay_pin-input1" type="number" min="1" max="27" class="input-small" data-bind="value: settings.plugins.octorelay.r1.relay_pin">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r1.inverted_output">
                    Inverted output
                </label>
            </div>
            <label class="control-label">OS Command ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r1.cmd_on">
                </label>
            </div>
            <label class="control-label">OS Command OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r1.cmd_off">
                </label>
            </div>
            <label class="control-label">Icon ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r1.icon_on">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r1.icon_on"
                    ></div>
                </label>
            </div>
            <label class="control-label">Icon OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r1.icon_off">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r1.icon_off"
                    ></div>
                </label>
            </div>
            <label class="control-label">Confirmation</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r1.confirm_off">
                    Warning on turning OFF
                </label>
            </div>


            <label class="control-label">Startup</label>
            <div class="controls">
                <div class="btn-group" >
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r1.rules.STARTUP.state() === true }">
                        <input type="radio" style="display:none" data-bind="checkedValue: true, checked: settings.plugins.octorelay.r1.rules.STARTUP.state" />
                        ON
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r1.rules.STARTUP.state() === false }">
                        <input type="radio" style="display:none" data-bind="checkedValue: false, checked: settings.plugins.octorelay.r1.rules.STARTUP.state" />
                        OFF
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r1.rules.STARTUP.state() === null }">
                        <input type="radio" style="display:none" data-bind="checkedValue: null, checked: settings.plugins.octorelay.r1.rules.STARTUP.state" />
                        no action
                    </label>
                </div>
            </div>


            <label class="control-label">Auto ON/OFF</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r1.auto_on_before_print">
                    ON before printing
                </label>
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r1.auto_off_after_print">
                    OFF after printing
                </label>
            </div>
            <label class="control-label" data-bind="visible: settings.plugins.octorelay.r1.auto_off_after_print">
                Delay
            </label>
            <div class="controls" data-bind="visible: settings.plugins.octorelay.r1.auto_off_after_print">
                <label class="text">
                    <div class="input-append">
                        <input type="number" min="0" max="86400" class="input-small" data-bind="value: settings.plugins.octorelay.r1.auto_off_delay">
                        <span class="add-on">seconds</span>
                    </div>
                    <span class="help-block">The delay to turn the relay OFF. For example for a fan, that should run a little longer after the print.</span>
                </label>
            </div>
        </div>
    </div>
    
    <div class="control-group">
        <label class="control-label">Relay 2</label>
        <div class="controls">
            <label class="checkbox">
                <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r2.active">
                Active
                <span
                    class="help-inline"
                    data-bind="hidden: settings.plugins.octorelay.r2.active, text: settings.plugins.octorelay.r2.label_text"
                    style="line-height: initial; vertical-align: unset;"
                ></span>
            </label>
        </div>
        <div data-bind="visible: settings.plugins.octorelay.r2.active">
            <label class="control-label">Label</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-small" data-bind="value: settings.plugins.octorelay.r2.label_text">
                </label>
            </div>
            <label class="control-label">GPIO Number</label>
            <div class="controls">
                <input id="relay_pin-input2" type="number" min="1" max="27" class="input-small" data-bind="value: settings.plugins.octorelay.r2.relay_pin">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r2.inverted_output">
                    Inverted output
                </label>
            </div>
            <label class="control-label">OS Command ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r2.cmd_on">
                </label>
            </div>
            <label class="control-label">OS Command OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r2.cmd_off">
                </label>
            </div>
            <label class="control-label">Icon ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r2.icon_on">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r2.icon_on"
                    ></div>
                </label>
            </div>
            <label class="control-label">Icon OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r2.icon_off">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r2.icon_off"
                    ></div>
                </label>
            </div>
            <label class="control-label">Confirmation</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r2.confirm_off">
                    Warning on turning OFF
                </label>
            </div>


            <label class="control-label">Startup</label>
            <div class="controls">
                <div class="btn-group" >
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r2.rules.STARTUP.state() === true }">
                        <input type="radio" style="display:none" data-bind="checkedValue: true, checked: settings.plugins.octorelay.r2.rules.STARTUP.state" />
                        ON
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r2.rules.STARTUP.state() === false }">
                        <input type="radio" style="display:none" data-bind="checkedValue: false, checked: settings.plugins.octorelay.r2.rules.STARTUP.state" />
                        OFF
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r2.rules.STARTUP.state() === null }">
                        <input type="radio" style="display:none" data-bind="checkedValue: null, checked: settings.plugins.octorelay.r2.rules.STARTUP.state" />
                        no action
                    </label>
                </div>
            </div>


            <label class="control-label">Auto ON/OFF</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r2.auto_on_before_print">
                    ON before printing
                </label>
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r2.auto_off_after_print">
                    OFF after printing
                </label>
            </div>
            <label class="control-label" data-bind="visible: settings.plugins.octorelay.r2.auto_off_after_print">
                Delay
            </label>
            <div class="controls" data-bind="visible: settings.plugins.octorelay.r2.auto_off_after_print">
                <label class="text">
                    <div class="input-append">
                        <input type="number" min="0" max="86400" class="input-small" data-bind="value: settings.plugins.octorelay.r2.auto_off_delay">
                        <span class="add-on">seconds</span>
                    </div>
                    <span class="help-block">The delay to turn the relay OFF. For example for a fan, that should run a little longer after the print.</span>
                </label>
            </div>
        </div>
    </div>
    
    <div class="control-group">
        <label class="control-label">Relay 3</label>
        <div class="controls">
            <label class="checkbox">
                <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r3.active">
                Active
                <span
                    class="help-inline"
                    data-bind="hidden: settings.plugins.octorelay.r3.active, text: settings.plugins.octorelay.r3.label_text"
                    style="line-height: initial; vertical-align: unset;"
                ></span>
            </label>
        </div>
        <div data-bind="visible: settings.plugins.octorelay.r3.active">
            <label class="control-label">Label</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-small" data-bind="value: settings.plugins.octorelay.r3.label_text">
                </label>
            </div>
            <label class="control-label">GPIO Number</label>
            <div class="controls">
                <input id="relay_pin-input3" type="number" min="1" max="27" class="input-small" data-bind="value: settings.plugins.octorelay.r3.relay_pin">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r3.inverted_output">
                    Inverted output
                </label>
            </div>
            <label class="control-label">OS Command ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r3.cmd_on">
                </label>
            </div>
            <label class="control-label">OS Command OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r3.cmd_off">
                </label>
            </div>
            <label class="control-label">Icon ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r3.icon_on">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r3.icon_on"
                    ></div>
                </label>
            </div>
            <label class="control-label">Icon OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r3.icon_off">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r3.icon_off"
                    ></div>
                </label>
            </div>
            <label class="control-label">Confirmation</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r3.confirm_off">
                    Warning on turning OFF
                </label>
            </div>


            <label class="control-label">Startup</label>
            <div class="controls">
                <div class="btn-group" >
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r3.rules.STARTUP.state() === true }">
                        <input type="radio" style="display:none" data-bind="checkedValue: true, checked: settings.plugins.octorelay.r3.rules.STARTUP.state" />
                        ON
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r3.rules.STARTUP.state() === false }">
                        <input type="radio" style="display:none" data-bind="checkedValue: false, checked: settings.plugins.octorelay.r3.rules.STARTUP.state" />
                        OFF
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r3.rules.STARTUP.state() === null }">
                        <input type="radio" style="display:none" data-bind="checkedValue: null, checked: settings.plugins.octorelay.r3.rules.STARTUP.state" />
                        no action
                    </label>
                </div>
            </div>


            <label class="control-label">Auto ON/OFF</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r3.auto_on_before_print">
                    ON before printing
                </label>
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r3.auto_off_after_print">
                    OFF after printing
                </label>
            </div>
            <label class="control-label" data-bind="visible: settings.plugins.octorelay.r3.auto_off_after_print">
                Delay
            </label>
            <div class="controls" data-bind="visible: settings.plugins.octorelay.r3.auto_off_after_print">
                <label class="text">
                    <div class="input-append">
                        <input type="number" min="0" max="86400" class="input-small" data-bind="value: settings.plugins.octorelay.r3.auto_off_delay">
                        <span class="add-on">seconds</span>
                    </div>
                    <span class="help-block">The delay to turn the relay OFF. For example for a fan, that should run a little longer after the print.</span>
                </label>
            </div>
        </div>
    </div>
    
    <div class="control-group">
        <label class="control-label">Relay 4</label>
        <div class="controls">
            <label class="checkbox">
                <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r4.active">
                Active
                <span
                    class="help-inline"
                    data-bind="hidden: settings.plugins.octorelay.r4.active, text: settings.plugins.octorelay.r4.label_text"
                    style="line-height: initial; vertical-align: unset;"
                ></span>
            </label>
        </div>
        <div data-bind="visible: settings.plugins.octorelay.r4.active">
            <label class="control-label">Label</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-small" data-bind="value: settings.plugins.octorelay.r4.label_text">
                </label>
            </div>
            <label class="control-label">GPIO Number</label>
            <div class="controls">
                <input id="relay_pin-input4" type="number" min="1" max="27" class="input-small" data-bind="value: settings.plugins.octorelay.r4.relay_pin">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r4.inverted_output">
                    Inverted output
                </label>
            </div>
            <label class="control-label">OS Command ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r4.cmd_on">
                </label>
            </div>
            <label class="control-label">OS Command OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r4.cmd_off">
                </label>
            </div>
            <label class="control-label">Icon ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r4.icon_on">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r4.icon_on"
                    ></div>
                </label>
            </div>
            <label class="control-label">Icon OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r4.icon_off">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r4.icon_off"
                    ></div>
                </label>
            </div>
            <label class="control-label">Confirmation</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r4.confirm_off">
                    Warning on turning OFF
                </label>
            </div>


            <label class="control-label">Startup</label>
            <div class="controls">
                <div class="btn-group" >
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r4.rules.STARTUP.state() === true }">
                        <input type="radio" style="display:none" data-bind="checkedValue: true, checked: settings.plugins.octorelay.r4.rules.STARTUP.state" />
                        ON
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r4.rules.STARTUP.state() === false }">
                        <input type="radio" style="display:none" data-bind="checkedValue: false, checked: settings.plugins.octorelay.r4.rules.STARTUP.state" />
                        OFF
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r4.rules.STARTUP.state() === null }">
                        <input type="radio" style="display:none" data-bind="checkedValue: null, checked: settings.plugins.octorelay.r4.rules.STARTUP.state" />
                        no action
                    </label>
                </div>
            </div>


            <label class="control-label">Auto ON/OFF</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r4.auto_on_before_print">
                    ON before printing
                </label>
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r4.auto_off_after_print">
                    OFF after printing
                </label>
            </div>
            <label class="control-label" data-bind="visible: settings.plugins.octorelay.r4.auto_off_after_print">
                Delay
            </label>
            <div class="controls" data-bind="visible: settings.plugins.octorelay.r4.auto_off_after_print">
                <label class="text">
                    <div class="input-append">
                        <input type="number" min="0" max="86400" class="input-small" data-bind="value: settings.plugins.octorelay.r4.auto_off_delay">
                        <span class="add-on">seconds</span>
                    </div>
                    <span class="help-block">The delay to turn the relay OFF. For example for a fan, that should run a little longer after the print.</span>
                </label>
            </div>
        </div>
    </div>
    
    <div class="control-group">
        <label class="control-label">Relay 5</label>
        <div class="controls">
            <label class="checkbox">
                <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r5.active">
                Active
                <span
                    class="help-inline"
                    data-bind="hidden: settings.plugins.octorelay.r5.active, text: settings.plugins.octorelay.r5.label_text"
                    style="line-height: initial; vertical-align: unset;"
                ></span>
            </label>
        </div>
        <div data-bind="visible: settings.plugins.octorelay.r5.active">
            <label class="control-label">Label</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-small" data-bind="value: settings.plugins.octorelay.r5.label_text">
                </label>
            </div>
            <label class="control-label">GPIO Number</label>
            <div class="controls">
                <input id="relay_pin-input5" type="number" min="1" max="27" class="input-small" data-bind="value: settings.plugins.octorelay.r5.relay_pin">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r5.inverted_output">
                    Inverted output
                </label>
            </div>
            <label class="control-label">OS Command ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r5.cmd_on">
                </label>
            </div>
            <label class="control-label">OS Command OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r5.cmd_off">
                </label>
            </div>
            <label class="control-label">Icon ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r5.icon_on">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r5.icon_on"
                    ></div>
                </label>
            </div>
            <label class="control-label">Icon OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r5.icon_off">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r5.icon_off"
                    ></div>
                </label>
            </div>
            <label class="control-label">Confirmation</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r5.confirm_off">
                    Warning on turning OFF
                </label>
            </div>


            <label class="control-label">Startup</label>
            <div class="controls">
                <div class="btn-group" >
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r5.rules.STARTUP.state() === true }">
                        <input type="radio" style="display:none" data-bind="checkedValue: true, checked: settings.plugins.octorelay.r5.rules.STARTUP.state" />
                        ON
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r5.rules.STARTUP.state() === false }">
                        <input type="radio" style="display:none" data-bind="checkedValue: false, checked: settings.plugins.octorelay.r5.rules.STARTUP.state" />
                        OFF
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r5.rules.STARTUP.state() === null }">
                        <input type="radio" style="display:none" data-bind="checkedValue: null, checked: settings.plugins.octorelay.r5.rules.STARTUP.state" />
                        no action
                    </label>
                </div>
            </div>


            <label class="control-label">Auto ON/OFF</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r5.auto_on_before_print">
                    ON before printing
                </label>
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r5.auto_off_after_print">
                    OFF after printing
                </label>
            </div>
            <label class="control-label" data-bind="visible: settings.plugins.octorelay.r5.auto_off_after_print">
                Delay
            </label>
            <div class="controls" data-bind="visible: settings.plugins.octorelay.r5.auto_off_after_print">
                <label class="text">
                    <div class="input-append">
                        <input type="number" min="0" max="86400" class="input-small" data-bind="value: settings.plugins.octorelay.r5.auto_off_delay">
                        <span class="add-on">seconds</span>
                    </div>
                    <span class="help-block">The delay to turn the relay OFF. For example for a fan, that should run a little longer after the print.</span>
                </label>
            </div>
        </div>
    </div>
    
    <div class="control-group">
        <label class="control-label">Relay 6</label>
        <div class="controls">
            <label class="checkbox">
                <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r6.active">
                Active
                <span
                    class="help-inline"
                    data-bind="hidden: settings.plugins.octorelay.r6.active, text: settings.plugins.octorelay.r6.label_text"
                    style="line-height: initial; vertical-align: unset;"
                ></span>
            </label>
        </div>
        <div data-bind="visible: settings.plugins.octorelay.r6.active">
            <label class="control-label">Label</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-small" data-bind="value: settings.plugins.octorelay.r6.label_text">
                </label>
            </div>
            <label class="control-label">GPIO Number</label>
            <div class="controls">
                <input id="relay_pin-input6" type="number" min="1" max="27" class="input-small" data-bind="value: settings.plugins.octorelay.r6.relay_pin">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r6.inverted_output">
                    Inverted output
                </label>
            </div>
            <label class="control-label">OS Command ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r6.cmd_on">
                </label>
            </div>
            <label class="control-label">OS Command OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r6.cmd_off">
                </label>
            </div>
            <label class="control-label">Icon ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r6.icon_on">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r6.icon_on"
                    ></div>
                </label>
            </div>
            <label class="control-label">Icon OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r6.icon_off">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r6.icon_off"
                    ></div>
                </label>
            </div>
            <label class="control-label">Confirmation</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r6.confirm_off">
                    Warning on turning OFF
                </label>
            </div>


            <label class="control-label">Startup</label>
            <div class="controls">
                <div class="btn-group" >
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r6.rules.STARTUP.state() === true }">
                        <input type="radio" style="display:none" data-bind="checkedValue: true, checked: settings.plugins.octorelay.r6.rules.STARTUP.state" />
                        ON
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r6.rules.STARTUP.state() === false }">
                        <input type="radio" style="display:none" data-bind="checkedValue: false, checked: settings.plugins.octorelay.r6.rules.STARTUP.state" />
                        OFF
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r6.rules.STARTUP.state() === null }">
                        <input type="radio" style="display:none" data-bind="checkedValue: null, checked: settings.plugins.octorelay.r6.rules.STARTUP.state" />
                        no action
                    </label>
                </div>
            </div>


            <label class="control-label">Auto ON/OFF</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r6.auto_on_before_print">
                    ON before printing
                </label>
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r6.auto_off_after_print">
                    OFF after printing
                </label>
            </div>
            <label class="control-label" data-bind="visible: settings.plugins.octorelay.r6.auto_off_after_print">
                Delay
            </label>
            <div class="controls" data-bind="visible: settings.plugins.octorelay.r6.auto_off_after_print">
                <label class="text">
                    <div class="input-append">
                        <input type="number" min="0" max="86400" class="input-small" data-bind="value: settings.plugins.octorelay.r6.auto_off_delay">
                        <span class="add-on">seconds</span>
                    </div>
                    <span class="help-block">The delay to turn the relay OFF. For example for a fan, that should run a little longer after the print.</span>
                </label>
            </div>
        </div>
    </div>
    
    <div class="control-group">
        <label class="control-label">Relay 7</label>
        <div class="controls">
            <label class="checkbox">
                <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r7.active">
                Active
                <span
                    class="help-inline"
                    data-bind="hidden: settings.plugins.octorelay.r7.active, text: settings.plugins.octorelay.r7.label_text"
                    style="line-height: initial; vertical-align: unset;"
                ></span>
            </label>
        </div>
        <div data-bind="visible: settings.plugins.octorelay.r7.active">
            <label class="control-label">Label</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-small" data-bind="value: settings.plugins.octorelay.r7.label_text">
                </label>
            </div>
            <label class="control-label">GPIO Number</label>
            <div class="controls">
                <input id="relay_pin-input7" type="number" min="1" max="27" class="input-small" data-bind="value: settings.plugins.octorelay.r7.relay_pin">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r7.inverted_output">
                    Inverted output
                </label>
            </div>
            <label class="control-label">OS Command ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r7.cmd_on">
                </label>
            </div>
            <label class="control-label">OS Command OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r7.cmd_off">
                </label>
            </div>
            <label class="control-label">Icon ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r7.icon_on">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r7.icon_on"
                    ></div>
                </label>
            </div>
            <label class="control-label">Icon OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r7.icon_off">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r7.icon_off"
                    ></div>
                </label>
            </div>
            <label class="control-label">Confirmation</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r7.confirm_off">
                    Warning on turning OFF
                </label>
            </div>


            <label class="control-label">Startup</label>
            <div class="controls">
                <div class="btn-group" >
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r7.rules.STARTUP.state() === true }">
                        <input type="radio" style="display:none" data-bind="checkedValue: true, checked: settings.plugins.octorelay.r7.rules.STARTUP.state" />
                        ON
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r7.rules.STARTUP.state() === false }">
                        <input type="radio" style="display:none" data-bind="checkedValue: false, checked: settings.plugins.octorelay.r7.rules.STARTUP.state" />
                        OFF
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r7.rules.STARTUP.state() === null }">
                        <input type="radio" style="display:none" data-bind="checkedValue: null, checked: settings.plugins.octorelay.r7.rules.STARTUP.state" />
                        no action
                    </label>
                </div>
            </div>


            <label class="control-label">Auto ON/OFF</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r7.auto_on_before_print">
                    ON before printing
                </label>
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r7.auto_off_after_print">
                    OFF after printing
                </label>
            </div>
            <label class="control-label" data-bind="visible: settings.plugins.octorelay.r7.auto_off_after_print">
                Delay
            </label>
            <div class="controls" data-bind="visible: settings.plugins.octorelay.r7.auto_off_after_print">
                <label class="text">
                    <div class="input-append">
                        <input type="number" min="0" max="86400" class="input-small" data-bind="value: settings.plugins.octorelay.r7.auto_off_delay">
                        <span class="add-on">seconds</span>
                    </div>
                    <span class="help-block">The delay to turn the relay OFF. For example for a fan, that should run a little longer after the print.</span>
                </label>
            </div>
        </div>
    </div>
    
    <div class="control-group">
        <label class="control-label">Relay 8</label>
        <div class="controls">
            <label class="checkbox">
                <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r8.active">
                Active
                <span
                    class="help-inline"
                    data-bind="hidden: settings.plugins.octorelay.r8.active, text: settings.plugins.octorelay.r8.label_text"
                    style="line-height: initial; vertical-align: unset;"
                ></span>
            </label>
        </div>
        <div data-bind="visible: settings.plugins.octorelay.r8.active">
            <label class="control-label">Label</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-small" data-bind="value: settings.plugins.octorelay.r8.label_text">
                </label>
            </div>
            <label class="control-label">GPIO Number</label>
            <div class="controls">
                <input id="relay_pin-input8" type="number" min="1" max="27" class="input-small" data-bind="value: settings.plugins.octorelay.r8.relay_pin">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r8.inverted_output">
                    Inverted output
                </label>
            </div>
            <label class="control-label">OS Command ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r8.cmd_on">
                </label>
            </div>
            <label class="control-label">OS Command OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r8.cmd_off">
                </label>
            </div>
            <label class="control-label">Icon ON</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r8.icon_on">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r8.icon_on"
                    ></div>
                </label>
            </div>
            <label class="control-label">Icon OFF</label>
            <div class="controls">
                <label class="text">
                    <input type="text" class="input-large" data-bind="value: settings.plugins.octorelay.r8.icon_off">
                    <div
                        style="display: inline-block; width: 24px; height: 24px; margin-left: 8px; overflow: hidden; line-height: unset; vertical-align: middle; font-size: 1.3em;"
                        data-bind="html: settings.plugins.octorelay.r8.icon_off"
                    ></div>
                </label>
            </div>
            <label class="control-label">Confirmation</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r8.confirm_off">
                    Warning on turning OFF
                </label>
            </div>


            <label class="control-label">Startup</label>
            <div class="controls">
                <div class="btn-group" >
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r8.rules.STARTUP.state() === true }">
                        <input type="radio" style="display:none" data-bind="checkedValue: true, checked: settings.plugins.octorelay.r8.rules.STARTUP.state" />
                        ON
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r8.rules.STARTUP.state() === false }">
                        <input type="radio" style="display:none" data-bind="checkedValue: false, checked: settings.plugins.octorelay.r8.rules.STARTUP.state" />
                        OFF
                    </label>
                    <label class="btn btn-default" data-bind="css: { active: settings.plugins.octorelay.r8.rules.STARTUP.state() === null }">
                        <input type="radio" style="display:none" data-bind="checkedValue: null, checked: settings.plugins.octorelay.r8.rules.STARTUP.state" />
                        no action
                    </label>
                </div>
            </div>


            <label class="control-label">Auto ON/OFF</label>
            <div class="controls">
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r8.auto_on_before_print">
                    ON before printing
                </label>
                <label class="checkbox">
                    <input type="checkbox" data-bind="checked: settings.plugins.octorelay.r8.auto_off_after_print">
                    OFF after printing
                </label>
            </div>
            <label class="control-label" data-bind="visible: settings.plugins.octorelay.r8.auto_off_after_print">
                Delay
            </label>
            <div class="controls" data-bind="visible: settings.plugins.octorelay.r8.auto_off_after_print">
                <label class="text">
                    <div class="input-append">
                        <input type="number" min="0" max="86400" class="input-small" data-bind="value: settings.plugins.octorelay.r8.auto_off_delay">
                        <span class="add-on">seconds</span>
                    </div>
                    <span class="help-block">The delay to turn the relay OFF. For example for a fan, that should run a little longer after the print.</span>
                </label>
            </div>
        </div>
    </div>
    
</form>'''
