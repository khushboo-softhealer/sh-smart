/** @odoo-module **/

import emojis from '@mail/js/emojis';

const { Component, useRef, onMounted } = owl;

export class BrEmojisDropdown extends Component {
    setup() {
        this.toggleRef = useRef('toggleRef');
        this.emojis = emojis;
        super.setup();
        onMounted(() => {
            new Dropdown(this.toggleRef.el, {
                  popperConfig: { placement: 'bottom-end', strategy: 'fixed' },
            });
        });
    }

    onEmojiClick(ev) {
        const unicode = ev.currentTarget.textContent.trim();
        const textInput = $('.sh_hive_five_input');
        var old_value = $('.sh_hive_five_input').val();
        textInput.val(old_value + unicode + ' ')
        textInput.focus();
 }
};
BrEmojisDropdown.template = 'bremojisDropdown';



export class BrChildEmojisDropdown extends Component {
    setup() {
        this.toggleRef = useRef('toggleRef');
        this.emojis = emojis;
        super.setup();

        onMounted(() => {
            new Dropdown(this.toggleRef.el, {
                  popperConfig: { placement: 'bottom-end', strategy: 'fixed' },
            });
        });
    }

    onEmojiClick(ev) {
        const unicode = ev.currentTarget.textContent.trim();
        var high_five_child_input_id= this.props.kishan
        var reply_input_id = '#reply_input_id_' + high_five_child_input_id;
        const childtextInput = $(reply_input_id);
        var old_value = $(reply_input_id).val();
        childtextInput.val(old_value + unicode + ' ')
        childtextInput.focus();

 }
};
BrChildEmojisDropdown.template = 'BrchildEmojisDropdown';