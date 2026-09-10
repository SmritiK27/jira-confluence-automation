$ErrorActionPreference = "Stop"

function Send-Response {
    param(
        [long]$Id,
        [object]$Result
    )

    $response = @{
        jsonrpc = "2.0"
        id = $Id
        result = $Result
    } | ConvertTo-Json -Compress -Depth 10

    [Console]::Out.WriteLine($response)
    [Console]::Out.Flush()
}

while ($null -ne ($line = [Console]::In.ReadLine())) {
    if ([string]::IsNullOrWhiteSpace($line)) {
        continue
    }

    $request = $line | ConvertFrom-Json
    if ($null -eq $request.id) {
        continue
    }

    switch ($request.method) {
        "initialize" {
            Send-Response $request.id @{
                protocolVersion = "2024-11-05"
                capabilities = @{ tools = @{} }
                serverInfo = @{
                    name = "echo-windows"
                    version = "1.0.0"
                }
            }
        }
        "tools/list" {
            Send-Response $request.id @{
                tools = @(
                    @{
                        name = "echo"
                        description = "Echo text back to the caller."
                        inputSchema = @{
                            type = "object"
                            properties = @{
                                message = @{
                                    type = "string"
                                    description = "Text to echo."
                                }
                            }
                            required = @("message")
                        }
                    }
                )
            }
        }
        "tools/call" {
            $message = $request.params.arguments.message
            Send-Response $request.id @{
                content = @(
                    @{
                        type = "text"
                        text = [string]$message
                    }
                )
            }
        }
    }
}
