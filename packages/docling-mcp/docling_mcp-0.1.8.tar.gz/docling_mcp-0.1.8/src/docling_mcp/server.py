import os
import time
import docling
import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from docling.datamodel.base_models import InputFormat
import mcp.server.stdio as stdio
import logging
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from pathlib import Path

server = Server("docling-mcp")

_log = logging.getLogger(__name__)

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="convert",
            description=("Converts a document to another format"),
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "The input file path"
                    },
                    "destination": {
                        "type": "string",
                        "description": "The output file path"
                    }
                },
                "required": ["source"]
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, params: dict | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name not in ["convert"]:
        raise ValueError(f"Unknown tool: {name}")
    
    print(params)

    if not params:
        raise ValueError("No parameters provided")
    
    input_file = params.get("source")
    output_file = params.get("destination")

    if not input_file:
        raise ValueError("No input file provided")
    
    try:
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = True
        pipeline_options.ocr_options.use_gpu = False  # <-- set this.
        pipeline_options.do_table_structure = True
        pipeline_options.table_structure_options.do_cell_matching = True

        doc_converter = DocumentConverter()   
        start_time = time.time()
        conv_result = doc_converter.convert(Path(input_file))
        end_time = time.time() - start_time
        _log.info(f"Document converted in {end_time:.2f} seconds.")
        output_dir = Path("scratch")
        output_dir.mkdir(parents=True, exist_ok=True)
        doc_filename = conv_result.input.file.stem
        
        if not output_file:
            with (output_dir / f"{doc_filename}.md").open("w", encoding="utf-8") as fp:
                fp.write(conv_result.document.export_to_markdown())
            notify = f"Converted Content saved to {conv_result.document.export_to_markdown()}."
        else:
            with (output_dir / f"{doc_filename}.md").open("w", encoding="utf-8") as fp:
                fp.write(conv_result.document.export_to_markdown())
            notify = f"Converted Content saved to {output_dir}."
        _log.info(f"got this: {notify}")
        return [types.TextContent(type="text", text=notify)]
    except Exception as e:
        raise ValueError(f"Error converting file: {e}")

async def main():

    logging.basicConfig(level=logging.INFO)

    async with stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="docling-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )