16.0.1(Date : 8 June 2023 )
---------------------------------
- Initial release
- Features: In website sale show popup of Pricelist when user visit page.

v16.0.2 (Date : 4th July 2023)
==============================
 = while user login in/out store pricelist in browser local so again n again 
   pricelist popup will not shown


v16.0.3 (Date : 25 Dec 2023)
==============================
  # ------------------------------------------------
  # SOFTHEALER CUSTOM CODE HERE IN ORDER TO REDIRECT PROPER PLACE
  # WHEN PRICELIST CHANGE.
  # for help check standard odoo route:
  # @http.route(['/shop/change_pricelist/<model("product.pricelist"):pricelist>'], type='http', auth="public", website=True, sitemap=False)
  # def pricelist_change(self, pricelist, **post):
  # we have issue when share product URL with attribute at that time
  # that attribute not kept when change pricelist to fix this issue
  # we have added redirect url from javascript side.
  # for ex, http://localhost:8084/shop/customizable-desk-9#attr=2,3
  # ------------------------------------------------

  