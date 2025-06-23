$(document).ready(function() {

    $(document).on("click",".js_cls_sh_currency_button",function(ev) {
        ev.preventDefault();
        var pricelist_id = $(ev.currentTarget).data('pricelist_id');
        var pricelist_url = $(ev.currentTarget).data('pricelist_url');
        localStorage.setItem('sh_website_sale_popup_current_pl', pricelist_id);


        /* ------------------------------------------------
        we have issue when share product URL with attribute at that time
        that attribute not kept when change pricelist to fix this issue
        we have added redirect url from javascript side.
        for ex, http://localhost:8084/shop/customizable-desk-9#attr=2,3
        # ------------------------------------------------
        */

        window.location = pricelist_url + '?redirect=' + encodeURIComponent(window.location.href)

    });

});