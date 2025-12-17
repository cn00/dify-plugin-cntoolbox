import base64
from collections.abc import Generator
from io import BytesIO
from typing import Any
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

# 使用自定义处理器设置日志
import logging
from dify_plugin.config.logger_format import plugin_logger_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(plugin_logger_handler)

class S3Put(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        self.duckdb = self.duckdb_init(tool_parameters)
        sql_query   = tool_parameters.get("sql_query", "select * from duckdb_extensions();")
        return_type = tool_parameters.get("return_type", "json").strip().lower()
        # extra_json_data = tool_parameters.get("extra_json_data", None)
        # if extra_json_data:
        #     try:
        #         import json
        #         import pandas as pd
        #         extra_params = json.loads(extra_json_data)
        #         extra_json_data = pd.DataFrame(extra_params)
        #     except Exception as e:
        #         yield self.create_json_message({
        #             "status": "error",
        #             "message": f"Invalid extra_json_data: {str(e)}",
        #             "tool_parameters": tool_parameters,
        #         })
        #         return
            
        try:
            self.duckdb.execute(sql_query)
            if return_type == "json":
                result = self.duckdb.fetchall()
                headers = [desc[0] for desc in self.duckdb.description]
                # result = [dict(zip(headers, row)) for row in result]
                yield self.create_json_message({
                    "status": "success",
                    "headers": headers,
                    "result": result,
                })
            elif return_type == "html":
                df = self.duckdb.df()
                html_str = df.to_html(index=False)
                yield self.create_text_message(html_str)
        except Exception as e:
            yield self.create_json_message({
                "status": "error",
                "message": str(e),
                "tool_parameters": tool_parameters,
            })

    def duckdb_init(self, tool_parameters: dict[str, Any]):
        AWS_REGION        = tool_parameters.get("AWS_REGION", "cn-northwest-1")
        ENV               = tool_parameters.get("ENV", "prod").strip().lower()
        aws_s3_endpoint   = tool_parameters.get("aws_s3_endpoint", 's3.cn-northwest-1.amazonaws.com.cn')

        import duckdb
        db = duckdb.connect(':memory:')
        if ENV == 'local':
            sql = f'''
                SET s3_endpoint = 's3.{AWS_REGION}.amazonaws.com.cn';
                call load_aws_credentials('dw-dev');
            '''
        else:
            home_directory = '/tmp/duckdb/'
            sql = f'''
            SET home_directory='{home_directory}';
            SET temp_directory='{home_directory}';
            SET extension_directory = '/app/storage/duckdb_extension';
            SET s3_endpoint = '{aws_s3_endpoint}';
            INSTALL httpfs;
            INSTALL aws;
            INSTALL mysql;
            call load_aws_credentials();
        '''
        db.execute(sql)
        # logging.info(sql)
        return db
