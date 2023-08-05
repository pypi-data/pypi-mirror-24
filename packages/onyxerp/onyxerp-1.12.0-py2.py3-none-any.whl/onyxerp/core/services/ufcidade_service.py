from onyxerp.core.api.request import Request
from onyxerp.core.services.onyxerp_service import OnyxErpService


class UfCidadeService(Request, OnyxErpService):

    jwt = None

    def __init__(self, base_url):
        super(UfCidadeService, self).__init__(base_url)

    def get_cidade(self, cidade_cod: int()):
        response = self.get("/v1/cidade/{0}/".format(cidade_cod))

        status = response.get_status_code()

        if status == 200:
            return response.get_decoded()
        else:
            return {
                "status": status,
                "response": response.get_content()
            }
