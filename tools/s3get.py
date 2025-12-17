import base64
from collections.abc import Generator
from io import BytesIO
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

import boto3
from botocore.client import Config
import os

class S3Gut(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        AWS_REGION         = tool_parameters.get("AWS_REGION", "cn-northwest-1")
        bucket         = tool_parameters.get("bucket", 'snn-udi-s3')
        s3key         = tool_parameters.get("s3key", "No Subject")
        content_type    = tool_parameters.get("content_type", "text")
        
        session = boto3.Session()
        s3_client = session.client(
            's3',
            region_name=AWS_REGION,
            config=Config(signature_version='s3v4')
        )

        try:
            response = s3_client.get_object(
                Bucket=bucket,
                Key=s3key,
                # Body=BytesIO(content_bytes),
                # ContentType='application/json'
            )
            content = response['Body'].read()
            # 如果是非文本则 base64 编码
            content_str =  content_type == 'base64' and base64.b64encode(content) or content.decode('utf-8')
            yield self.create_json_message({
                "status": "success",
                "s3key": s3key,
                "Bucket": bucket,
                "content_type": content_type,
                "content": content_str,
            })
        except Exception as e:
            yield self.create_json_message({
                "status": "error",
                "s3key": s3key,
                "Bucket": bucket,
                "content_type": content_type,
                "message": str(e),
                "tool_parameters": tool_parameters,
            })
