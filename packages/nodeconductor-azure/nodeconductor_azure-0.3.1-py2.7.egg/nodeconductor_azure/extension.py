from nodeconductor.core import NodeConductorExtension


class AzureExtension(NodeConductorExtension):

    @staticmethod
    def django_app():
        return 'nodeconductor_azure'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in
