odoo.define('theme_softhealer_website.s_dynamic_snippet', function (require) {

const DynamicSnippet = require('website.s_dynamic_snippet');

DynamicSnippet.include({
    _fetchData: async function() {
        const res = await this._super.apply(this, arguments);
        if(this.$el.hasClass('s_blog_post_sh_image_gird')){
            this.template_key = 'theme_softhealer_website.sh_s_dynamic_snippet';
            const result = [];
            for (let i = 0; i < this.data.length; i += 8) {
                const chunk = this.data.slice(i, i + 8);
                result.push(chunk);
            }
            this.data = result;
        }
        return res;
    }
});
return DynamicSnippet;

});
