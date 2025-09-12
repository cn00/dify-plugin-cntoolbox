from collections.abc import Generator
from typing import Any
import asyncio
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from msgraph.generated.models.body_type import BodyType
from tools.msgraphApi import GraphApi
from tools.markdown_utils import convert_markdown_to_html
class SendMail(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        subject         = tool_parameters.get("subject", "No Subject")
        content         = tool_parameters.get("content", "No Content")
        recipients      = tool_parameters.get("recipients", "cool-navy@outlook.com")
        content_type    = tool_parameters.get("content_type", "text")
        try:
            api = GraphApi(
                username        =self.runtime.credentials["MICROSOFT_GRAPH_USERNAME"],
                tenant_id       =self.runtime.credentials["MICROSOFT_GRAPH_TENANTID"],
                client_id       =self.runtime.credentials["MICROSOFT_GRAPH_CLIENTID"],
                client_secret   =self.runtime.credentials["MICROSOFT_GRAPH_CLIENTSECRET"],
                scopes          =[self.runtime.credentials["MICROSOFT_GRAPH_SCOPE_1"]],
            )
            (html, plain_text_content) = convert_markdown_to_html(content)
            asyncio.run(api.sendMail(
                to=[i.strip() for i in recipients.split(",")],
                subject=subject,
                content_type=content_type,
                content=(html if content_type == 'html' else plain_text_content),
            ))
        except Exception as e:
            yield self.create_text_message(text=f'tool_parameters:{tool_parameters} err:{str(e)}')
