# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import io
import zipfile
import os
import shutil
import werkzeug
from odoo import http, _
from odoo.http import request


class Redirects(http.Controller):

    def get_latest_commit(self, connector_obj, module):
        response = connector_obj.get_req(
            module.sh_module_url.replace(f'/{module.name}', ''))
        if response.status_code != 200:
            return False

        for data in response.json():
            if data.get('type') == 'dir':
                if data.get('name') == module.name:
                    module.write({
                        'sha': data.get('sha')
                    })
                    return data.get('sha')

        return False

    def _add_depends_product(self, product_list, depends_failed_list):
        '''Recursively find the depends of the product/module'''
        failed_depends_list = []
        depends_product_list = []
        for product_obj in product_list:
            if not product_obj.depends:
                continue

            error = False
            if not product_obj.product_template_attribute_value_ids:
                error = True

            if len(product_obj.product_template_attribute_value_ids) != 1:
                error = True

            if error:
                for depends_obj in product_obj.depends:
                    if depends_obj.technical_name:
                        failed_depends_list.append(depends_obj.technical_name)
                continue

            version_obj = product_obj.product_template_attribute_value_ids[0]

            for depends_obj in product_obj.depends:
                if not depends_obj.technical_name:
                    failed_depends_list.append(depends_obj.name)
                    continue

                find_depends_product_objs = product_obj.search([
                    ('sh_technical_name', '=', depends_obj.technical_name)
                ])
                if not find_depends_product_objs:
                    failed_depends_list.append(depends_obj.technical_name)
                    continue

                depends_found = False
                for depends_product_obj in find_depends_product_objs:
                    depends_version_obj = depends_product_obj.product_template_attribute_value_ids
                    if not depends_version_obj:
                        continue
                    if len(depends_version_obj) != 1:
                        continue
                    depends_version_obj = depends_version_obj[0]
                    if version_obj.name == depends_version_obj.name:
                        depends_product_list.append(depends_product_obj)
                        depends_found = True
                        break
                if not depends_found:
                    failed_depends_list.append(depends_obj.technical_name)

        if depends_product_list:
            self._add_depends_product(depends_product_list, depends_failed_list)
            product_list += depends_product_list

        if failed_depends_list:
            depends_failed_list += failed_depends_list

    def sh_message(self, message):
        # return f"""
        #     <div style="verticle-align: center; margin: auto; background-color: blue;">
        #         <h1 style="text-align: center;">
        #             {message}
        #         </h1>
        #     </div>
        # """
        return f"""
            <h1 style="text-align: center;">
                {message}
            </h1>
        """

    @http.route("/github/sh_download_module_internal", auth="user")
    def download_module_request(self, **params):
        try:
            return self._process_download_module_request(params)
        except Exception as e:
            return self.sh_message(f"An error occurred: {str(e)}")

    def _process_download_module_request(self, params):
        login_user_obj = request.env.user

        # Ignore Public User
        if login_user_obj._is_public():
            return self.sh_message("401: Apologies, you are not an authorized user to access this record.")

        # Check For Internal User
        if not login_user_obj.has_group('base.group_user'):
            return self.sh_message("401: Apologies, you are not an Internal user to access this record.")

        connector_obj = request.env["sh.github.connector"].search(
            [("state", "=", "success")], limit=1)
        if not connector_obj:
            return self.sh_message('Internal Server Error 500: Not find the Github Connector')

        # When the TL is Approved the module download request
        # --------------------------------------------------

        if params.get('request_token'):
            download_req_obj = request.env["sh.download.module.req"].search([
                ('request_token', '=', params['request_token']),
                # ('create_uid', '=', login_user_obj.id)
            ], limit=1)
            if not download_req_obj:
                return self.sh_message("Internal Server Error 500: Failed To Find The Download Request !")
            if download_req_obj.create_uid.id != login_user_obj.id:
                return self.sh_message("Error 401: You are not the create user for This Download Request  !")
            return self._download_modules_internal(connector_obj, [
                module for module in download_req_obj.module_ids
            ])

        # Process the module request from the wizard.
        # --------------------------------------------------

        if not params.get('wizard_id'):
            return self.sh_message("Something want wrong !")

        module_req_obj = request.env["sh.module.req.wizard"].browse(int(params['wizard_id']))
        if not module_req_obj:
            return self.sh_message("Not Getting The Wizard/Request Object !")

        if module_req_obj.req_ref:
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            redirect_url = f'{base_url}/mail/view?model=sh.download.module.req&res_id={str(module_req_obj.req_ref)}'
            return werkzeug.utils.redirect(redirect_url)

        not_product_task_list = []
        product_object_list = []
        is_manager = login_user_obj.has_group('sh_project_task_base.group_project_officer')
        req_approval_person = 'TL'
        is_appstore_project = False
        company_obj = request.env.company
        is_migration_module_request = False

        if module_req_obj.project_id and company_obj.appstore_project_id:
            if module_req_obj.project_id.id == company_obj.appstore_project_id.id:
                is_appstore_project = True

        if module_req_obj.for_which == 'project':

            # Download request for the Migration Task Module
            # Configuration: Migration Version Refrence, Bool(Is Migration Module Request Ignore)
            # If Appstore Project
            # Login User is set in the task's Developer 1
            if is_appstore_project and company_obj.sh_is_migration_enabled:
                version_ref_obj = company_obj.sh_migration_v17_version_id
                if version_ref_obj:
                    task_obj = module_req_obj.task_id
                    if task_obj:
                        task_dev1_obj = task_obj.sh_project_task_base_dev_id
                        if task_dev1_obj and task_dev1_obj.id == login_user_obj.id:
                            if task_obj.version_ids and len(task_obj.version_ids) == 1:
                                if task_obj.version_ids[0].id == version_ref_obj.id:
                                    is_migration_module_request = True

            if not module_req_obj.product_ids:
                message = "Please select the products !"
                return self.sh_message(message)
            
            # New Code to find modules using product variants m2m
            for product in module_req_obj.product_ids:
                product_task = product.sudo().related_sub_task
                if not product_task.sh_product_id:
                    product_task._add_sh_product_variant()
                if product_task.sh_product_id:
                    product_object_list.append(product_task.sh_product_id)
                else:
                    not_product_task_list.append(product_task.name)

            # Old Code to find modules using tasks m2m
            # if not module_req_obj.product_task_ids:
            #     message = "Please select the product tasks !"
            #     return self.sh_message(message)
            # for product_task in module_req_obj.product_task_ids:
            #     if not product_task.sh_product_id:
            #         product_task._add_sh_product_variant()
            #     if product_task.sh_product_id:
            #         product_object_list.append(product_task.sh_product_id)
            #     else:
            #         not_product_task_list.append(product_task.name)

        elif module_req_obj.for_which == 'ticket':
            ticket_product_ids = module_req_obj.ticket_id.product_ids
            if not ticket_product_ids:
                message = "Ticket doesn't contain the Module/Product !"
                return self.sh_message(message)
            product_object_list = [product for product in ticket_product_ids]

            # find_req_obj = module_req_obj.env['sh.download.module.req'].search([
            #     ('project_id', '=', module_req_obj.project_id.id),
            #     ('task_id', '=', module_req_obj.task_id.id),
            #     ('create_uid', '=', login_user_obj.id)
            # ], limit=1)
            # if find_req_obj:

            #     if find_req_obj.module_ids:
            #         already_req_exists = True
            #         for module_obj in find_req_obj.module_ids:
            #             if module_obj.id not in product_object_list.ids:
            #                 already_req_exists = False
            #                 break
            #         if already_req_exists:
            #             module_req_obj._message_popup("Already a request exist for the provided Ticket !")
            #             return
        message = "No modules to download !"
        if not product_object_list:
            if not_product_task_list:
                message = f"Task not link with product variant:\n{', '.join(not_product_task_list)}"
            return self.sh_message(message)

        # When Project is App Store
        if is_appstore_project:
            req_approval_person = 'App Store Module Request Manager'
            is_manager = request.env.user.has_group('sh_download_module_internal.sh_appstore_module_req_manager')

        msg_list = []
        failed_depends_list = []
        module_base = module_req_obj.env['sh.module']

        # Also add the depends product in the list
        self._add_depends_product(product_object_list, failed_depends_list)
        if failed_depends_list:
            message = f"Failed to find the depends for the the: {', '.join(failed_depends_list)}"
            module_req_obj._message_popup(message)
            msg_list.append(message)

        # ----------------------------------
        username_error_covered = False
        not_module_list = []
        module_list = []
        not_access_list = []

        for product_obj in product_object_list:
            module_objs = module_base.sudo().search([
                ('sh_product_id', '=', product_obj.id)
            ], order='datetime desc')
            if not module_objs:
                not_module_list.append(product_obj.sh_technical_name)
                continue

            module = False
            if len(module_objs) > 1:
                module = module_base.sudo().search([
                    ('sh_product_id', '=', product_obj.id)
                ], order='datetime desc', limit=1)

                for mo_obj in module_objs:
                    if module.id == mo_obj.id:
                        continue
                    mo_obj.sudo().sudo().write({
                        'sh_product_id': False,
                        'message': f"Probably the module move in the repo '{module.repo_id.name}' !",
                        # 'state': 'error'
                        'active': False
                    })
                    connector_obj._generate_activity('product.product', product_obj, f"Search module queue for tech name '{product_obj.sh_technical_name}' and archived, If that module not moved from the repo '{mo_obj.repo_id.name}' to '{module.repo_id.name}' then contact the responsible person for the issue ! else done the activity.")
            else:
                module = module_objs

            if not module:
                not_module_list.append(product_obj.sh_technical_name)
                continue

            # When Testing
            # not_access_list.append(module)
            # continue

            if is_manager or is_migration_module_request:
                # If Login user is TL, then no need to check the repo access
                # or
                # Module request is for a migration module
                module_list.append(module)
            else:
                # If not manager then check for the repo access by the user or not ?
                response_dict = module.repo_id._can_acces_by_login_use(connector_obj)
                if response_dict.get('error'):
                    not_access_list.append(module)
                    # Raise error pop-up
                    if 'username' in response_dict['error'] or 'is not a user' in response_dict['error']:
                        if not username_error_covered:
                            module_req_obj._message_popup(response_dict['error'])
                        username_error_covered = True
                    else:
                        module_req_obj._message_popup(response_dict['error'])
                else:
                    module_list.append(module)

        if not_product_task_list:
            message = f"Following task(s) doesn't contain the product variant: \n{', '.join(not_product_task_list)}"
            module_req_obj._message_popup(message)
            msg_list.append(message)

        if not_module_list:
            message = f"Module(s) which are not synced in Softhealer or Deprecated: \n{', '.join(not_module_list)}"
            module_req_obj._message_popup(message)
            msg_list.append(message)

        if not_access_list or module_list:
            # Create Billing Activity if project
            module_req_obj._generate_activity(connector_obj.billing_activity_user_ids)

        if not_access_list:
            # Create the module download request
            module_req_obj._req(not_access_list)
            # Return the proper appropiat message that:
            message = f"Your module request is create for:</br>{',</br>'.join([module.name for module in not_access_list])},</br>Please contact to your '{req_approval_person}' for approval"
            module_req_obj._message_popup(message)
            msg_list.append(message)

        # Download the modules direct from the Wizard
        if not module_list:
            # if module_req_obj.active_page_url:
            #     return redirect(module_req_obj.active_page_url)
            return self.sh_message(f"{',</br></br>'.join(msg_list)}")

        module_req_obj._log(module_list, is_migration_module_request)
        return self._download_modules_internal(connector_obj, module_list)

   

    def _download_modules_internal(self, connector_obj, module_list):
        '''Make an API call to download the modules'''
        try:
            download_zip_name = 'sh_modules'
            new_zip_content_stream = io.BytesIO()

            for module in module_list:
                sha = module.sha
                if not sha:
                    sha = self.get_latest_commit(connector_obj, module)
                    if not sha:
                        return self.sh_message(f'Failed To Get Latest Commit(Sha) For The Module {module.name}')
                response = connector_obj.get_req(f"{module.sh_module_url.split('contents')[0]}zipball/{sha}", '+json')
                if response.status_code != 200:
                    return self.sh_message(f'Failed To Get The Module {module.name}, Response text: {response.text}')
                is_error = False
                # Conver Binary Data to File
                with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_file:

                    # Extract names
                    zip_entries = zip_file.namelist()
                    old_folder_name = None
                    # Process to set proper Module Name
                    for entry in zip_entries:
                        if entry.endswith('/'):
                            old_folder_name = entry.split('/')[0]
                            break
                    if old_folder_name is not None:
                        with zipfile.ZipFile(new_zip_content_stream, 'a') as new_zip_file:
                            for entry in zip_entries:
                                # Replace the old folder name with the new folder name
                                # in the entry's filename and Update new_zip_file
                                new_entry_filename = entry.replace(old_folder_name, module.name, 1)
                                entry_content = zip_file.read(entry)
                                new_zip_file.writestr(new_entry_filename, entry_content)
                    else:
                        is_error = True
                if is_error:
                    return self.sh_message(f'Something Went Wrong When Generating the Module Zip File ! status_code: {response.status_code}, ')

            # new_zip_content_stream = self._update_module_permission(new_zip_content_stream)
            file_content_bytes = new_zip_content_stream.getvalue()
            return request.make_response(file_content_bytes, headers=[
                ('Content-Disposition', http.content_disposition(f'{download_zip_name}.zip')),
                ('Content-Type', 'application/zip'),
                ('Content-Length', len(file_content_bytes))
            ])
        except Exception as e:
            error = str(e)
            if 'Temporary failure in name resolution' in error:
                error = f"Please check your Internet Connection</br>Error: {error}"
            return self.sh_message(error)

    # def _update_module_permission(self, zip_file):
    #     # Define the extraction directory
    #     extraction_dir = 'sh_download_module_internal'

    #     # Create the extraction directory if it doesn't exist
    #     os.makedirs(extraction_dir, exist_ok=True)

    #     # Step 1: Extract all files from the ZIP archive
    #     with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    #         zip_ref.extractall(extraction_dir)

    #     # Step 2: Walk through the extracted directory and update permissions
    #     for root, dirs, files in os.walk(extraction_dir):
    #         for file in files:
    #             file_path = os.path.join(root, file)
    #             # Set the permissions to Read and write for the owner, none for group and others
    #             os.chmod(file_path, 0o755)

    #     # (Optional) Step 3: Re-compress the files into a new ZIP archive
    #     new_zip_content_stream = io.BytesIO()
    #     with zipfile.ZipFile(new_zip_content_stream, 'w') as new_zip:
    #         for root, dirs, files in os.walk(extraction_dir):
    #             for file in files:
    #                 file_path = os.path.join(root, file)
    #                 # Add the file to the new ZIP archive
    #                 new_zip.write(file_path, arcname=os.path.relpath(file_path, extraction_dir))

    #     # Clean up the extracted files
    #     shutil.rmtree(extraction_dir)
    #     return new_zip_content_stream
