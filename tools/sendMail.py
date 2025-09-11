from collections.abc import Generator
from typing import Any
import asyncio
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from msgraph.generated.models.body_type import BodyType
from ..tools.msgraph import GraphApi

class SendMail(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        subject = tool_parameters.get("subject", "No Subject")
        content = tool_parameters.get("content", "No Content")
        recipients = tool_parameters.get("recipients", [])
        api = GraphApi(
            username        =self.runtime.credentials["MICROSOFT_GRAPH_USERNAME"],
            tenant_id       =self.runtime.credentials["MICROSOFT_GRAPH_TENANTID"],
            client_id       =self.runtime.credentials["MICROSOFT_GRAPH_CLIENTID"],
            client_secret   =self.runtime.credentials["MICROSOFT_GRAPH_CLIENTSECRET"],
            scopes          =[self.runtime.credentials["MICROSOFT_GRAPH_SCOPE_1"]],
        )
        asyncio.run(api.sendMail(
            to=[i.strip() for i in recipients],
            subject=subject,
            content_type=BodyType.TEXT,
            content=content,
        ))
        # yield ToolInvokeMessage(
        #     tool=api,
        #     action="sendMail",
        #     parameters={
        #         "to": [i.strip() for i in recipients],
        #         "subject": subject,
        #         "content_type": BodyType.TEXT,
        #         "content": content,
        #     },
        # )