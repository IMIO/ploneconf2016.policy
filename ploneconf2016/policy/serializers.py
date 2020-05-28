from plone.app.uuid.utils import uuidToObject
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxcontent import SerializeToJson
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.interface import implementer

from .content.presentation import IPresentation
from .content.person import IPerson


def getSiteRootRelativePath(context, request):
    """ Get site root relative path to an item
    @param context: Content item which path is resolved
    @param request: HTTP request object
    @return: Path to the context object, relative to site root, prefixed with a slash.
    """

    portal_state = getMultiAdapter((context, request), name=u"plone_portal_state")
    site = portal_state.portal()

    # Both of these are tuples
    site_path = site.getPhysicalPath()
    context_path = context.getPhysicalPath()

    relative_path = context_path[len(site_path) :]

    return "/" + "/".join(relative_path)

def twitter_url(person):
    if person.twitter_handle != None:
        return 'https://twitter.com/%s' % person.twitter_handle
    return ''

@adapter(IPresentation, Interface)
@implementer(ISerializeToJson)
class PresentationSerializer(SerializeToJson):

    def __init__(self, context, request):
        super().__init__(context, request)

    def __call__(self, version=None, include_items=True):
        serialized_presentation = super().__call__(version, include_items)
        avdanced_speaker = []
        for speaker in self.context.speaker:
            full_speaker = uuidToObject(speaker)
            avdanced_speaker.append(
                {
                    "site_root_relative_url": getSiteRootRelativePath(
                        full_speaker, self.request
                    ),
                    "title": full_speaker.Title(),
                    "twitter_url": twitter_url(full_speaker),
                    "twitter_handle": full_speaker.twitter_handle,
                    "headshot": SerializeToJson(full_speaker, self.request)()['headshot']
                }
            )
        serialized_presentation["speaker"] = json_compatible(avdanced_speaker)

        return serialized_presentation


@adapter(IPerson, Interface)
@implementer(ISerializeToJson)
class PersonSerializer(SerializeToJson):

    def __init__(self, context, request):
        super().__init__(context, request)

    def __call__(self, version=None, include_items=True):
        serialized_person = super().__call__(version, include_items)
        serialized_person = json_compatible(serialized_person)
        return serialized_person
