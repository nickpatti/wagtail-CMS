import requests
from django.conf import settings

from CMS.test.mocks import SearchMocks


def query_course_and_institution(course, institution, limit, offset):
    if settings.LOCAL:
        return SearchMocks.get_successful_search_response()
    else:
        headers = {
            'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
        }
        base_url = "%s?limit=%s&offset=%s&qc=%s&institutions=%s"
        return requests.get(url=base_url % (settings.SEARCHAPIHOST, limit, offset, course, institution),
                            headers=headers)


def course_finder_query(subject, institution, countries, postcode, filters, limit, offset):
    if settings.LOCAL:
        return SearchMocks.get_successful_search_response()
    else:
        return SearchMocks.get_successful_search_response()
        headers = {
            'Ocp-Apim-Subscription-Key': settings.DATASETAPIKEY
        }
        url = "%s?limit=%s&offset=%s" % (settings.SEARCHAPIHOST, limit, offset)
        if subject and subject != '':
            url = f"{url}&qc={subject}"
        if institution and institution != '':
            url = f"{url}&institutions={institution}"
        if countries and countries != '':
            url = f"{url}&countries={countries.lower().replace(' ', '_')}"
        if postcode and postcode != '':
            url = f"{url}&postcode={postcode}"
        if filters and filters != '':
            url = f"{url}&filters={filters}"
        return requests.get(url=url, headers=headers)
