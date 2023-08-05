# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page


class IpAccessControlListMappingList(ListResource):
    """  """

    def __init__(self, version, account_sid, domain_sid):
        """
        Initialize the IpAccessControlListMappingList

        :param Version version: Version that contains the resource
        :param account_sid: The account_sid
        :param domain_sid: A string that uniquely identifies the SIP Domain

        :returns: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingList
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingList
        """
        super(IpAccessControlListMappingList, self).__init__(version)

        # Path Solution
        self._solution = {
            'account_sid': account_sid,
            'domain_sid': domain_sid,
        }
        self._uri = '/Accounts/{account_sid}/SIP/Domains/{domain_sid}/IpAccessControlListMappings.json'.format(**self._solution)

    def create(self, ip_access_control_list_sid):
        """
        Create a new IpAccessControlListMappingInstance

        :param unicode ip_access_control_list_sid: The ip_access_control_list_sid

        :returns: Newly created IpAccessControlListMappingInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingInstance
        """
        data = values.of({
            'IpAccessControlListSid': ip_access_control_list_sid,
        })

        payload = self._version.create(
            'POST',
            self._uri,
            data=data,
        )

        return IpAccessControlListMappingInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            domain_sid=self._solution['domain_sid'],
        )

    def stream(self, limit=None, page_size=None):
        """
        Streams IpAccessControlListMappingInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, limit=None, page_size=None):
        """
        Lists IpAccessControlListMappingInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingInstance]
        """
        return list(self.stream(
            limit=limit,
            page_size=page_size,
        ))

    def page(self, page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of IpAccessControlListMappingInstance records from the API.
        Request is executed immediately

        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of IpAccessControlListMappingInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingPage
        """
        params = values.of({
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )

        return IpAccessControlListMappingPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of IpAccessControlListMappingInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of IpAccessControlListMappingInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingPage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return IpAccessControlListMappingPage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a IpAccessControlListMappingContext

        :param sid: The sid

        :returns: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingContext
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingContext
        """
        return IpAccessControlListMappingContext(
            self._version,
            account_sid=self._solution['account_sid'],
            domain_sid=self._solution['domain_sid'],
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a IpAccessControlListMappingContext

        :param sid: The sid

        :returns: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingContext
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingContext
        """
        return IpAccessControlListMappingContext(
            self._version,
            account_sid=self._solution['account_sid'],
            domain_sid=self._solution['domain_sid'],
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.IpAccessControlListMappingList>'


class IpAccessControlListMappingPage(Page):
    """  """

    def __init__(self, version, response, solution):
        """
        Initialize the IpAccessControlListMappingPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API
        :param account_sid: The account_sid
        :param domain_sid: A string that uniquely identifies the SIP Domain

        :returns: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingPage
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingPage
        """
        super(IpAccessControlListMappingPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of IpAccessControlListMappingInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingInstance
        """
        return IpAccessControlListMappingInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            domain_sid=self._solution['domain_sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Api.V2010.IpAccessControlListMappingPage>'


class IpAccessControlListMappingContext(InstanceContext):
    """  """

    def __init__(self, version, account_sid, domain_sid, sid):
        """
        Initialize the IpAccessControlListMappingContext

        :param Version version: Version that contains the resource
        :param account_sid: The account_sid
        :param domain_sid: The domain_sid
        :param sid: The sid

        :returns: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingContext
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingContext
        """
        super(IpAccessControlListMappingContext, self).__init__(version)

        # Path Solution
        self._solution = {
            'account_sid': account_sid,
            'domain_sid': domain_sid,
            'sid': sid,
        }
        self._uri = '/Accounts/{account_sid}/SIP/Domains/{domain_sid}/IpAccessControlListMappings/{sid}.json'.format(**self._solution)

    def fetch(self):
        """
        Fetch a IpAccessControlListMappingInstance

        :returns: Fetched IpAccessControlListMappingInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingInstance
        """
        params = values.of({})

        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )

        return IpAccessControlListMappingInstance(
            self._version,
            payload,
            account_sid=self._solution['account_sid'],
            domain_sid=self._solution['domain_sid'],
            sid=self._solution['sid'],
        )

    def delete(self):
        """
        Deletes the IpAccessControlListMappingInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._version.delete('delete', self._uri)

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.IpAccessControlListMappingContext {}>'.format(context)


class IpAccessControlListMappingInstance(InstanceResource):
    """  """

    def __init__(self, version, payload, account_sid, domain_sid, sid=None):
        """
        Initialize the IpAccessControlListMappingInstance

        :returns: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingInstance
        """
        super(IpAccessControlListMappingInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload['account_sid'],
            'date_created': deserialize.rfc2822_datetime(payload['date_created']),
            'date_updated': deserialize.rfc2822_datetime(payload['date_updated']),
            'friendly_name': payload['friendly_name'],
            'sid': payload['sid'],
            'uri': payload['uri'],
            'subresource_uris': payload['subresource_uris'],
        }

        # Context
        self._context = None
        self._solution = {
            'account_sid': account_sid,
            'domain_sid': domain_sid,
            'sid': sid or self._properties['sid'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: IpAccessControlListMappingContext for this IpAccessControlListMappingInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingContext
        """
        if self._context is None:
            self._context = IpAccessControlListMappingContext(
                self._version,
                account_sid=self._solution['account_sid'],
                domain_sid=self._solution['domain_sid'],
                sid=self._solution['sid'],
            )
        return self._context

    @property
    def account_sid(self):
        """
        :returns: The account_sid
        :rtype: unicode
        """
        return self._properties['account_sid']

    @property
    def date_created(self):
        """
        :returns: The date_created
        :rtype: datetime
        """
        return self._properties['date_created']

    @property
    def date_updated(self):
        """
        :returns: The date_updated
        :rtype: datetime
        """
        return self._properties['date_updated']

    @property
    def friendly_name(self):
        """
        :returns: The friendly_name
        :rtype: unicode
        """
        return self._properties['friendly_name']

    @property
    def sid(self):
        """
        :returns: The sid
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def uri(self):
        """
        :returns: The uri
        :rtype: unicode
        """
        return self._properties['uri']

    @property
    def subresource_uris(self):
        """
        :returns: The subresource_uris
        :rtype: unicode
        """
        return self._properties['subresource_uris']

    def fetch(self):
        """
        Fetch a IpAccessControlListMappingInstance

        :returns: Fetched IpAccessControlListMappingInstance
        :rtype: twilio.rest.api.v2010.account.sip.domain.ip_access_control_list_mapping.IpAccessControlListMappingInstance
        """
        return self._proxy.fetch()

    def delete(self):
        """
        Deletes the IpAccessControlListMappingInstance

        :returns: True if delete succeeds, False otherwise
        :rtype: bool
        """
        return self._proxy.delete()

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Api.V2010.IpAccessControlListMappingInstance {}>'.format(context)
