/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { FormStatusIndicator } from "@web/views/form/form_status_indicator/form_status_indicator"
import {useSetupView} from "@web/views/view_hook";
import {ListController} from "@web/views/list/list_controller";
const {useRef, toRaw} = owl;
import core from "web.core";
var _t = core._t;
import { patch } from "@web/core/utils/patch";
var sh_disable_auto_edit_model = false
var rpc = require('web.rpc');
var session = require('web.session');






const oldSetup = FormController.prototype.setup;
const oldonPagerUpdated = FormController.prototype.onPagerUpdate;



rpc.query({
    model: 'res.users',
    method: 'search_read',
    fields: ['sh_disable_auto_edit_model'],
    domain: [['id', '=', session.uid]]
}, { async: false }).then(function (data) {
    if (data) {
        _.each(data, function (user) {
            if (user.sh_disable_auto_edit_model) {
                sh_disable_auto_edit_model = user.sh_disable_auto_edit_model
            }
        });

    }
});



const Formsetup = function () {
    const rootRef = useRef("root");
    useSetupView({
        beforeLeave: () => {
            if (this.model.root.isDirty && sh_disable_auto_edit_model) {
                if (confirm("Do you want to save changes Automatically?")) {
                    return this.model.root.save({noReload: true, stayInEdition: true});
                } else {
                    this.model.root.discard();
                    return true;
                }
                //return this.model.root.save({ noReload: true, stayInEdition: true });
            }
        },
    });
    const result = oldSetup.apply(this, arguments);
    return result;
};
FormController.prototype.setup = Formsetup;

const onPagerUpdate = await function () {
    this.model.root.askChanges();

    if (this.model.root.isDirty && sh_disable_auto_edit_model) {
        if (confirm("Do you want to save changes Automatically?")) {
            return oldonPagerUpdated.apply(this, arguments);
        }
        this.model.root.discard();
    }
    return oldonPagerUpdated.apply(this, arguments);
};

//assign setup to FormController

FormController.prototype.onPagerUpdate = onPagerUpdate;

// FormStatusIndicator.template = 'web_no_auto_save.FormStatusIndicator';

const ListSuper = ListController.prototype.setup;
const Listsetup = function () {

    useSetupView({
        rootRef: this.rootRef,
        beforeLeave: () => {
            const list = this.model.root;
            const editedRecord = list.editedRecord;
            if (editedRecord && editedRecord.isDirty && sh_disable_auto_edit_model) {
                if (confirm("Do you want to save changes Automatically?")) {
                    if (!list.unselectRecord(true)) {
                        throw new Error("View can't be saved");
                    }
                } else {
                    this.onClickDiscard();
                    return true;
                }
            }
        },
    });
    const result = ListSuper.apply(this, arguments);
    return result;
};
ListController.prototype.setup = Listsetup;

