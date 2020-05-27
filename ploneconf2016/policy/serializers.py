from plone.app.uuid.utils import uuidToObject
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxcontent import SerializeToJson
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.interface import implementer

from .content.presentation import IPresentation


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


# @adapter(ISet, IPresentation, Interface)
# @implementer(IFieldSerializer)
# class PresentationSetFieldSerializer(DefaultFieldSerializer):
#     def __init__(self, field, context, request):
#         self.context = context
#         self.request = request
#         self.field = field
#
#     def __call__(self):
#         result = super(PresentationSetFieldSerializer, self).__call__
#         if IField.providedBy(self.field):  # Binding is necessary for named vocabularies
#             self.field = self.field.bind(self.context)
#
#         value = self.get_value()
#         value_type = self.field.value_type
#         collection_to_serialize = []
#         import ipdb; ipdb.set_trace() # TODO REMOVE BREAKPOINT
#         for item in value:
#             term = value_type.vocabulary.getTerm(item)
#             item_to_serialize = {
#                 u"token": term.token,
#                 u"title": term.title,
#             }
#             obj = uuidToObject(item)
#             if IDexterityContent.providedBy(obj):
#                 # If obj is a Dexterity Content type, we can provide a site_root_relative_url
#                 item_to_serialize["site_root_relative_url"] = getSiteRootRelativePath(
#                     obj, self.request
#                 )
#             collection_to_serialize.append(item_to_serialize)
#
#         return json_compatible(collection_to_serialize)



@adapter(IPresentation, Interface)
@implementer(ISerializeToJson)
class PresentationSerializer(SerializeToJson):

    def __init__(self, context, request):
        super().__init__(context, request)

    def __call__(self, version=None, include_items=True):
        serialized_presentation = super().__call__(version, include_items)
        avdanced_speaker = []
        if self.context.speaker:
            speaker = uuidToObject(next(iter(self.context.speaker)))
            if speaker.headshot and speaker.headshot.filename:
                speaker_headshot_filename = speaker.headshot.filename
            else:
                speaker_headshot_filename = ""
            avdanced_speaker.append(
                {
                    "site_root_relative_url": getSiteRootRelativePath(
                        speaker, self.request
                    ),
                    "title": speaker.Title(),
                    "speaker_url": speaker.absolute_url(),
                    # "headshot_url": "{}/@@images/{}".format(speaker.absolute_url(), speaker_headshot_filename),
                }
            )
            serialized_presentation["speaker"] = json_compatible(avdanced_speaker)

        return serialized_presentation

