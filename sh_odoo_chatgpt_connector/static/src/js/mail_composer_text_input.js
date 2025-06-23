/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { shCustomDialog } from "./sh_custom_dialog";
import { useService } from "@web/core/utils/hooks";
import { ComposerTextInput } from "@mail/components/composer_text_input/composer_text_input";
const { useEffect, onWillStart,useState } = owl;
import { _t, qweb } from 'web.core';


patch(ComposerTextInput.prototype, 'sh_odoo_chatgpt_connector/static/src/js/mail_composer_text_input.js', {

    setup(){
        this._super();
        this.dialogService = useService("dialog");
        this.orm = useService("orm");
        this.user = useService("user");
        onWillStart(async () => {
            this.accesschatgpt = await this.user.hasGroup('sh_odoo_chatgpt_connector.chatgpt_group_user');
        });
    },

    async get_output_data(input_data,default_values,api_key,api_model){

                
        let command_label = $(`label[for="command_${default_values[0]}"]`).text();
        let language_label = $(`label[for="language_${default_values[1]}"]`).text();
        let length_label = $(`label[for="length_${default_values[2]}"]`).text();
        let style_label = $(`label[for="style_${default_values[3]}"]`).text();
        let tra_to_lan_label = $(`label[for="tra_to_lang_${default_values[4]}"]`).text();

        let default_output_data = ''
        
        let commands_to_follow = 'For above message'
        
        if(command_label.trimStart()){
            commands_to_follow += ' ' + command_label
        }

        if(language_label.trimStart()){
            commands_to_follow += ' with ' + language_label + ' type '
        }

        if(length_label.trimStart()){
            commands_to_follow += ' length should be ' + length_label
        }

        if(style_label.trimStart()){
            commands_to_follow += ' style should be ' + style_label
        }

        if(tra_to_lan_label.trimStart()){
            commands_to_follow += ' please Give response in' + tra_to_lan_label + 'language'
        }

        let keywords = $(document).find('.key_words').val()
        if (keywords){

            commands_to_follow += ' add ' + keywords + ' keyword also '

        }

        let input_with_commands = input_data + '\n' + commands_to_follow

        var shHeaders = new Headers();
        
        shHeaders.append("Content-Type", "application/json");
        shHeaders.append("Authorization", "Bearer " + api_key);
        
        var data = JSON.stringify({
            "model": api_model,
            "messages": [{"role": "user", "content": input_with_commands}],
            "temperature": 0.2,
            "top_p": 1,
            "max_tokens": 1000,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        });

        var requestParams = {
            method: 'POST',
            headers: shHeaders,
            body: data,
            redirect: "follow",

        };

        try {
            const response = await fetch("https://api.openai.com/v1/chat/completions", requestParams )
            const isValid = (response.status === 200);
            if(!isValid){
               default_output_data = _t("Check The API Key. The following error was returned by Chatgpt:") + " " + (await response.text())
            }
            else{
                let result = await response.text()
                const obj = JSON.parse(result);
                
                if(obj && obj.choices && obj.choices[0].message && obj.choices[0].message.content){
                    const output = obj.choices[0].message && obj.choices[0].message.content
                    
                    default_output_data = output
                
                }
            }
        } catch (_err) {
            default_output_data = _t("Check your connection and try again"+ _err)
        }

    return default_output_data

},


    async click_on_fa_circle(ev) {
        var self = this
        
        var datas = await self.orm.call("res.company", 'sh_get_data')

        const input_data = $(document).find('.o_ComposerTextInput_textarea').val();
        
        self.dialogService.add(shCustomDialog, {
            body: self.env._t(""),
            confirmLabel: self.env._t("Confirm"),
            cancelLabel : self.env._t("Cancel"),
            previewLabel : self.env._t("Generate Response"),
            title : "Generate Response",
            context: {
                input_data : input_data,
                commands_dict : datas[0],
                languages_dict : datas[1],
                styles_dict : datas[2],
                lengths_dict : datas[3],
                translate_to_languages_dict : datas[4],
                default_values : datas[6],
                
            },
            _confirm() {
                
                let output_data = $(document).find('.output_data').val()
               
                $(document).find('.o_ComposerTextInput_textarea').val(output_data).click()   
                this.props.close()
            },

            async _preview(){
                const input_data = $(document).find('.input_data').val() || ''

                const command = $('.type_of_command').find(":selected").val();
                const language = $('.type_of_language').find(":selected").val();
                const length = $('.length').find(":selected").val();
                const style = $('.style').find(":selected").val();
                const translate_to_language = $('.translate_to_language').find(":selected").val();

                if(input_data){
                    $(document).find('#sh_loading_bubble').show()
                    let output = await self.get_output_data(input_data,[command,language,length,style,translate_to_language],datas[5],datas[7])
                    $(document).find('.output_data').val(output)
                    $(document).find('#sh_loading_bubble').hide()
                 }

            },

            _cancel() {
                this.props.close();
            }
        });
    
    }


})