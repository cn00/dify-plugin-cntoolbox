import os
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.email_address import EmailAddress
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.message import Message
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.attachment import Attachment


class GraphApi:
    username: str
    tenant_id: str
    client_id: str
    client_secret: str
    scopes: [str]
    def __init__(self, username, tenant_id, client_id, client_secret, scopes):
        self.username = username
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.graph_client = self.getClient()

    async def sendMail(self, to: [str], subject: str, content_type: BodyType, content: str,
                       attachments: [Attachment] = None, cc: [str] = None) -> None:
        from msgraph.generated.users.item.send_mail.send_mail_post_request_body import (
            SendMailPostRequestBody
        )
        if attachments is None:
            attachments = []
        if cc is None:
            cc = []
        request_body = SendMailPostRequestBody(
            message=Message(
                subject=subject,
                body=ItemBody(
                    content_type=content_type,
                    content=content,
                ),
                attachments=attachments,
                to_recipients=[
                    Recipient(
                        email_address=EmailAddress(
                            address=i,
                        ),
                    ) for i in to
                ],
                cc_recipients=[
                    Recipient(
                        email_address=EmailAddress(
                            address=i,
                        ),
                    ) for i in cc
                ],
            ),
            save_to_sent_items=False,
        )
        graph_client = self.graph_client
        await graph_client.users.by_user_id(self.username).send_mail.post(request_body)

    def getClient(self):
        from azure.identity.aio import (
            ClientSecretCredential
        )
        from plugin.msgraph.tools.msgraph import GraphServiceClient

        # https://github.com/Azure-Samples/ms-identity-python-webapp
        # https://learn.microsoft.com/zh-cn/entra/msal/python/
        # azure.identity.aio
        credential = ClientSecretCredential(
            tenant_id    =self.tenant_id,
            client_id    =self.client_id,
            client_secret=self.client_secret
        )

        graph_client = GraphServiceClient(
            credentials=credential,
            scopes=self.scopes,
        )
        return graph_client
