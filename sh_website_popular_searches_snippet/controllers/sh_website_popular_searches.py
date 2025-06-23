# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import http
from odoo.addons.website.controllers.main import Website
from odoo.http import request


class ShWebsitePopularSearches(Website):

    @http.route()
    def autocomplete(self, search_type=None, term=None, order=None, limit=5, max_nb_chars=999, options=None):
        """
        OVERRIDE BY SOFTHEALER TECHNOLOGIES
        The function tracks popular searches on a website and increments the count for each search term.
        """
        response = super().autocomplete(search_type, term,
                                        order, limit, max_nb_chars, options)

        website = request.website
        if website.enable_website_popular_searches:
            search_term = response.get('fuzzy_search') or term
            if response.get('results_count', 0) and search_type and search_term and len(search_term) >= 5:
                domain = [('name', '=', search_term)]
                if website:
                    domain += website.website_domain()

                PopularSearches = request.env['sh.website.popular.searches']
                searches = PopularSearches.search(domain)
                if not searches:
                    PopularSearches.create({'name': search_term,
                                            'search_type': search_type,
                                            'website_id': website.id,
                                            'searches_count': 1})
                else:
                    searches.searches_count += 1

        return response

    @http.route('/sh_website/popular_searches', type='json', auth='public', website=True)
    def popular_searches(self, min_search_count=100):
        """
        METHOD OF SOFTHEALER TECHNOLOGIES

        This function returns a list of popular searches on a website with a minimum search count and
        filters based on user permissions.

        :param min_search_count: This parameter is an optional integer value that sets the minimum
        number of searches required for a search term to be considered "popular". By default, it is set
        to 100, defaults to 100 (optional)
        :return: a list of dictionaries containing the name, searches_count, and is_published fields of
        popular searches on the website that have a searches_count greater than or equal to the
        specified min_search_count and are published. If the user is an admin or website designer, the
        is_published filter is ignored. The list is empty if no popular searches meet the criteria.
        """
        website = request.website
        searches=[]
        if website.enable_website_popular_searches:
            
            domain = [('searches_count', '>=', min_search_count),
                    ('is_published', '=', True)]
            if request.env.user._is_admin() or request.env.user.has_group("website.group_website_designer"):
                domain = [('searches_count', '>=', min_search_count)]

            if website:
                domain += website.website_domain()

            searches = request.env['sh.website.popular.searches'].search_read(
                domain, fields=['name', 'searches_count', 'is_published'])

        return searches
