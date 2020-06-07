from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxcontent import SerializeToJson
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.interface import implementer
from plone.app.uuid.utils import uuidToObject

from .content.training_class import ITrainingClass


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


@adapter(ITrainingClass, Interface)
@implementer(ISerializeToJson)
class TrainingClassSerializer(SerializeToJson):
    def __init__(self, context, request):
        super().__init__(context, request)

    def __call__(self, version=None, include_items=True):
        serialized_training = super().__call__(version, include_items)

        instructors = []
        for item in self.context.instructor:
            instructor = uuidToObject(item)
            if instructor is not None:
                instructors.append(
                    {
                        "site_root_relative_url": getSiteRootRelativePath(
                            instructor, self.request
                        ),
                        "title": instructor.Title(),
                    }
            )
        serialized_training["instructor"] = json_compatible(instructors)

        return serialized_training
