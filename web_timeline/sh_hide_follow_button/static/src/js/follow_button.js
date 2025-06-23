/** @odoo-module **/

import { FollowButton } from '@mail/components/follow_button/follow_button';
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
patch(FollowButton.prototype, 'show.followbutton', {
    setup() {
        this._super();
        this.sh_follow_group_allow = session.sh_show_follow_button || false;
    },
});
