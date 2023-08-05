# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from twilio.base import deserialize
from twilio.base import serialize
from twilio.base import values
from twilio.base.instance_context import InstanceContext
from twilio.base.instance_resource import InstanceResource
from twilio.base.list_resource import ListResource
from twilio.base.page import Page


class EventList(ListResource):
    """  """

    def __init__(self, version):
        """
        Initialize the EventList

        :param Version version: Version that contains the resource

        :returns: twilio.rest.monitor.v1.event.EventList
        :rtype: twilio.rest.monitor.v1.event.EventList
        """
        super(EventList, self).__init__(version)

        # Path Solution
        self._solution = {}
        self._uri = '/Events'.format(**self._solution)

    def stream(self, actor_sid=values.unset, event_type=values.unset,
               resource_sid=values.unset, source_ip_address=values.unset,
               start_date=values.unset, end_date=values.unset, limit=None,
               page_size=None):
        """
        Streams EventInstance records from the API as a generator stream.
        This operation lazily loads records as efficiently as possible until the limit
        is reached.
        The results are returned as a generator, so this operation is memory efficient.

        :param unicode actor_sid: The actor_sid
        :param unicode event_type: The event_type
        :param unicode resource_sid: The resource_sid
        :param unicode source_ip_address: The source_ip_address
        :param date start_date: The start_date
        :param date end_date: The end_date
        :param int limit: Upper limit for the number of records to return. stream()
                          guarantees to never return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, stream() will attempt to read the
                              limit with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.monitor.v1.event.EventInstance]
        """
        limits = self._version.read_limits(limit, page_size)

        page = self.page(
            actor_sid=actor_sid,
            event_type=event_type,
            resource_sid=resource_sid,
            source_ip_address=source_ip_address,
            start_date=start_date,
            end_date=end_date,
            page_size=limits['page_size'],
        )

        return self._version.stream(page, limits['limit'], limits['page_limit'])

    def list(self, actor_sid=values.unset, event_type=values.unset,
             resource_sid=values.unset, source_ip_address=values.unset,
             start_date=values.unset, end_date=values.unset, limit=None,
             page_size=None):
        """
        Lists EventInstance records from the API as a list.
        Unlike stream(), this operation is eager and will load `limit` records into
        memory before returning.

        :param unicode actor_sid: The actor_sid
        :param unicode event_type: The event_type
        :param unicode resource_sid: The resource_sid
        :param unicode source_ip_address: The source_ip_address
        :param date start_date: The start_date
        :param date end_date: The end_date
        :param int limit: Upper limit for the number of records to return. list() guarantees
                          never to return more than limit.  Default is no limit
        :param int page_size: Number of records to fetch per request, when not set will use
                              the default value of 50 records.  If no page_size is defined
                              but a limit is defined, list() will attempt to read the limit
                              with the most efficient page size, i.e. min(limit, 1000)

        :returns: Generator that will yield up to limit results
        :rtype: list[twilio.rest.monitor.v1.event.EventInstance]
        """
        return list(self.stream(
            actor_sid=actor_sid,
            event_type=event_type,
            resource_sid=resource_sid,
            source_ip_address=source_ip_address,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            page_size=page_size,
        ))

    def page(self, actor_sid=values.unset, event_type=values.unset,
             resource_sid=values.unset, source_ip_address=values.unset,
             start_date=values.unset, end_date=values.unset,
             page_token=values.unset, page_number=values.unset,
             page_size=values.unset):
        """
        Retrieve a single page of EventInstance records from the API.
        Request is executed immediately

        :param unicode actor_sid: The actor_sid
        :param unicode event_type: The event_type
        :param unicode resource_sid: The resource_sid
        :param unicode source_ip_address: The source_ip_address
        :param date start_date: The start_date
        :param date end_date: The end_date
        :param str page_token: PageToken provided by the API
        :param int page_number: Page Number, this value is simply for client state
        :param int page_size: Number of records to return, defaults to 50

        :returns: Page of EventInstance
        :rtype: twilio.rest.monitor.v1.event.EventPage
        """
        params = values.of({
            'ActorSid': actor_sid,
            'EventType': event_type,
            'ResourceSid': resource_sid,
            'SourceIpAddress': source_ip_address,
            'StartDate': serialize.iso8601_date(start_date),
            'EndDate': serialize.iso8601_date(end_date),
            'PageToken': page_token,
            'Page': page_number,
            'PageSize': page_size,
        })

        response = self._version.page(
            'GET',
            self._uri,
            params=params,
        )

        return EventPage(self._version, response, self._solution)

    def get_page(self, target_url):
        """
        Retrieve a specific page of EventInstance records from the API.
        Request is executed immediately

        :param str target_url: API-generated URL for the requested results page

        :returns: Page of EventInstance
        :rtype: twilio.rest.monitor.v1.event.EventPage
        """
        response = self._version.domain.twilio.request(
            'GET',
            target_url,
        )

        return EventPage(self._version, response, self._solution)

    def get(self, sid):
        """
        Constructs a EventContext

        :param sid: The sid

        :returns: twilio.rest.monitor.v1.event.EventContext
        :rtype: twilio.rest.monitor.v1.event.EventContext
        """
        return EventContext(
            self._version,
            sid=sid,
        )

    def __call__(self, sid):
        """
        Constructs a EventContext

        :param sid: The sid

        :returns: twilio.rest.monitor.v1.event.EventContext
        :rtype: twilio.rest.monitor.v1.event.EventContext
        """
        return EventContext(
            self._version,
            sid=sid,
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Monitor.V1.EventList>'


class EventPage(Page):
    """  """

    def __init__(self, version, response, solution):
        """
        Initialize the EventPage

        :param Version version: Version that contains the resource
        :param Response response: Response from the API

        :returns: twilio.rest.monitor.v1.event.EventPage
        :rtype: twilio.rest.monitor.v1.event.EventPage
        """
        super(EventPage, self).__init__(version, response)

        # Path Solution
        self._solution = solution

    def get_instance(self, payload):
        """
        Build an instance of EventInstance

        :param dict payload: Payload response from the API

        :returns: twilio.rest.monitor.v1.event.EventInstance
        :rtype: twilio.rest.monitor.v1.event.EventInstance
        """
        return EventInstance(
            self._version,
            payload,
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        return '<Twilio.Monitor.V1.EventPage>'


class EventContext(InstanceContext):
    """  """

    def __init__(self, version, sid):
        """
        Initialize the EventContext

        :param Version version: Version that contains the resource
        :param sid: The sid

        :returns: twilio.rest.monitor.v1.event.EventContext
        :rtype: twilio.rest.monitor.v1.event.EventContext
        """
        super(EventContext, self).__init__(version)

        # Path Solution
        self._solution = {
            'sid': sid,
        }
        self._uri = '/Events/{sid}'.format(**self._solution)

    def fetch(self):
        """
        Fetch a EventInstance

        :returns: Fetched EventInstance
        :rtype: twilio.rest.monitor.v1.event.EventInstance
        """
        params = values.of({})

        payload = self._version.fetch(
            'GET',
            self._uri,
            params=params,
        )

        return EventInstance(
            self._version,
            payload,
            sid=self._solution['sid'],
        )

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Monitor.V1.EventContext {}>'.format(context)


class EventInstance(InstanceResource):
    """  """

    def __init__(self, version, payload, sid=None):
        """
        Initialize the EventInstance

        :returns: twilio.rest.monitor.v1.event.EventInstance
        :rtype: twilio.rest.monitor.v1.event.EventInstance
        """
        super(EventInstance, self).__init__(version)

        # Marshaled Properties
        self._properties = {
            'account_sid': payload['account_sid'],
            'actor_sid': payload['actor_sid'],
            'actor_type': payload['actor_type'],
            'description': payload['description'],
            'event_data': payload['event_data'],
            'event_date': deserialize.iso8601_datetime(payload['event_date']),
            'event_type': payload['event_type'],
            'resource_sid': payload['resource_sid'],
            'resource_type': payload['resource_type'],
            'sid': payload['sid'],
            'source': payload['source'],
            'source_ip_address': payload['source_ip_address'],
            'url': payload['url'],
            'links': payload['links'],
        }

        # Context
        self._context = None
        self._solution = {
            'sid': sid or self._properties['sid'],
        }

    @property
    def _proxy(self):
        """
        Generate an instance context for the instance, the context is capable of
        performing various actions.  All instance actions are proxied to the context

        :returns: EventContext for this EventInstance
        :rtype: twilio.rest.monitor.v1.event.EventContext
        """
        if self._context is None:
            self._context = EventContext(
                self._version,
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
    def actor_sid(self):
        """
        :returns: The actor_sid
        :rtype: unicode
        """
        return self._properties['actor_sid']

    @property
    def actor_type(self):
        """
        :returns: The actor_type
        :rtype: unicode
        """
        return self._properties['actor_type']

    @property
    def description(self):
        """
        :returns: The description
        :rtype: unicode
        """
        return self._properties['description']

    @property
    def event_data(self):
        """
        :returns: The event_data
        :rtype: dict
        """
        return self._properties['event_data']

    @property
    def event_date(self):
        """
        :returns: The event_date
        :rtype: datetime
        """
        return self._properties['event_date']

    @property
    def event_type(self):
        """
        :returns: The event_type
        :rtype: unicode
        """
        return self._properties['event_type']

    @property
    def resource_sid(self):
        """
        :returns: The resource_sid
        :rtype: unicode
        """
        return self._properties['resource_sid']

    @property
    def resource_type(self):
        """
        :returns: The resource_type
        :rtype: unicode
        """
        return self._properties['resource_type']

    @property
    def sid(self):
        """
        :returns: The sid
        :rtype: unicode
        """
        return self._properties['sid']

    @property
    def source(self):
        """
        :returns: The source
        :rtype: unicode
        """
        return self._properties['source']

    @property
    def source_ip_address(self):
        """
        :returns: The source_ip_address
        :rtype: unicode
        """
        return self._properties['source_ip_address']

    @property
    def url(self):
        """
        :returns: The url
        :rtype: unicode
        """
        return self._properties['url']

    @property
    def links(self):
        """
        :returns: The links
        :rtype: unicode
        """
        return self._properties['links']

    def fetch(self):
        """
        Fetch a EventInstance

        :returns: Fetched EventInstance
        :rtype: twilio.rest.monitor.v1.event.EventInstance
        """
        return self._proxy.fetch()

    def __repr__(self):
        """
        Provide a friendly representation

        :returns: Machine friendly representation
        :rtype: str
        """
        context = ' '.join('{}={}'.format(k, v) for k, v in self._solution.items())
        return '<Twilio.Monitor.V1.EventInstance {}>'.format(context)
