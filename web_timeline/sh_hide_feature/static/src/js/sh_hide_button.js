/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { FormController } from "@web/views/form/form_controller";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import core from "web.core";
var _t = core._t;
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { patch } from "@web/core/utils/patch";
import session from 'web.session';

var group_show_delete = false;
    session?.user_has_group("sh_hide_feature.group_show_delete").then(function (has_group) {
        group_show_delete = has_group;
    });
var group_show_export = false;
session?.user_has_group("sh_hide_feature.group_show_export").then(function (has_group) {
    group_show_export = has_group;
});
var group_show_duplicate = false;
session?.user_has_group("sh_hide_feature.group_show_duplicate").then(function (has_group) {
    group_show_duplicate = has_group;
});
var group_show_create = false;
session?.user_has_group("sh_hide_feature.group_show_create").then(function (has_group) {
    group_show_create = has_group;
});



patch(ListController.prototype, 'sh_hide_feature/static/src/js/sh_hide_button.js', {
    setup() {
        this._super();
        this.group_show_export = group_show_export;
        this.group_show_create = group_show_create;
    },
    getActionMenuItems() {
        const isM2MGrouped = this.model.root.isM2MGrouped;
        const otherActionItems = [];
        if (this.isExportEnable && group_show_export) {
            otherActionItems.push({
                key: "export",
                description: this.env._t("Export"),
                callback: () => this.onExportData(),
            });
        }
        if (this.archiveEnabled && !isM2MGrouped) {
            otherActionItems.push({
                key: "archive",
                description: this.env._t("Archive"),
                callback: () => {
                    const dialogProps = {
                        body: this.env._t(
                            "Are you sure that you want to archive all the selected records?"
                        ),
                        confirm: () => {
                            this.toggleArchiveState(true);
                        },
                        cancel: () => {},
                    };
                    this.dialogService.add(ConfirmationDialog, dialogProps);
                },
            });
            otherActionItems.push({
                key: "unarchive",
                description: this.env._t("Unarchive"),
                callback: () => this.toggleArchiveState(false),
            });
        }
        if (this.activeActions.delete && !isM2MGrouped && group_show_delete) {
            otherActionItems.push({
                key: "delete",
                description: this.env._t("Delete"),
                callback: () => this.onDeleteSelectedRecords(),
            });
        }
        return Object.assign({}, this.props.info.actionMenus, { other: otherActionItems });
    },    
});


patch(FormController.prototype, 'sh_hide_feature/static/src/js/sh_hide_button.js', {
    setup() {
        this._super();
        this.group_show_create = group_show_create;
    },
    getActionMenuItems() {
        const otherActionItems = [];
        if (this.archiveEnabled) {
            if (this.model.root.isActive) {
                otherActionItems.push({
                    key: "archive",
                    description: this.env._t("Archive"),
                    callback: () => {
                        const dialogProps = {
                            body: this.env._t(
                                "Are you sure that you want to archive all this record?"
                            ),
                            confirm: () => this.model.root.archive(),
                            cancel: () => {},
                        };
                        this.dialogService.add(ConfirmationDialog, dialogProps);
                    },
                });
            } else {
                otherActionItems.push({
                    key: "unarchive",
                    description: this.env._t("Unarchive"),
                    callback: () => this.model.root.unarchive(),
                });
            }
        }
        if (this.archInfo.activeActions.create && this.archInfo.activeActions.duplicate && group_show_duplicate) {
            otherActionItems.push({
                key: "duplicate",
                description: this.env._t("Duplicate"),
                callback: () => this.duplicateRecord(),
            });
        }
        if (this.archInfo.activeActions.delete && !this.model.root.isVirtual && group_show_delete) {
            otherActionItems.push({
                key: "delete",
                description: this.env._t("Delete"),
                callback: () => this.deleteRecord(),
                skipSave: true,
            });
        }
        return Object.assign({}, this.props.info.actionMenus, { other: otherActionItems });
    }
    
});


patch(KanbanController.prototype, 'sh_hide_feature/static/src/js/sh_hide_button.js', {
    setup() {
        this._super();
        this.group_show_create = group_show_create;
    },
    
    async createRecord(group) {
        const { activeActions, onCreate } = this.props.archInfo;
        const { root } = this.model;
        if (this.group_show_create) {
            if (activeActions.quickCreate && onCreate === "quick_create" && root.canQuickCreate()) {
                await root.quickCreate(group);
            } else if (onCreate && onCreate !== "quick_create") {
                const options = {
                    additionalContext: root.context,
                    onClose: async () => {
                        await this.model.root.load();
                        this.render(true); // FIXME WOWL reactivity
                    },
                };
                await this.actionService.doAction(onCreate, options);
            } else {
                await this.props.createRecord();
            }
        }        
    }
    
});
