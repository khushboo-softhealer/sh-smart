odoo.define('migration_dashboard.dashboard', function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;
    var rpc = require('web.rpc');
    var session = require('web.session');
    var QWeb = core.qweb;
    var migration_details = [];
    var MigrationDashboardView = AbstractAction.extend({
        events: {},
        init: function (parent, context) {
            this._super(parent, context);
            var self = this;
            if (context.tag == 'migration_dashboard.dashboard') {
                self._rpc({
                    model: 'sh.migrations.dashboard',
                    method: 'get_migration_details',
                    args: ['123']
                }, []).then(function(result){
                    migration_details = result
                    self.render(migration_details);
                })
            }
        },

        render: function (migration_details) {
            var super_render = this._super;
            var self = this;
            const migration_details_array = Object.entries(migration_details).map(([key, value]) => ({ key, value }));
            var migration_dashboiard = QWeb.render('migration_dashboard.dashboard', {
                widget: self,
                migration_details: migration_details_array
            });
            $( ".o_control_panel" ).addClass( "o_hidden" );
            $(migration_dashboiard).prependTo(self.$el);
            return migration_dashboiard
        },
    });
    core.action_registry.add('migration_dashboard.dashboard', MigrationDashboardView);
    return MigrationDashboardView
});