/** @odoo-module */
import { useService } from "@web/core/utils/hooks";
var rpc = require('web.rpc');
const { Component, onWillStart } = owl;

export class MeetingRoomsDashBoard extends Component {
    setup() {               
        this.orm = useService("orm");
        this.action = useService("action"); 
        // onWillStart(async () => {
        //     this.Roomsdata = await this.orm.call(
        //         "sh.room",
        //         "dashboard_date",
        //     );
        //     if (window.sessionStorage.getItem('check')) {
        //         this.Roomsdata['from_date'] = window.sessionStorage.getItem('from_date');
        //         this.Roomsdata['end_date'] = window.sessionStorage.getItem('end_date');
        //         this.Roomsdata['check_avaibilty'] = 'true';                
        //     }           
        // });            
    }         
    // action_to_call_wizard(ev){
    //     $('#exampleModal').modal('show');
    // }
    // sh_save_avaibility(ev){
    //     var from_date = new Date($('#from_date').val());
    //     var end_date = new Date($('#end_date').val());        
    //     ev.preventDefault();                
    //     rpc.query({
    //         model: 'sh.room',
    //         method: 'current_dashboard',
    //         args: [{ 'check_avaibilty': 'True', 'from_date': new Date($('#from_date').val()), 'end_date': new Date($('#end_date').val()) }],

    //     }).then(function (data) {
    //         window.sessionStorage.removeItem('from_date', from_date);
    //         window.sessionStorage.removeItem('end_date', end_date);
    //         window.sessionStorage.removeItem('currunt', 'current');
    //         window.sessionStorage.setItem('from_date', from_date.toLocaleDateString());
    //         window.sessionStorage.setItem('end_date', end_date.toLocaleDateString());
    //         window.sessionStorage.setItem('check', 'check');
    //         if (window.sessionStorage.getItem('check')) {               
    //                 $('.datedashboard').append(
    //                     '<h5>  Check avaibility Date  :  ' + '</h5>' + '<h6>' + window.sessionStorage.getItem('from_date')
    //                     + " " + 'TO' + " " + window.sessionStorage.getItem('end_date') + '</h6>');
    //         }
    //         location.reload();           
    //     });   
    // }
    // sh_button_to_call_method(ev){
    //     ev.preventDefault();
    //     ev.stopPropagation();
    //     var from_date = new Date();
    //     var end_date = new Date();        
    //     rpc.query({
    //         model: 'sh.room',
    //         method: 'current_dashboard',
    //         args: [{ 'check_avaibilty': 'False' }],

    //     }).then(function (data) {
    //         window.sessionStorage.removeItem('from_date', from_date);
    //         window.sessionStorage.removeItem('end_date', end_date);
    //         window.sessionStorage.removeItem('check', 'check');
    //         window.sessionStorage.setItem('from_date', from_date.toLocaleDateString());
    //         window.sessionStorage.setItem('end_date', end_date.toLocaleDateString());
    //         window.sessionStorage.setItem('currunt', 'current');
    //         if (window.sessionStorage.getItem('current')) {
    //             $('.datedashboard').append(
    //                 '<h5>  Current Date  :  ' + '</h5>' + '<h6>' + window.sessionStorage.getItem('from_date')
    //                 + '</h6>');
    //         }
    //         location.reload();
    //     });
    // }
}

MeetingRoomsDashBoard.template = 'Rooms.RoomDashboard'


