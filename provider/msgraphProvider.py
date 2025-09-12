from typing import Any
import logging
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
import asyncio

from tools.msgraphApi import GraphApi

class MSGraphProvider(ToolProvider):
    logger = logging.getLogger()
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        def getenv(key: str, default: str | None = None) -> str | None:
            return credentials[key] if key in credentials else default

        self.logger.info(f'============credentials:{credentials}')
        try:
            """
            IMPLEMENT YOUR VALIDATION HERE
            """
            required_keys = [
                "MICROSOFT_GRAPH_USERNAME", 
                "MICROSOFT_GRAPH_CLIENTID", 
                "MICROSOFT_GRAPH_CLIENTSECRET", 
                "MICROSOFT_GRAPH_TENANTID",
                "MICROSOFT_GRAPH_TEST_EMAIL"
            ]
            for key in required_keys:
                if key not in credentials:
                    raise ToolProviderCredentialValidationError(f"Missing required credential: {key}")
            username        = getenv('MICROSOFT_GRAPH_USERNAME')
            client_id       = getenv('MICROSOFT_GRAPH_CLIENTID')
            client_secret   = getenv('MICROSOFT_GRAPH_CLIENTSECRET')
            tenant_id       = getenv('MICROSOFT_GRAPH_TENANTID', 'common')
            scopes_1        = getenv('MICROSOFT_GRAPH_SCOPE_1', 'https://graph.microsoft.com/.default')
            test_email      = getenv('MICROSOFT_GRAPH_TEST_EMAIL', 'cool.navy@outlook.com')
            self.logger.info(f'''username:{username} client_id:{client_id}''')
            
            api = GraphApi(username, tenant_id, client_id, client_secret, [scopes_1])
            asyncio.run(api.sendMail(to=[test_email], subject='Test Email', content_type='text', content='Hello from Dify msgraph plugin'))

        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
