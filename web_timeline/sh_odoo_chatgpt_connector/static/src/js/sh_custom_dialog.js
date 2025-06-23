/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
const { useEffect, onWillStart } = owl;
import { Component, onMounted } from "@odoo/owl";
import { View } from "@web/views/view";
import { useChildRef } from "@web/core/utils/hooks";
import { session } from "@web/session";

export class shCustomDialog extends Component {
    setup() {
        super.setup();
        
        this.orm = useService("orm");
        this.modalRef = useChildRef();
        owl.onMounted(this.onMounted);
    }

    async onMounted(){

        const args = {
            domain: [['id', '=', session.uid]],
            fields: ["auto_generate_response"],
            context: [],
        }
        var self = this

        let input_data = self.props.context.input_data || ''
        $(document).find('#sh_loading_bubble').hide()
        self.orm.call("res.users", 'search_read',[],args).then(async function (user) {
            if (user && user[0].auto_generate_response == true) {
                if(input_data.trimStart() && !self.props.context.is_open_from_send_msg){
                    self.props._preview()
                }
            }
        })
        
    }
   
}

shCustomDialog.components = { Dialog, View };

shCustomDialog.props = {

    title: { type: String, optional: true },
    size: Dialog.props.size,
    body: "",
    confirmLabel: "",
    cancelLabel : "",
    previewLabel : "",
    _cancel : Function,
    _preview : Function,
    _confirm : Function,
    close: Function,
    context: { type: Object, optional: true },
        
};

shCustomDialog.template = "sh_odoo_chatgpt_connector.shCustomDialog";

