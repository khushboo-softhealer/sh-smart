/** @odoo-module */

import { useService } from '@web/core/utils/hooks';


const { Component, onWillStart, useState, onWillUpdateProps } = owl;
import { markup } from "@odoo/owl";

export class HighFiveDescPanel extends Component {
    setup() {
        this.orm = useService('orm');
        this.actionService = useService('action');
        this.dialog = useService('dialog');

        this._insertFromProps(this.props);
        onWillUpdateProps(nextProps => this._insertFromProps(nextProps));

        // onWillUpdateProps(newProps => {
        // //   console.log("---HighFivePanelTest-newProps---->", newProps);
        // //   console.log("---HighFivePanelTest-this---->", this);

        // });

        this.state = useState({
            data: {
                milestones: {
                    data: [],
                },
                profitability_items: {
                    costs: { data: [], total: { billed: 0.0, to_bill: 0.0 } },
                    revenues: { data: [], total: { invoiced: 0.0, to_invoice: 0.0 } },
                },
                user: {},
                currency_id: false,
            }
        });
        // onWillStart(() => this.loadData());
    }

    get projectId() {
        var text=this.props.sh_str
        var modifiedText = text;
        if (text.includes('#')) {
            // Use a regular expression to find and highlight the badge
            modifiedText = modifiedText.replace(/(#\S+)/g, '<span style="color: red;">$1</span>');
          }
        var usrnamewithtag='@'+ this.props.sh_user

        if (text.includes(usrnamewithtag)) {
            // Use a regular expression to find and bold the employee name
            modifiedText = modifiedText.replace(new RegExp(usrnamewithtag, 'g'), '<span style="font-weight: bold;">'+usrnamewithtag+'</span>');
          }
        //to pass html content in field
        modifiedText = markup(modifiedText);
        return modifiedText;
    }

    /**
     * @private
     */
         _insertFromProps(props) {

        }

    // get context() {
    //     return this.props.context;
    // }

    // get domain() {
    //     return this.props.domain;
    // }


    // get sectionNames() {
    //     return {
    //         'milestones': this.env._t('Milestones'),
    //         'profitability': this.env._t('Profitability'),
    //     };
    // }

    // get showProjectProfitability() {
    //     return !!this.state.data.profitability_items
    //         && (
    //             this.state.data.profitability_items.revenues.data.length > 0
    //             || this.state.data.profitability_items.costs.data.length > 0
    //         );
    // }

}

// HighFiveDescPanel.components = { ProjectRightSidePanelSection, ProjectMilestone, ViewButton, ProjectProfitability };

HighFiveDescPanel.template = 'sh_br_highfive_test_template';
// HighFivePanelTest.template = 'sh_br_engaging.sh_br_highfive_test_template';

HighFiveDescPanel.props = {
    sh_str: String,
    sh_user: String,
    // context: Object,
    // domain: Array,
};
