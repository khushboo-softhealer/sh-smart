# -*- coding: utf-8 -*-

from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome


import logging
import werkzeug
from werkzeug.urls import url_encode

from odoo import http, tools, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.home import ensure_db, Home, SIGN_UP_REQUEST_PARAMS, LOGIN_SUCCESSFUL_PARAMS
from odoo.addons.base_setup.controllers.main import BaseSetup
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)

LOGIN_SUCCESSFUL_PARAMS.add('account_created')

from odoo import http, _
#from odoo.http import request
#from odoo.addons.web.controllers.main import Home
#from odoo import http
import pyotp


# class sh_WebsiteTwitterWall(http.Controller):

#     # Pagination after 15 tweet in storify view
#     _tweet_per_page = 15


#     @http.route(['/sh_twitter_wall/get_tweet'], 
#                 type='json', auth='public', website=True, sitemap=False)
#     def twitter_wall_get_tweet(self, **kwargs):

				



class otp_auth_AuthSignupHome(AuthSignupHome):

    @http.route(['/generate/otp'], type='json', auth="public", methods=['POST'], website=True)
    def generate_otp(self, **kwargs):
        message = ""
        # ============== CODE BY SAGAR 
        token = kwargs.get('g_recaptcha_response')
        print("\n\n\n reCAPTCHA token received: %s", token)
        
        ip_addr = request.httprequest.remote_addr
        print("\n\n\n ip_addr: %s", ip_addr)
        recaptcha_result = request.env['ir.http']._verify_recaptcha_token(ip_addr, token, 'generate_otp')
        print("\n\n\n recaptcha_result: %s", recaptcha_result)

        is_human = False
        if recaptcha_result in ['is_human', 'no_secret']:
            is_human = True
            pass

        if not is_human:
            if recaptcha_result == 'wrong_secret':
                return [0, _("The reCaptcha private key is invalid"), 0]
            
            elif recaptcha_result == 'wrong_token':
                return [0, _("The reCaptcha token is invalid"), 0]
            
            elif recaptcha_result == 'timeout':
                return [0, _("Your request has timed out, please retry"), 0]
            
            elif recaptcha_result == 'bad_request':
                return [0, _("The request is invalid or malformed."), 0]
            
            else:
                return [0, _("Suspicious activity detected by Google reCaptcha."), 0]
        # ============== CODE BY SAGAR 
        email = kwargs.get('email')
        if email:
            if int(kwargs.get('validUser',0))==0:
                message = self.checkExistingUser(**kwargs)
            else:
                message = [1, _("Thanks for the registration."), 0]
            if message[0] != 0:
                otpdata = self.getOTPData()
                otp = otpdata[0]
                otp_time = otpdata[1]
                self.sendOTP(otp, **kwargs)
                message = [1, _("OTP has been sent to given Email Address : {}".format(email)), otp_time]
        else:
            message = [0, _("Please enter an email address"), 0]
        return message

    def checkExistingUser(self, **kwargs):
        email = kwargs.get('email')
        user_obj = request.env["res.users"].sudo().search([("login", "=", email)])
        message = [1, _("Thanks for the registration."), 0]
        if user_obj:
            val = "Another user is already registered with {} email address!!".format(email)
            message = [0, _(val), 0]
        return message

    def sendOTP(self, otp, **kwargs):
        user_name = kwargs.get('userName')
        email = kwargs.get('email')
        request.env['send.otp'].email_send_otp(email, user_name, otp)

        return True


    # softhealer added email parameter in this controller and some logic
    
    @http.route(['/verify/otp'], type='json', auth="public", methods=['POST'], website=True)
    def verify_otp(self, email=False, otp=False):
        if otp:
            totp = int(request.session.get('otpobj'))
            if otp.isdigit():
                # return True if totp==int(otp) else False
                value = False
                if totp==int(otp): 
                    value = True
                
                # SOFTHEALER CUSTOM CODE TO STORE PENDING VERIFICATION EMAILS IN MODE MODEL
                # TO PREVENT IT TO SIGNUP THROUGH API/BOT
                if value:
                    sh_signup_otp_email = request.env['sh.signup.otp.email'].sudo().search([
                        ('email','=', email)
                    ])
                    if not sh_signup_otp_email:
                        request.env['sh.signup.otp.email'].sudo().create({
                            'email':email,
                            'state':'verified',
                        })
                # SOFTHEALER CUSTOM CODE TO STORE PENDING VERIFICATION EMAILS IN MODE MODEL

                return value
            
                # SOFTHEALER CUSTOM CODE TO STORE PENDING VERIFICATION EMAILS IN MODE MODEL
                # TO PREVENT IT TO SIGNUP THROUGH API/BOT
                # if value:
                #     sh_signup_otp_email = request.env['sh.signup.otp.email'].sudo().search([
                #         ('email','=', email)
                #     ])
                #     if sh_signup_otp_email:
                #         sh_signup_otp_email.sudo().unlink()
                

                # SOFTHEALER CUSTOM CODE TO STORE PENDING VERIFICATION EMAILS IN MODE MODEL


            else:
                return False
        else:
            return False
    
    # @http.route(website=True, auth="public", sitemap=False)
    # def web_login(self, redirect=None, *args, **kw):
    #     if 'password' not in kw:
    #         request.session['otploginobj'] = False
    #     response = super(otp_auth_AuthSignupHome, self).web_login(redirect=redirect, *args, **kw)

    #     totp = request.session.get('otploginobj')
    #     password = kw.get('password','***')
    #     if kw.get('radio-otp')=='radiotp' :
    #         request.session['radio-otp']='radiotp'
    #         if totp and totp.isdigit() and password.isdigit():
    #             if int(totp) != int(password):
    #                 response.qcontext['error'] = _("Incorrect OTP")
    #                 request.session['otploginobj'] = False
    #         else:
    #             response.qcontext['error'] = _("Incorrect OTP")
    #             request.session['otploginobj'] = False
    #     else:
    #         request.session['radio-otp']='radiotp'
    #     return response

    # @http.route('/web/reset_password', type='http', auth='public', website=True, sitemap=False)
    # def web_auth_reset_password(self, *args, **kw):
    #     request.session['radio-otp']=None
    #     return super(otp_auth_AuthSignupHome, self).web_auth_reset_password(*args, **kw)

    # @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    # def web_auth_signup(self, *args, **kw):
    #     # request.session['radio-otp']='radiopwd'z
    #     qcontext = self.get_auth_signup_qcontext()
    #     if not qcontext.get('token') and not qcontext.get('signup_enabled'):
    #         raise werkzeug.exceptions.NotFound()
        
    #     try:
    #         # if not request.env['ir.http']._verify_request_recaptcha_token('signup'):
    #         #         raise UserError(_("Suspicious activity detected by Google reCaptcha."))

    #         if not kw.get('login'):
    #             return super(otp_auth_AuthSignupHome, self).web_auth_signup(*args, **kw)
    #         if kw.get('otp'):
    #             totp = int(request.session.get('otpobj'))
    #             if totp == int(kw.get('otp')):
    #                 return super(otp_auth_AuthSignupHome, self).web_auth_signup(*args, **kw)
    #             else:
    #                 qcontext = self.get_auth_signup_qcontext()
    #                 response = request.render('auth_signup.signup', qcontext)
    #                 response.headers['X-Frame-Options'] = 'DENY'
    #                 return response
    #         else:
    #             return super(otp_auth_AuthSignupHome, self).web_auth_signup(*args, **kw)
    #     except UserError as e:
    #         qcontext['error'] = e.args[0]
    #         response = request.render('auth_signup.signup', qcontext)
    #         response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    #         response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
    #         return response
    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        # request.session['radio-otp']='radiopwd'
        if not kw.get('login'):
            return super(otp_auth_AuthSignupHome, self).web_auth_signup(*args, **kw)
        if kw.get('otp'):
            totp = int(request.session.get('otpobj'))
            if totp == int(kw.get('otp')):
                return super(otp_auth_AuthSignupHome, self).web_auth_signup(*args, **kw)
            else:
                qcontext = self.get_auth_signup_qcontext()
                response = request.render('auth_signup.signup', qcontext)
                response.headers['X-Frame-Options'] = 'DENY'
                return response
        else:
            return super(otp_auth_AuthSignupHome, self).web_auth_signup(*args, **kw)


    @http.route(['/check/user'], type='json', auth="public", methods=['POST'], website=True)
    def check_odoo_user(self, **kwargs):
        email = kwargs.get('email')
        mobile = kwargs.get('mobile')
        _logger.info("========kwargs======== : %r", kwargs)
        if email:
            if request.env["res.users"].sudo().search([("login", "=", email)]):
                message = {'status':1, 'message':_("Enter password to login into the user : {}.".format(email))}
            else:
                message = {'status':2, 'message':_("Enter the basic details of the user : {}. for Sign-up".format(email))}
        elif mobile:
            if request.env["res.users"].sudo().search([("mobile", "=", mobile)]):
                message = {'status':1, 'message':_("Enter password to login into the user : {}.".format(mobile))}
            else:
                message = {'status':2, 'message':_("Enter the basic details of the user : {}. for Sign-up".format(mobile))}
        else:
            message = {'status':0, 'message':_("Failed to sign in !! Please enter an email address/mobile no")}
        return message
        
    @http.route(['/send/otp'], type='json', auth="public", methods=['POST'], website=True)
    def send_otp(self, **kwargs):
        email = kwargs.get('email')
        if email:
            msgemail = ''
            if '@' in email:
                msgemail =  email.replace("".join(email.split('@')[:1]), '*****')
            else:
                msgemail = email.replace(email[:3], '****')
            if request.env["res.users"].sudo().search([("login", "=", email)]):
                otpdata = kwargs.get('otpdata') if kwargs.get('otpdata') else self.getOTPData()
                otp = otpdata[0]
                otp_time = otpdata[1]
                request.env['send.otp'].email_send_otp(email, False, otp)
                _logger.info("========optdata======== : %r", otpdata)
                message = {"email":{'status':1, 'message':_("OTP has been sent to given Email Address : {}.".format(msgemail)), 'otp_time':otp_time, 'email':email}}
            else:
                otpdata = self.getOTPData()
                _logger.info("========optdata===otpdata===== : %r", otpdata)
                otp = otpdata[0]
                otp_time = otpdata[1]
                self.sendOTP(otp, **kwargs)
                message = {"email":{'status':2, 'message':_("OTP has been sent to given Email Address : {}.".format(msgemail)), 'otp_time':otp_time, 'email':email}}
        else:
            message = {"email":{'status':0, 'message':_("Failed to send OTP !! Please enter an email address."), 'otp_time':0, 'email':False}}
        return message

    def getOTPData(self):
        otp_time = request.env['ir.default'].sudo().get('website.otp.settings', 'otp_time_limit')
        otp_time = int(otp_time)
        if otp_time < 30:
            otp_time = 30
        #Extra Time added to process OTP
        main_otp_time = otp_time
        totp = pyotp.TOTP(pyotp.random_base32(), interval=main_otp_time)
        otp = totp.now()
        # request.session['otploginobj'] = otp
        request.session['otpobj'] = otp
        return [otp, otp_time]
