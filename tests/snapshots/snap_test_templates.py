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

    <ul class="nav nav-pills">
        
        <li data-bind="css: { active: 1 === 1 }, using: settings.plugins.octorelay.r1">
            <a
                href="#relay_settings_1"
                data-bind="text: label_text() || \'Relay 1\'"
                data-toggle="tab"
            ></a>
        </li>
        
        <li data-bind="css: { active: 1 === 2 }, using: settings.plugins.octorelay.r2">
            <a
                href="#relay_settings_2"
                data-bind="text: label_text() || \'Relay 2\'"
                data-toggle="tab"
            ></a>
        </li>
        
        <li data-bind="css: { active: 1 === 3 }, using: settings.plugins.octorelay.r3">
            <a
                href="#relay_settings_3"
                data-bind="text: label_text() || \'Relay 3\'"
                data-toggle="tab"
            ></a>
        </li>
        
        <li data-bind="css: { active: 1 === 4 }, using: settings.plugins.octorelay.r4">
            <a
                href="#relay_settings_4"
                data-bind="text: label_text() || \'Relay 4\'"
                data-toggle="tab"
            ></a>
        </li>
        
        <li data-bind="css: { active: 1 === 5 }, using: settings.plugins.octorelay.r5">
            <a
                href="#relay_settings_5"
                data-bind="text: label_text() || \'Relay 5\'"
                data-toggle="tab"
            ></a>
        </li>
        
        <li data-bind="css: { active: 1 === 6 }, using: settings.plugins.octorelay.r6">
            <a
                href="#relay_settings_6"
                data-bind="text: label_text() || \'Relay 6\'"
                data-toggle="tab"
            ></a>
        </li>
        
        <li data-bind="css: { active: 1 === 7 }, using: settings.plugins.octorelay.r7">
            <a
                href="#relay_settings_7"
                data-bind="text: label_text() || \'Relay 7\'"
                data-toggle="tab"
            ></a>
        </li>
        
        <li data-bind="css: { active: 1 === 8 }, using: settings.plugins.octorelay.r8">
            <a
                href="#relay_settings_8"
                data-bind="text: label_text() || \'Relay 8\'"
                data-toggle="tab"
            ></a>
        </li>
        
    </ul>

    <div class="tab-content">
        
        <div
            id="relay_settings_1"
            class="tab-pane fade"
            data-bind="css: { \'active in\': 1 === 1 }, using: settings.plugins.octorelay.r1"
        >
            <div class="control-group">
                <label class="control-label">Active</label>
                <div class="controls">
                    <div class="btn-group">
                        
                        <!--ko let: { classBinding: {
                            'active btn-info': active() === true,
                            'btn-default': active() !== true
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: true, checked: active"
                            />
                            YES
                        </label>
                        <!--/ko-->
                        
                        <!--ko let: { classBinding: {
                            'active btn-default': active() === false,
                            'btn-default': active() !== false
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: false, checked: active"
                            />
                            NO
                        </label>
                        <!--/ko-->
                        
                    </div>
                    <span class="help-block" data-bind="hidden: active">
                        All operations on this relay are disabled
                    </span>
                </div>
            </div>

            <div data-bind="visible: active">
                
                <div class="preview" style="left: 315px;" data-bind="html: icon_on"></div>
                <div class="preview-caption" style="left: 315px">
                    <span class="label">ON</span>
                    preview
                </div>
                
                <div class="preview" style="left: 415px;" data-bind="html: icon_off"></div>
                <div class="preview-caption" style="left: 415px">
                    <span class="label">OFF</span>
                    preview
                </div>
                

                <div class="control-group">
                    <label class="control-label">Label</label>
                    <div class="controls">
                        <input type="text" class="input-small" data-bind="value: label_text">
                    </div>
                </div>

                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_off"
                            >
                        </div>
                    </div>
                </div>
                

                <div class="control-group">
                    <label class="control-label">GPIO Number</label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on tiny">BCM</span>
                            <input
                                id="relay_pin-input1"
                                type="number"
                                min="1"
                                max="27"
                                class="input-mini"
                                data-bind="value: relay_pin"
                            >
                        </div>
                        <span class="help-inline">
                            <a href="https://pinout.xyz/" target="_blank" class="same-color">
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Inverted output</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': inverted_output() === true,
                                'btn-default': inverted_output() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: inverted_output"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': inverted_output() === false,
                                'btn-default': inverted_output() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: inverted_output"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <span class="help-inline">
                            For normally closed relays
                            <a
                                href="https://www.google.com/search?q=what+normally+closed+relay+is"
                                target="_blank"
                                class="same-color"
                            >
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">
                        Warn if turning
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': confirm_off() === true,
                                'btn-default': confirm_off() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: confirm_off"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': confirm_off() === false,
                                'btn-default': confirm_off() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: confirm_off"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Alert on switches ahead</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': show_upcoming() === true,
                                'btn-default': show_upcoming() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: show_upcoming"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': show_upcoming() === false,
                                'btn-default': show_upcoming() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: show_upcoming"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                
                <div class="control-group" data-bind="using: rules.STARTUP">
                    <label class="control-label">on Startup</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STARTED">
                    <label class="control-label">on Printing Started</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STOPPED">
                    <label class="control-label">on Printing Stopped</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                

                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_off"
                            >
                        </div>
                    </div>
                </div>
                

            </div>
        </div>
        
        <div
            id="relay_settings_2"
            class="tab-pane fade"
            data-bind="css: { \'active in\': 1 === 2 }, using: settings.plugins.octorelay.r2"
        >
            <div class="control-group">
                <label class="control-label">Active</label>
                <div class="controls">
                    <div class="btn-group">
                        
                        <!--ko let: { classBinding: {
                            'active btn-info': active() === true,
                            'btn-default': active() !== true
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: true, checked: active"
                            />
                            YES
                        </label>
                        <!--/ko-->
                        
                        <!--ko let: { classBinding: {
                            'active btn-default': active() === false,
                            'btn-default': active() !== false
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: false, checked: active"
                            />
                            NO
                        </label>
                        <!--/ko-->
                        
                    </div>
                    <span class="help-block" data-bind="hidden: active">
                        All operations on this relay are disabled
                    </span>
                </div>
            </div>

            <div data-bind="visible: active">
                
                <div class="preview" style="left: 315px;" data-bind="html: icon_on"></div>
                <div class="preview-caption" style="left: 315px">
                    <span class="label">ON</span>
                    preview
                </div>
                
                <div class="preview" style="left: 415px;" data-bind="html: icon_off"></div>
                <div class="preview-caption" style="left: 415px">
                    <span class="label">OFF</span>
                    preview
                </div>
                

                <div class="control-group">
                    <label class="control-label">Label</label>
                    <div class="controls">
                        <input type="text" class="input-small" data-bind="value: label_text">
                    </div>
                </div>

                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_off"
                            >
                        </div>
                    </div>
                </div>
                

                <div class="control-group">
                    <label class="control-label">GPIO Number</label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on tiny">BCM</span>
                            <input
                                id="relay_pin-input2"
                                type="number"
                                min="1"
                                max="27"
                                class="input-mini"
                                data-bind="value: relay_pin"
                            >
                        </div>
                        <span class="help-inline">
                            <a href="https://pinout.xyz/" target="_blank" class="same-color">
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Inverted output</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': inverted_output() === true,
                                'btn-default': inverted_output() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: inverted_output"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': inverted_output() === false,
                                'btn-default': inverted_output() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: inverted_output"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <span class="help-inline">
                            For normally closed relays
                            <a
                                href="https://www.google.com/search?q=what+normally+closed+relay+is"
                                target="_blank"
                                class="same-color"
                            >
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">
                        Warn if turning
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': confirm_off() === true,
                                'btn-default': confirm_off() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: confirm_off"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': confirm_off() === false,
                                'btn-default': confirm_off() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: confirm_off"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Alert on switches ahead</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': show_upcoming() === true,
                                'btn-default': show_upcoming() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: show_upcoming"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': show_upcoming() === false,
                                'btn-default': show_upcoming() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: show_upcoming"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                
                <div class="control-group" data-bind="using: rules.STARTUP">
                    <label class="control-label">on Startup</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STARTED">
                    <label class="control-label">on Printing Started</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STOPPED">
                    <label class="control-label">on Printing Stopped</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                

                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_off"
                            >
                        </div>
                    </div>
                </div>
                

            </div>
        </div>
        
        <div
            id="relay_settings_3"
            class="tab-pane fade"
            data-bind="css: { \'active in\': 1 === 3 }, using: settings.plugins.octorelay.r3"
        >
            <div class="control-group">
                <label class="control-label">Active</label>
                <div class="controls">
                    <div class="btn-group">
                        
                        <!--ko let: { classBinding: {
                            'active btn-info': active() === true,
                            'btn-default': active() !== true
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: true, checked: active"
                            />
                            YES
                        </label>
                        <!--/ko-->
                        
                        <!--ko let: { classBinding: {
                            'active btn-default': active() === false,
                            'btn-default': active() !== false
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: false, checked: active"
                            />
                            NO
                        </label>
                        <!--/ko-->
                        
                    </div>
                    <span class="help-block" data-bind="hidden: active">
                        All operations on this relay are disabled
                    </span>
                </div>
            </div>

            <div data-bind="visible: active">
                
                <div class="preview" style="left: 315px;" data-bind="html: icon_on"></div>
                <div class="preview-caption" style="left: 315px">
                    <span class="label">ON</span>
                    preview
                </div>
                
                <div class="preview" style="left: 415px;" data-bind="html: icon_off"></div>
                <div class="preview-caption" style="left: 415px">
                    <span class="label">OFF</span>
                    preview
                </div>
                

                <div class="control-group">
                    <label class="control-label">Label</label>
                    <div class="controls">
                        <input type="text" class="input-small" data-bind="value: label_text">
                    </div>
                </div>

                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_off"
                            >
                        </div>
                    </div>
                </div>
                

                <div class="control-group">
                    <label class="control-label">GPIO Number</label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on tiny">BCM</span>
                            <input
                                id="relay_pin-input3"
                                type="number"
                                min="1"
                                max="27"
                                class="input-mini"
                                data-bind="value: relay_pin"
                            >
                        </div>
                        <span class="help-inline">
                            <a href="https://pinout.xyz/" target="_blank" class="same-color">
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Inverted output</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': inverted_output() === true,
                                'btn-default': inverted_output() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: inverted_output"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': inverted_output() === false,
                                'btn-default': inverted_output() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: inverted_output"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <span class="help-inline">
                            For normally closed relays
                            <a
                                href="https://www.google.com/search?q=what+normally+closed+relay+is"
                                target="_blank"
                                class="same-color"
                            >
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">
                        Warn if turning
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': confirm_off() === true,
                                'btn-default': confirm_off() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: confirm_off"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': confirm_off() === false,
                                'btn-default': confirm_off() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: confirm_off"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Alert on switches ahead</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': show_upcoming() === true,
                                'btn-default': show_upcoming() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: show_upcoming"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': show_upcoming() === false,
                                'btn-default': show_upcoming() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: show_upcoming"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                
                <div class="control-group" data-bind="using: rules.STARTUP">
                    <label class="control-label">on Startup</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STARTED">
                    <label class="control-label">on Printing Started</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STOPPED">
                    <label class="control-label">on Printing Stopped</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                

                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_off"
                            >
                        </div>
                    </div>
                </div>
                

            </div>
        </div>
        
        <div
            id="relay_settings_4"
            class="tab-pane fade"
            data-bind="css: { \'active in\': 1 === 4 }, using: settings.plugins.octorelay.r4"
        >
            <div class="control-group">
                <label class="control-label">Active</label>
                <div class="controls">
                    <div class="btn-group">
                        
                        <!--ko let: { classBinding: {
                            'active btn-info': active() === true,
                            'btn-default': active() !== true
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: true, checked: active"
                            />
                            YES
                        </label>
                        <!--/ko-->
                        
                        <!--ko let: { classBinding: {
                            'active btn-default': active() === false,
                            'btn-default': active() !== false
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: false, checked: active"
                            />
                            NO
                        </label>
                        <!--/ko-->
                        
                    </div>
                    <span class="help-block" data-bind="hidden: active">
                        All operations on this relay are disabled
                    </span>
                </div>
            </div>

            <div data-bind="visible: active">
                
                <div class="preview" style="left: 315px;" data-bind="html: icon_on"></div>
                <div class="preview-caption" style="left: 315px">
                    <span class="label">ON</span>
                    preview
                </div>
                
                <div class="preview" style="left: 415px;" data-bind="html: icon_off"></div>
                <div class="preview-caption" style="left: 415px">
                    <span class="label">OFF</span>
                    preview
                </div>
                

                <div class="control-group">
                    <label class="control-label">Label</label>
                    <div class="controls">
                        <input type="text" class="input-small" data-bind="value: label_text">
                    </div>
                </div>

                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_off"
                            >
                        </div>
                    </div>
                </div>
                

                <div class="control-group">
                    <label class="control-label">GPIO Number</label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on tiny">BCM</span>
                            <input
                                id="relay_pin-input4"
                                type="number"
                                min="1"
                                max="27"
                                class="input-mini"
                                data-bind="value: relay_pin"
                            >
                        </div>
                        <span class="help-inline">
                            <a href="https://pinout.xyz/" target="_blank" class="same-color">
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Inverted output</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': inverted_output() === true,
                                'btn-default': inverted_output() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: inverted_output"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': inverted_output() === false,
                                'btn-default': inverted_output() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: inverted_output"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <span class="help-inline">
                            For normally closed relays
                            <a
                                href="https://www.google.com/search?q=what+normally+closed+relay+is"
                                target="_blank"
                                class="same-color"
                            >
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">
                        Warn if turning
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': confirm_off() === true,
                                'btn-default': confirm_off() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: confirm_off"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': confirm_off() === false,
                                'btn-default': confirm_off() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: confirm_off"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Alert on switches ahead</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': show_upcoming() === true,
                                'btn-default': show_upcoming() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: show_upcoming"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': show_upcoming() === false,
                                'btn-default': show_upcoming() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: show_upcoming"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                
                <div class="control-group" data-bind="using: rules.STARTUP">
                    <label class="control-label">on Startup</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STARTED">
                    <label class="control-label">on Printing Started</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STOPPED">
                    <label class="control-label">on Printing Stopped</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                

                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_off"
                            >
                        </div>
                    </div>
                </div>
                

            </div>
        </div>
        
        <div
            id="relay_settings_5"
            class="tab-pane fade"
            data-bind="css: { \'active in\': 1 === 5 }, using: settings.plugins.octorelay.r5"
        >
            <div class="control-group">
                <label class="control-label">Active</label>
                <div class="controls">
                    <div class="btn-group">
                        
                        <!--ko let: { classBinding: {
                            'active btn-info': active() === true,
                            'btn-default': active() !== true
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: true, checked: active"
                            />
                            YES
                        </label>
                        <!--/ko-->
                        
                        <!--ko let: { classBinding: {
                            'active btn-default': active() === false,
                            'btn-default': active() !== false
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: false, checked: active"
                            />
                            NO
                        </label>
                        <!--/ko-->
                        
                    </div>
                    <span class="help-block" data-bind="hidden: active">
                        All operations on this relay are disabled
                    </span>
                </div>
            </div>

            <div data-bind="visible: active">
                
                <div class="preview" style="left: 315px;" data-bind="html: icon_on"></div>
                <div class="preview-caption" style="left: 315px">
                    <span class="label">ON</span>
                    preview
                </div>
                
                <div class="preview" style="left: 415px;" data-bind="html: icon_off"></div>
                <div class="preview-caption" style="left: 415px">
                    <span class="label">OFF</span>
                    preview
                </div>
                

                <div class="control-group">
                    <label class="control-label">Label</label>
                    <div class="controls">
                        <input type="text" class="input-small" data-bind="value: label_text">
                    </div>
                </div>

                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_off"
                            >
                        </div>
                    </div>
                </div>
                

                <div class="control-group">
                    <label class="control-label">GPIO Number</label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on tiny">BCM</span>
                            <input
                                id="relay_pin-input5"
                                type="number"
                                min="1"
                                max="27"
                                class="input-mini"
                                data-bind="value: relay_pin"
                            >
                        </div>
                        <span class="help-inline">
                            <a href="https://pinout.xyz/" target="_blank" class="same-color">
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Inverted output</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': inverted_output() === true,
                                'btn-default': inverted_output() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: inverted_output"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': inverted_output() === false,
                                'btn-default': inverted_output() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: inverted_output"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <span class="help-inline">
                            For normally closed relays
                            <a
                                href="https://www.google.com/search?q=what+normally+closed+relay+is"
                                target="_blank"
                                class="same-color"
                            >
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">
                        Warn if turning
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': confirm_off() === true,
                                'btn-default': confirm_off() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: confirm_off"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': confirm_off() === false,
                                'btn-default': confirm_off() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: confirm_off"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Alert on switches ahead</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': show_upcoming() === true,
                                'btn-default': show_upcoming() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: show_upcoming"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': show_upcoming() === false,
                                'btn-default': show_upcoming() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: show_upcoming"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                
                <div class="control-group" data-bind="using: rules.STARTUP">
                    <label class="control-label">on Startup</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STARTED">
                    <label class="control-label">on Printing Started</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STOPPED">
                    <label class="control-label">on Printing Stopped</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                

                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_off"
                            >
                        </div>
                    </div>
                </div>
                

            </div>
        </div>
        
        <div
            id="relay_settings_6"
            class="tab-pane fade"
            data-bind="css: { \'active in\': 1 === 6 }, using: settings.plugins.octorelay.r6"
        >
            <div class="control-group">
                <label class="control-label">Active</label>
                <div class="controls">
                    <div class="btn-group">
                        
                        <!--ko let: { classBinding: {
                            'active btn-info': active() === true,
                            'btn-default': active() !== true
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: true, checked: active"
                            />
                            YES
                        </label>
                        <!--/ko-->
                        
                        <!--ko let: { classBinding: {
                            'active btn-default': active() === false,
                            'btn-default': active() !== false
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: false, checked: active"
                            />
                            NO
                        </label>
                        <!--/ko-->
                        
                    </div>
                    <span class="help-block" data-bind="hidden: active">
                        All operations on this relay are disabled
                    </span>
                </div>
            </div>

            <div data-bind="visible: active">
                
                <div class="preview" style="left: 315px;" data-bind="html: icon_on"></div>
                <div class="preview-caption" style="left: 315px">
                    <span class="label">ON</span>
                    preview
                </div>
                
                <div class="preview" style="left: 415px;" data-bind="html: icon_off"></div>
                <div class="preview-caption" style="left: 415px">
                    <span class="label">OFF</span>
                    preview
                </div>
                

                <div class="control-group">
                    <label class="control-label">Label</label>
                    <div class="controls">
                        <input type="text" class="input-small" data-bind="value: label_text">
                    </div>
                </div>

                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_off"
                            >
                        </div>
                    </div>
                </div>
                

                <div class="control-group">
                    <label class="control-label">GPIO Number</label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on tiny">BCM</span>
                            <input
                                id="relay_pin-input6"
                                type="number"
                                min="1"
                                max="27"
                                class="input-mini"
                                data-bind="value: relay_pin"
                            >
                        </div>
                        <span class="help-inline">
                            <a href="https://pinout.xyz/" target="_blank" class="same-color">
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Inverted output</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': inverted_output() === true,
                                'btn-default': inverted_output() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: inverted_output"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': inverted_output() === false,
                                'btn-default': inverted_output() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: inverted_output"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <span class="help-inline">
                            For normally closed relays
                            <a
                                href="https://www.google.com/search?q=what+normally+closed+relay+is"
                                target="_blank"
                                class="same-color"
                            >
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">
                        Warn if turning
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': confirm_off() === true,
                                'btn-default': confirm_off() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: confirm_off"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': confirm_off() === false,
                                'btn-default': confirm_off() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: confirm_off"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Alert on switches ahead</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': show_upcoming() === true,
                                'btn-default': show_upcoming() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: show_upcoming"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': show_upcoming() === false,
                                'btn-default': show_upcoming() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: show_upcoming"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                
                <div class="control-group" data-bind="using: rules.STARTUP">
                    <label class="control-label">on Startup</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STARTED">
                    <label class="control-label">on Printing Started</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STOPPED">
                    <label class="control-label">on Printing Stopped</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                

                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_off"
                            >
                        </div>
                    </div>
                </div>
                

            </div>
        </div>
        
        <div
            id="relay_settings_7"
            class="tab-pane fade"
            data-bind="css: { \'active in\': 1 === 7 }, using: settings.plugins.octorelay.r7"
        >
            <div class="control-group">
                <label class="control-label">Active</label>
                <div class="controls">
                    <div class="btn-group">
                        
                        <!--ko let: { classBinding: {
                            'active btn-info': active() === true,
                            'btn-default': active() !== true
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: true, checked: active"
                            />
                            YES
                        </label>
                        <!--/ko-->
                        
                        <!--ko let: { classBinding: {
                            'active btn-default': active() === false,
                            'btn-default': active() !== false
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: false, checked: active"
                            />
                            NO
                        </label>
                        <!--/ko-->
                        
                    </div>
                    <span class="help-block" data-bind="hidden: active">
                        All operations on this relay are disabled
                    </span>
                </div>
            </div>

            <div data-bind="visible: active">
                
                <div class="preview" style="left: 315px;" data-bind="html: icon_on"></div>
                <div class="preview-caption" style="left: 315px">
                    <span class="label">ON</span>
                    preview
                </div>
                
                <div class="preview" style="left: 415px;" data-bind="html: icon_off"></div>
                <div class="preview-caption" style="left: 415px">
                    <span class="label">OFF</span>
                    preview
                </div>
                

                <div class="control-group">
                    <label class="control-label">Label</label>
                    <div class="controls">
                        <input type="text" class="input-small" data-bind="value: label_text">
                    </div>
                </div>

                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_off"
                            >
                        </div>
                    </div>
                </div>
                

                <div class="control-group">
                    <label class="control-label">GPIO Number</label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on tiny">BCM</span>
                            <input
                                id="relay_pin-input7"
                                type="number"
                                min="1"
                                max="27"
                                class="input-mini"
                                data-bind="value: relay_pin"
                            >
                        </div>
                        <span class="help-inline">
                            <a href="https://pinout.xyz/" target="_blank" class="same-color">
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Inverted output</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': inverted_output() === true,
                                'btn-default': inverted_output() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: inverted_output"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': inverted_output() === false,
                                'btn-default': inverted_output() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: inverted_output"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <span class="help-inline">
                            For normally closed relays
                            <a
                                href="https://www.google.com/search?q=what+normally+closed+relay+is"
                                target="_blank"
                                class="same-color"
                            >
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">
                        Warn if turning
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': confirm_off() === true,
                                'btn-default': confirm_off() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: confirm_off"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': confirm_off() === false,
                                'btn-default': confirm_off() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: confirm_off"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Alert on switches ahead</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': show_upcoming() === true,
                                'btn-default': show_upcoming() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: show_upcoming"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': show_upcoming() === false,
                                'btn-default': show_upcoming() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: show_upcoming"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                
                <div class="control-group" data-bind="using: rules.STARTUP">
                    <label class="control-label">on Startup</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STARTED">
                    <label class="control-label">on Printing Started</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STOPPED">
                    <label class="control-label">on Printing Stopped</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                

                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_off"
                            >
                        </div>
                    </div>
                </div>
                

            </div>
        </div>
        
        <div
            id="relay_settings_8"
            class="tab-pane fade"
            data-bind="css: { \'active in\': 1 === 8 }, using: settings.plugins.octorelay.r8"
        >
            <div class="control-group">
                <label class="control-label">Active</label>
                <div class="controls">
                    <div class="btn-group">
                        
                        <!--ko let: { classBinding: {
                            'active btn-info': active() === true,
                            'btn-default': active() !== true
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: true, checked: active"
                            />
                            YES
                        </label>
                        <!--/ko-->
                        
                        <!--ko let: { classBinding: {
                            'active btn-default': active() === false,
                            'btn-default': active() !== false
                        } } -->
                        <label class="btn" data-bind="css: classBinding">
                            <input
                                type="radio"
                                data-bind="checkedValue: false, checked: active"
                            />
                            NO
                        </label>
                        <!--/ko-->
                        
                    </div>
                    <span class="help-block" data-bind="hidden: active">
                        All operations on this relay are disabled
                    </span>
                </div>
            </div>

            <div data-bind="visible: active">
                
                <div class="preview" style="left: 315px;" data-bind="html: icon_on"></div>
                <div class="preview-caption" style="left: 315px">
                    <span class="label">ON</span>
                    preview
                </div>
                
                <div class="preview" style="left: 415px;" data-bind="html: icon_off"></div>
                <div class="preview-caption" style="left: 415px">
                    <span class="label">OFF</span>
                    preview
                </div>
                

                <div class="control-group">
                    <label class="control-label">Label</label>
                    <div class="controls">
                        <input type="text" class="input-small" data-bind="value: label_text">
                    </div>
                </div>

                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Icon
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-code fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: icon_off"
                            >
                        </div>
                    </div>
                </div>
                

                <div class="control-group">
                    <label class="control-label">GPIO Number</label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on tiny">BCM</span>
                            <input
                                id="relay_pin-input8"
                                type="number"
                                min="1"
                                max="27"
                                class="input-mini"
                                data-bind="value: relay_pin"
                            >
                        </div>
                        <span class="help-inline">
                            <a href="https://pinout.xyz/" target="_blank" class="same-color">
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Inverted output</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': inverted_output() === true,
                                'btn-default': inverted_output() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: inverted_output"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': inverted_output() === false,
                                'btn-default': inverted_output() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: inverted_output"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <span class="help-inline">
                            For normally closed relays
                            <a
                                href="https://www.google.com/search?q=what+normally+closed+relay+is"
                                target="_blank"
                                class="same-color"
                            >
                                <i class="fa fa-info"></i>
                            </a>
                        </span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">
                        Warn if turning
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': confirm_off() === true,
                                'btn-default': confirm_off() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: confirm_off"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': confirm_off() === false,
                                'btn-default': confirm_off() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: confirm_off"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Alert on switches ahead</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-info': show_upcoming() === true,
                                'btn-default': show_upcoming() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: show_upcoming"
                                />
                                YES
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': show_upcoming() === false,
                                'btn-default': show_upcoming() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: show_upcoming"
                                />
                                NO
                            </label>
                            <!--/ko-->
                            
                        </div>
                    </div>
                </div>

                
                <div class="control-group" data-bind="using: rules.STARTUP">
                    <label class="control-label">on Startup</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STARTED">
                    <label class="control-label">on Printing Started</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="control-group" data-bind="using: rules.PRINTING_STOPPED">
                    <label class="control-label">on Printing Stopped</label>
                    <div class="controls">
                        <div class="btn-group">
                            
                            <!--ko let: { classBinding: {
                                'active btn-success': state() === true,
                                'btn-default': state() !== true
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: true, checked: state"
                                />
                                ON
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-default': state() === null,
                                'btn-default': state() !== null
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: null, checked: state"
                                />
                                skip
                            </label>
                            <!--/ko-->
                            
                            <!--ko let: { classBinding: {
                                'active btn-danger': state() === false,
                                'btn-default': state() !== false
                            } } -->
                            <label class="btn" data-bind="css: classBinding">
                                <input
                                    type="radio"
                                    data-bind="checkedValue: false, checked: state"
                                />
                                OFF
                            </label>
                            <!--/ko-->
                            
                        </div>
                        <div class="input-prepend input-append" data-bind="hidden: state() === null">
                            <span class="add-on">delay</span>
                            <input type="number" min="0" max="86400" class="input-mini" data-bind="value: delay">
                            <span class="add-on">s</span>
                        </div>
                    </div>
                </div>
                

                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">ON</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_on"
                            >
                        </div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">
                        Command
                        <span class="label">OFF</span>
                    </label>
                    <div class="controls">
                        <div class="input-prepend">
                            <span class="add-on"><i class="fa fa-terminal fa-sm"></i></span>
                            <input
                                type="text"
                                class="input-xlarge code"
                                data-bind="value: cmd_off"
                            >
                        </div>
                    </div>
                </div>
                

            </div>
        </div>
        
    </div>
</form>'''
