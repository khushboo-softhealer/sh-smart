/** @odoo-module */

import { patch } from 'web.utils';
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";
import ajax from 'web.ajax';
var model_list = []
var has_access = ''

patch(Many2XAutocomplete.prototype, 'web/static/src/views/fields/relational_utils.js', {
    setup() {
        
        ajax.jsonRpc('/sh_get_models_user_access', 'call', {}).then(function (result) {
            if(result.has_access && result.model_list.length > 0){
                model_list = result.model_list
                has_access = result.has_access
            }
        });
        this._super();
    },

    async loadOptionsSource(request) {
        if (model_list.includes(this.props.resModel)){
            this.props.quickCreate = null; 
            this.activeActions.createEdit = false;
            this.activeActions.create = false;
        }
        
        return this._super(request);
    },

});