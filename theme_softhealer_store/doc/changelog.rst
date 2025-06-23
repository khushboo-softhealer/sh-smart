16.0.1 (Date : 30 july 2023)
----------------------------
Initial Release

(9 august 2023)
-------------------
- change store home page banner (independence day banner)

v16.0.6 (Date : 29th Aug 2023)
==============================
 = [ADD] restrict add to cart from shop listing,
 detail page and wishlist page,
 if product variant does not have blog post assign.
(18 august 2023)
-----------------
- remove independence day banner and add other offer banner for store

(29 august 2023)
--------------------
- [UPDATE] store home page banner (rakshabandhan offer)


v16.0.8 (Date : 31 Aug 2023)
============================

- [ADD]
    - Shop cart removing dependency product warning
    - Log note removed dependency product

(Date: 4 SEP 2023)
============================
- [UPDATE] offer banner for store (Janmashtami offer)


(Date: 11 SEP 2023)
=========================
- [REMOVE] property management(coming soon) section from store home page

(Date: 14 SEP 2023)
====================
- [UPDATE] store home page banner (Ganesh Chaturthi Banner)

(Date: 23 SEP 2023)
====================
- [UPDATE] store home page banner

(Date: 23 SEP 2023)
====================
- [UPDATE] chatGPT ChatGPT Integration With Odoo section.

(Date: 28 OCT 2023)
===================
- [UPDATE] store home page banner (Diwali Offer)

(Date: 20 NOV 2023)
======================
- [REMOVE] Diwali Offer Banner

(Date: 22 NOV 2023)
======================
- [UPDATE] Black Friday Offer Banner

(Date: 25 NOV 2023)
=======================
- [UPDATE] Cyber Monday Offer Banner

(Date: 27 NOV 2023)
=======================
- [UPDATE] Offer Banner for store

(Date: 11 DEC 2023)
====================
- [UPDATE] Offer Banner for store (christmas)

(Date: 25 DEC 2023)
====================
- [UPDATE] Offer Banner for store (christmas)

(Date: 1 January 2023)
====================
- [UPDATE] Offer Banner for store (New Year)

(Date: 9 January 2024)
====================
- [UPDATE] Offer Banner

(Date: 24 January 2024)
====================
- [UPDATE] Offer Banner for Republic Day

(Date: 1 February 2024)
====================
- [UPDATE] Offer Banner for store


(Date: 14 Oct 2024) ==> 16.0.9
====================
- [fix] below error when press add to cart button in store in product detail page


RPC_ERROR
Odoo Server Error
Traceback (most recent call last):
  File "/odoo/odoo-server/odoo/http.py", line 1651, in _serve_db
    return service_model.retrying(self._serve_ir_http, self.env)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/odoo/odoo-server/odoo/service/model.py", line 133, in retrying
    result = func()
             ^^^^^^
  File "/odoo/odoo-server/odoo/http.py", line 1678, in _serve_ir_http
    response = self.dispatcher.dispatch(rule.endpoint, args)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/odoo/odoo-server/odoo/http.py", line 1882, in dispatch
    result = self.request.registry['ir.http']._dispatch(endpoint)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/odoo/odoo-server/addons/website/models/ir_http.py", line 237, in _dispatch
    response = super()._dispatch(endpoint)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/odoo/odoo-server/odoo/addons/base/models/ir_http.py", line 154, in _dispatch
    result = endpoint(**request.params)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/odoo/odoo-server/odoo/http.py", line 734, in route_wrapper
    result = endpoint(self, args, *params_ok)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/odoo/odoo-server/addons/website_sale_loyalty/controllers/main.py", line 132, in cart_update_json
    return super().cart_update_json(*args, set_qty=set_qty, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/odoo/odoo-server/odoo/http.py", line 734, in route_wrapper
    result = endpoint(self, args, *params_ok)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/odoo/odoo-server/addons/website_sale/controllers/main.py", line 839, in cart_update_json
    values = order._cart_update(
             ^^^^^^^^^^^^^^^^^^^
  File "/odoo/custom/shsmart/theme_softhealer_store/model/sale.py", line 32, in _cart_update
    res = super(SaleOrder, self)._cart_update(
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/odoo/odoo-server/addons/website_sale_loyalty/models/sale_order.py", line 160, in _cart_update
    product_id, set_qty = kwargs['product_id'], kwargs.get('set_qty')
                          ~~~~~~^^^^^^^^^^^^^^
KeyError: 'product_id'
