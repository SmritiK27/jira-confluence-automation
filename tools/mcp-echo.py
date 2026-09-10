#!/usr/bin/env python3
"""Minimal MCP stdio server exposing echo and time tools."""

from datetime import datetime
import json
import sys


def send_message(message: dict) -> None:
    payload = json.dumps(message, separators=(",", ":")).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(payload)}\r\n\r\n".encode("ascii"))
    sys.stdout.buffer.write(payload)
    sys.stdout.buffer.flush()


def read_message() -> dict | None:
    content_length = None
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        name, separator, value = line.decode("ascii").partition(":")
        if separator and name.lower() == "content-length":
            content_length = int(value.strip())

    if content_length is None:
        raise ValueError("MCP message is missing Content-Length")
    payload = sys.stdin.buffer.read(content_length)
    if len(payload) != content_length:
        raise EOFError("MCP message ended before Content-Length bytes were read")
    return json.loads(payload)


def main() -> None:
    while True:
        request = read_message()
        if request is None:
            return
        request_id = request.get("id")
        if request_id is None:
            continue

        method = request.get("method")
        if method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "echo", "version": "1.0.0"},
            }
        elif method == "tools/list":
            result = {
                "tools": [
                    {
                        "name": "echo",
                        "description": "Echo text back to the caller.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"message": {"type": "string"}},
                            "required": ["message"],
                        },
                    },
                    {
                        "name": "get_time",
                        "description": "Get the current local time with timezone information.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                            "additionalProperties": False,
                        },
                    },
                ]
            }
        elif method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            if tool_name == "echo":
                text = str(arguments.get("message", ""))
            elif tool_name == "get_time":
                now = datetime.now().astimezone()
                text = now.strftime("%Y-%m-%d %H:%M:%S %Z (%z)")
            else:
                send_message(
                    {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32602,
                            "message": f"Unknown tool: {tool_name}",
                        },
                    }
                )
                continue
            result = {"content": [{"type": "text", "text": text}]}
        elif method == "ping":
            result = {}
        else:
            send_message(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"Unknown method: {method}"},
                }
            )
            continue

        send_message({"jsonrpc": "2.0", "id": request_id, "result": result})


if __name__ == "__main__":
    main()
