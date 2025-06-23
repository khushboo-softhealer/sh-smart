/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { registerPatch } from "@mail/model/model_core";
const { useEffect, onWillStart,useState } = owl;
import { useService } from "@web/core/utils/hooks";

import { session } from "@web/session";

import { Chatter } from "@mail/components/chatter/chatter";

patch(Chatter.prototype, 'sh_odoo_chatgpt_connector/static/src/js/field.js', {

    setup(){
        this._super();
        this.state = useState({ show_summary_btn: false });
        this.orm = useService("orm");
        owl.onMounted(this.onMounted);
        this.user = useService("user");
        onWillStart(async () => {
            this.accesschatgpt = await this.user.hasGroup('sh_odoo_chatgpt_connector.chatgpt_group_user');
        });
    },

    async onMounted(){
        const args = {
            domain: [['id', '=', session.uid]],
            fields: ["show_summary_button"],
            context: [],
        }
        var self = this
        self.orm.call("res.users", 'search_read',[],args).then(async function (user) {
            if (user && user[0].show_summary_button == true) {
                self.state.show_summary_btn = true
            }
        })
       
    },


    async click_summary(ev) {
        
        var self = this
        
        const summary_msg = await this.env.services.orm.call('res.company', 'summarize_response', [self.props.record.threadModel,self.props.record.threadId], {});

        this.env.services['action'].doAction({
            type: 'ir.actions.act_window',
            name: this.env._t('Response'),
            target: 'new',
            res_model: 'sh.response.wizard',
            views: [[false, 'form']],
            context : {
                'default_response_message' : summary_msg
            }
        });
    }
});
