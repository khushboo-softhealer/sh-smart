/** @odoo-module **/

import { CalendarModel } from "@web/views/calendar/calendar_model";
import { AttendeeCalendarModel } from "@calendar/views/attendee_calendar/attendee_calendar_model";
import { patch } from "@web/core/utils/patch";

patch(AttendeeCalendarModel, "calender_inherit", {
    services: [...AttendeeCalendarModel.services, "rpc"],
});
patch(AttendeeCalendarModel.prototype, "calender_inherit", {
    fetchRecords(data) {     
    
        if (this.meta.context.active_model == "meeting.rooms"){
            var upd_obj = data['filterSections']['partner_ids']['filters'].map(obj => {            
                if (obj['type'] == "all") {
                    obj['active']= true;
                }    
                else if (obj['type'] == "user"){
                    obj['active']= true;
                }  
                else{
                    obj['active']= false;
                }                 
                })
            const { fieldNames, resModel } = this.meta;                               
            return this.orm.searchRead(resModel, this.computeDomain(data), fieldNames);
        }
        else{
            const { fieldNames, resModel } = this.meta;       
            return this.orm.searchRead(resModel, this.computeDomain(data), fieldNames);
        }        
    }
})
