/** @odoo-module **/

import { View } from "@web/views/view";
import { patch } from "@web/core/utils/patch";
const { onWillStart } = owl;

patch(View.prototype, '/sh_knowledge_base_customised/static/src/js/sh_sop_custom_class.js', {
    setup() {
        this._super()
        onWillStart(async () => {
        if (this.props.resModel == "sh.sop.article" || this.props.resModel == "sh.knowledge.article") {
            this.props.className = this.props.className + ' sh_sop_article_custom_class';
        }
        })
      },
});