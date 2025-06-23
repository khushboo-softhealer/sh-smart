/** @odoo-module **/

import { FollowerListMenu } from '@mail/components/follower_list_menu/follower_list_menu';
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
patch(FollowerListMenu.prototype, 'show.followbutton', {
    setup() {
        this._super();
        this.sh_follow_group_allow = session.sh_show_follow_button || false;
    },
});
