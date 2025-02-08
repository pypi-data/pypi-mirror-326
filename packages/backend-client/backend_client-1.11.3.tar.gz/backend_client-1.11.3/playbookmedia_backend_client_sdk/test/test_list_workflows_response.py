# coding: utf-8

"""
    Lead Scraping Service API

    Vector Lead Scraping Service API - Manages Lead Scraping Jobs

    The version of the OpenAPI document: 1.0
    Contact: yoanyomba@vector.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from playbookmedia_backend_client_sdk.models.list_workflows_response import ListWorkflowsResponse

class TestListWorkflowsResponse(unittest.TestCase):
    """ListWorkflowsResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ListWorkflowsResponse:
        """Test ListWorkflowsResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ListWorkflowsResponse`
        """
        model = ListWorkflowsResponse()
        if include_optional:
            return ListWorkflowsResponse(
                workflows = [
                    playbookmedia_backend_client_sdk.models.scraping_workflow_defines_recurring_scraping_configurations.ScrapingWorkflow defines recurring scraping configurations(
                        id = '', 
                        cron_expression = '', 
                        next_run_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        last_run_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        status = 'BACKGROUND_JOB_STATUS_UNSPECIFIED', 
                        retry_count = 56, 
                        max_retries = 56, 
                        alert_emails = '', 
                        org_id = '', 
                        tenant_id = '', 
                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        jobs = [
                            playbookmedia_backend_client_sdk.models.scraping_job.ScrapingJob(
                                id = '', 
                                name = '', 
                                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                keywords = [
                                    ''
                                    ], 
                                lang = '', 
                                zoom = 56, 
                                lat = '', 
                                lon = '', 
                                fast_mode = True, 
                                radius = 56, 
                                depth = 56, 
                                email = True, 
                                max_time = 56, 
                                proxies = [
                                    ''
                                    ], 
                                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                payload_type = '', 
                                priority = 56, 
                                payload = 'YQ==', 
                                leads = [
                                    playbookmedia_backend_client_sdk.models.lead_represents_a_scraped_business_entity.Lead represents a scraped business entity(
                                        id = '', 
                                        name = '', 
                                        website = '', 
                                        phone = '', 
                                        address = '', 
                                        city = '', 
                                        state = '', 
                                        country = '', 
                                        latitude = 1.337, 
                                        longitude = 1.337, 
                                        google_rating = 1.337, 
                                        review_count = 56, 
                                        industry = '', 
                                        employee_count = 56, 
                                        estimated_revenue = '', 
                                        org_id = '', 
                                        tenant_id = '', 
                                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        job = playbookmedia_backend_client_sdk.models.scraping_job.ScrapingJob(
                                            id = '', 
                                            name = '', 
                                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                            keywords = [
                                                ''
                                                ], 
                                            lang = '', 
                                            zoom = 56, 
                                            lat = '', 
                                            lon = '', 
                                            fast_mode = True, 
                                            radius = 56, 
                                            depth = 56, 
                                            email = True, 
                                            max_time = 56, 
                                            proxies = [
                                                ''
                                                ], 
                                            updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                            payload_type = '', 
                                            priority = 56, 
                                            payload = 'YQ==', 
                                            leads = [
                                                playbookmedia_backend_client_sdk.models.lead_represents_a_scraped_business_entity.Lead represents a scraped business entity(
                                                    id = '', 
                                                    name = '', 
                                                    website = '', 
                                                    phone = '', 
                                                    address = '', 
                                                    city = '', 
                                                    state = '', 
                                                    country = '', 
                                                    latitude = 1.337, 
                                                    longitude = 1.337, 
                                                    google_rating = 1.337, 
                                                    review_count = 56, 
                                                    industry = '', 
                                                    employee_count = 56, 
                                                    estimated_revenue = '', 
                                                    org_id = '', 
                                                    tenant_id = '', 
                                                    created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                    updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                    deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                    workspace = playbookmedia_backend_client_sdk.models.workspace_represents_a_business_entity_with_multiple_accounts.Workspace represents a business entity with multiple accounts(
                                                        id = '', 
                                                        name = '', 
                                                        industry = '', 
                                                        domain = '', 
                                                        gdpr_compliant = True, 
                                                        hipaa_compliant = True, 
                                                        soc2_compliant = True, 
                                                        storage_quota = '', 
                                                        used_storage = '', 
                                                        created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                        updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                        deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                        workflows = [
                                                            playbookmedia_backend_client_sdk.models.scraping_workflow_defines_recurring_scraping_configurations.ScrapingWorkflow defines recurring scraping configurations(
                                                                id = '', 
                                                                cron_expression = '', 
                                                                next_run_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                                last_run_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                                retry_count = 56, 
                                                                max_retries = 56, 
                                                                alert_emails = '', 
                                                                org_id = '', 
                                                                tenant_id = '', 
                                                                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                                updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                                deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                                jobs = [
                                                                    
                                                                    ], 
                                                                geo_fencing_radius = 1.337, 
                                                                geo_fencing_lat = 1.337, 
                                                                geo_fencing_lon = 1.337, 
                                                                geo_fencing_zoom_min = 56, 
                                                                geo_fencing_zoom_max = 56, 
                                                                include_reviews = True, 
                                                                include_photos = True, 
                                                                include_business_hours = True, 
                                                                max_reviews_per_business = 56, 
                                                                output_format = 'OUTPUT_FORMAT_UNSPECIFIED', 
                                                                output_destination = '', 
                                                                data_retention = '', 
                                                                anonymize_pii = True, 
                                                                notification_webhook_url = '', 
                                                                notification_slack_channel = '', 
                                                                notification_email_group = '', 
                                                                notification_notify_on_start = True, 
                                                                notification_notify_on_complete = True, 
                                                                notification_notify_on_failure = True, 
                                                                content_filter_allowed_countries = [
                                                                    ''
                                                                    ], 
                                                                content_filter_excluded_types = [
                                                                    ''
                                                                    ], 
                                                                content_filter_minimum_rating = 1.337, 
                                                                content_filter_minimum_reviews = 56, 
                                                                qos_max_concurrent_requests = 56, 
                                                                qos_max_retries = 56, 
                                                                qos_request_timeout = '', 
                                                                qos_enable_javascript = True, 
                                                                respect_robots_txt = True, 
                                                                accept_terms_of_service = True, 
                                                                user_agent = '', )
                                                            ], 
                                                        jobs_run_this_month = 56, 
                                                        workspace_job_limit = 56, 
                                                        daily_job_quota = 56, 
                                                        active_scrapers = 56, 
                                                        total_leads_collected = 56, 
                                                        last_job_run = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                                                    place_id = '', 
                                                    google_maps_url = '', 
                                                    business_status = '', 
                                                    regular_hours = [
                                                        playbookmedia_backend_client_sdk.models.temporal_data.Temporal data(
                                                            id = '', 
                                                            day = 'DAY_OF_WEEK_UNSPECIFIED', 
                                                            open_time = '', 
                                                            close_time = '', 
                                                            closed = True, 
                                                            lead_id = '', )
                                                        ], 
                                                    special_hours = [
                                                        playbookmedia_backend_client_sdk.models.temporal_data.Temporal data(
                                                            id = '', 
                                                            open_time = '', 
                                                            close_time = '', 
                                                            closed = True, 
                                                            lead_id = '', )
                                                        ], 
                                                    photo_references = [
                                                        ''
                                                        ], 
                                                    main_photo_url = '', 
                                                    reviews = [
                                                        playbookmedia_backend_client_sdk.models.detailed_reviews.Detailed reviews(
                                                            id = '', 
                                                            author = '', 
                                                            rating = 1.337, 
                                                            text = '', 
                                                            time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                            language = '', 
                                                            profile_photo_url = '', 
                                                            review_count = 56, )
                                                        ], 
                                                    types = [
                                                        ''
                                                        ], 
                                                    amenities = [
                                                        ''
                                                        ], 
                                                    serves_vegetarian_food = True, 
                                                    outdoor_seating = True, 
                                                    payment_methods = [
                                                        ''
                                                        ], 
                                                    wheelchair_accessible = True, 
                                                    parking_available = True, 
                                                    social_media = {
                                                        'key' : ''
                                                        }, 
                                                    rating_category = '', 
                                                    rating = 1.337, 
                                                    count = 56, 
                                                    last_updated = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                    data_source_version = '', 
                                                    scraping_session_id = '', 
                                                    alternate_phones = [
                                                        ''
                                                        ], 
                                                    contact_person_name = '', 
                                                    contact_person_title = '', 
                                                    contact_email = '', 
                                                    founded_year = 56, 
                                                    business_type = '', 
                                                    certifications = [
                                                        ''
                                                        ], 
                                                    license_number = '', 
                                                    revenue_range = 'REVENUE_RANGE_UNSPECIFIED', 
                                                    funding_stage = '', 
                                                    is_public_company = True, 
                                                    website_load_speed = 1.337, 
                                                    has_ssl_certificate = True, 
                                                    cms_used = '', 
                                                    ecommerce_platforms = [
                                                        ''
                                                        ], 
                                                    timezone = '', 
                                                    neighborhood = '', 
                                                    nearby_landmarks = [
                                                        ''
                                                        ], 
                                                    transportation_access = '', 
                                                    employee_benefits = [
                                                        'EMPLOYEE_BENEFIT_UNSPECIFIED'
                                                        ], 
                                                    parent_company = '', 
                                                    subsidiaries = [
                                                        ''
                                                        ], 
                                                    is_franchise = True, 
                                                    seo_keywords = [
                                                        ''
                                                        ], 
                                                    uses_google_ads = True, 
                                                    google_my_business_category = '', 
                                                    naics_code = '', 
                                                    sic_code = '', 
                                                    unspsc_code = '', 
                                                    is_green_certified = True, 
                                                    energy_sources = [
                                                        ''
                                                        ], 
                                                    sustainability_rating = '', 
                                                    recent_announcements = [
                                                        ''
                                                        ], 
                                                    last_product_launch = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                    has_litigation_history = True, 
                                                    export_control_status = '', )
                                                ], 
                                            workflow_id = '', ), 
                                        workspace = playbookmedia_backend_client_sdk.models.workspace_represents_a_business_entity_with_multiple_accounts.Workspace represents a business entity with multiple accounts(
                                            id = '', 
                                            name = '', 
                                            industry = '', 
                                            domain = '', 
                                            gdpr_compliant = True, 
                                            hipaa_compliant = True, 
                                            soc2_compliant = True, 
                                            storage_quota = '', 
                                            used_storage = '', 
                                            created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                            updated_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                            deleted_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                            workflows = [
                                                
                                                ], 
                                            jobs_run_this_month = 56, 
                                            workspace_job_limit = 56, 
                                            daily_job_quota = 56, 
                                            active_scrapers = 56, 
                                            total_leads_collected = 56, 
                                            last_job_run = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), ), 
                                        place_id = '', 
                                        google_maps_url = '', 
                                        business_status = '', 
                                        regular_hours = [
                                            
                                            ], 
                                        special_hours = [
                                            
                                            ], 
                                        photo_references = [
                                            ''
                                            ], 
                                        main_photo_url = '', 
                                        reviews = [
                                            playbookmedia_backend_client_sdk.models.detailed_reviews.Detailed reviews(
                                                id = '', 
                                                author = '', 
                                                rating = 1.337, 
                                                text = '', 
                                                time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                                language = '', 
                                                profile_photo_url = '', 
                                                review_count = 56, )
                                            ], 
                                        types = [
                                            ''
                                            ], 
                                        amenities = [
                                            ''
                                            ], 
                                        serves_vegetarian_food = True, 
                                        outdoor_seating = True, 
                                        payment_methods = [
                                            ''
                                            ], 
                                        wheelchair_accessible = True, 
                                        parking_available = True, 
                                        social_media = {
                                            'key' : ''
                                            }, 
                                        rating_category = '', 
                                        rating = 1.337, 
                                        count = 56, 
                                        last_updated = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        data_source_version = '', 
                                        scraping_session_id = '', 
                                        alternate_phones = [
                                            ''
                                            ], 
                                        contact_person_name = '', 
                                        contact_person_title = '', 
                                        contact_email = '', 
                                        founded_year = 56, 
                                        business_type = '', 
                                        certifications = [
                                            ''
                                            ], 
                                        license_number = '', 
                                        revenue_range = 'REVENUE_RANGE_UNSPECIFIED', 
                                        funding_stage = '', 
                                        is_public_company = True, 
                                        website_load_speed = 1.337, 
                                        has_ssl_certificate = True, 
                                        cms_used = '', 
                                        ecommerce_platforms = [
                                            ''
                                            ], 
                                        timezone = '', 
                                        neighborhood = '', 
                                        nearby_landmarks = [
                                            ''
                                            ], 
                                        transportation_access = '', 
                                        employee_benefits = [
                                            'EMPLOYEE_BENEFIT_UNSPECIFIED'
                                            ], 
                                        parent_company = '', 
                                        subsidiaries = [
                                            ''
                                            ], 
                                        is_franchise = True, 
                                        seo_keywords = [
                                            ''
                                            ], 
                                        uses_google_ads = True, 
                                        google_my_business_category = '', 
                                        naics_code = '', 
                                        sic_code = '', 
                                        unspsc_code = '', 
                                        is_green_certified = True, 
                                        energy_sources = [
                                            ''
                                            ], 
                                        sustainability_rating = '', 
                                        recent_announcements = [
                                            ''
                                            ], 
                                        last_product_launch = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                                        has_litigation_history = True, 
                                        export_control_status = '', )
                                    ], 
                                workflow_id = '', )
                            ], 
                        workspace = , 
                        geo_fencing_radius = 1.337, 
                        geo_fencing_lat = 1.337, 
                        geo_fencing_lon = 1.337, 
                        geo_fencing_zoom_min = 56, 
                        geo_fencing_zoom_max = 56, 
                        include_reviews = True, 
                        include_photos = True, 
                        include_business_hours = True, 
                        max_reviews_per_business = 56, 
                        output_format = 'OUTPUT_FORMAT_UNSPECIFIED', 
                        output_destination = '', 
                        data_retention = '', 
                        anonymize_pii = True, 
                        notification_webhook_url = '', 
                        notification_slack_channel = '', 
                        notification_email_group = '', 
                        notification_notify_on_start = True, 
                        notification_notify_on_complete = True, 
                        notification_notify_on_failure = True, 
                        content_filter_allowed_countries = [
                            ''
                            ], 
                        content_filter_excluded_types = [
                            ''
                            ], 
                        content_filter_minimum_rating = 1.337, 
                        content_filter_minimum_reviews = 56, 
                        qos_max_concurrent_requests = 56, 
                        qos_max_retries = 56, 
                        qos_request_timeout = '', 
                        qos_enable_javascript = True, 
                        respect_robots_txt = True, 
                        accept_terms_of_service = True, 
                        user_agent = '', )
                    ],
                next_page_token = ''
            )
        else:
            return ListWorkflowsResponse(
        )
        """

    def testListWorkflowsResponse(self):
        """Test ListWorkflowsResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
