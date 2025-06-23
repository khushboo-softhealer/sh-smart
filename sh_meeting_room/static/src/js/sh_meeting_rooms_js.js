/** @odoo-module **/

import { registry } from "@web/core/registry";
import { kanbanView } from '@web/views/kanban/kanban_view';
import { KanbanRenderer } from '@web/views/kanban/kanban_renderer';


export class MeetingRoomsDashBoardKanbanRenderer extends KanbanRenderer {};

MeetingRoomsDashBoardKanbanRenderer.template = 'Rooms.KanbanView';
MeetingRoomsDashBoardKanbanRenderer.components= Object.assign({}, KanbanRenderer.components, {MeetingRoomsDashBoard})

export const MeetingRoomsDashBoardKanbanView = {
    ...kanbanView,
    Renderer: MeetingRoomsDashBoardKanbanRenderer,
};

registry.category("views").add("room_kanban", MeetingRoomsDashBoardKanbanView);
