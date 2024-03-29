<!--
This Markdown has been generated by essentials-openapi
https://github.com/Neoteroi/essentials-openapi

Most likely, it is not desirable to edit this file by hand!
-->

# Software Platform API <span class="api-version">v1</span>

Optional multiline or single-line description in
[CommonMark](http://commonmark.org/help/) or HTML.
<hr />
## <span class="api-tag">Blobs</span>

<hr class="operation-separator" />

### <span class="http-post">POST</span> /api/blobs/initialize-upload
Initializes a file upload operation.

??? note "Description"
    The client receives a Shared Access Signature that can be used to upload a
    file directly to the Azure Storage Blob Service.

<p class="request-body-title"><strong>Request body</strong></p>



=== "application/json"


    ```json
    {
        "releaseId": "00000000-0000-0000-0000-000000000000",
        "fileName": "string",
        "fileSize": 131,
        "fileType": "string"
    }
    ```
    <span class="small-note">⚠️</span>&nbsp;<em class="small-note warning">This example has been generated automatically from the schema and it is not accurate. Refer to the schema for more information.</em>



    ??? hint "Schema of the request body"
        ```json
        {
            "type": "object",
            "properties": {
                "releaseId": {
                    "type": "string",
                    "format": "uuid"
                },
                "fileName": {
                    "type": "string",
                    "nullable": true
                },
                "fileSize": {
                    "type": "integer",
                    "format": "int32"
                },
                "fileType": {
                    "type": "string",
                    "nullable": true
                }
            },
            "additionalProperties": false
        }
        ```



<p class="response-title">
    <strong>Response <span class="response-code code-200">200</span>&nbsp;<span class="status-phrase">OK</span></strong>
</p>

=== "application/json"



    ??? hint "Schema of the response body"
        ```json
        {
            "type": "object"
        }
        ```



<p class="response-title">
    <strong>Response <span class="response-code code-400">400</span>&nbsp;<span class="status-phrase">Bad Request</span></strong>
</p>
<div class="common-response"><p>Refer to the common response description: <a href="#illegalinput" class="ref-link">IllegalInput</a>.</p></div>

<p class="response-title">
    <strong>Response <span class="response-code code-401">401</span>&nbsp;<span class="status-phrase">Unauthorized</span></strong>
</p>
<div class="common-response"><p>Refer to the common response description: <a href="#unauthorized" class="ref-link">Unauthorized</a>.</p></div>




---
## Schemas


### GenericError

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>code</code></td>
            <td><span class="integer-type">integer</span>(<span class="int32-format format">int32</span>)</td>
        </tr>
        <tr>
            <td><code>message</code></td>
            <td><span class="string-type">string</span></td>
        </tr>
    </tbody>
</table>



### HealthCheck

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>alive</code></td>
            <td><span class="boolean-type">boolean</span></td>
        </tr>
        <tr>
            <td><code>regionName</code></td>
            <td><span class="string-type">string</span>&#124; <span class="null-type">null</span></td>
        </tr>
        <tr>
            <td><code>timestamp</code></td>
            <td><span class="string-type">string</span>(<span class="date-time-format format">date-time</span>)</td>
        </tr>
    </tbody>
</table>



### InitializeUploadInput

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>fileName</code></td>
            <td><span class="string-type">string</span>&#124; <span class="null-type">null</span></td>
        </tr>
        <tr>
            <td><code>fileSize</code></td>
            <td><span class="integer-type">integer</span>(<span class="int32-format format">int32</span>)</td>
        </tr>
        <tr>
            <td><code>fileType</code></td>
            <td><span class="string-type">string</span>&#124; <span class="null-type">null</span></td>
        </tr>
        <tr>
            <td><code>releaseId</code></td>
            <td><span class="string-type">string</span>(<span class="uuid-format format">uuid</span>)</td>
        </tr>
    </tbody>
</table>



### InitializeUploadOutput




## Common responses

This section describes common responses that are reused across operations.



### NotFound
Entity not found.

<p class="message-separator"></p>

=== "application/json"


    ```json
    {
        "code": 404,
        "message": "Entity not found"
    }
    ```




    ??? hint "Schema of the response body"
        ```json
        {
            "type": "object",
            "properties": {
                "code": {
                    "type": "integer",
                    "format": "int32"
                },
                "message": {
                    "type": "string"
                }
            }
        }
        ```






### IllegalInput
Illegal input for operation.

<p class="message-separator"></p>

=== "application/json"


    ```json
    {
        "code": 400,
        "message": "Illegal Input"
    }
    ```




    ??? hint "Schema of the response body"
        ```json
        {
            "type": "object",
            "properties": {
                "code": {
                    "type": "integer",
                    "format": "int32"
                },
                "message": {
                    "type": "string"
                }
            }
        }
        ```






### Unauthorized
The user is not authorized.

<p class="message-separator"></p>

=== "application/json"


    ```json
    {
        "code": 401,
        "message": "Unauthorized"
    }
    ```




    ??? hint "Schema of the response body"
        ```json
        {
            "type": "object",
            "properties": {
                "code": {
                    "type": "integer",
                    "format": "int32"
                },
                "message": {
                    "type": "string"
                }
            }
        }
        ```






### GenericError
This base error type is used for all raised exceptions.

<p class="message-separator"></p>

=== "application/json"


    ```json
    {
        "code": 195,
        "message": "string"
    }
    ```
    <span class="small-note">⚠️</span>&nbsp;<em class="small-note warning">This example has been generated automatically from the schema and it is not accurate. Refer to the schema for more information.</em>



    ??? hint "Schema of the response body"
        ```json
        {
            "type": "object",
            "properties": {
                "code": {
                    "type": "integer",
                    "format": "int32"
                },
                "message": {
                    "type": "string"
                }
            }
        }
        ```






## Common parameters

This section describes common parameters that are reused across operations.



### PageNumber

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>In</th>
            <th>Type</th>
            <th>Default</th>
            <th>Nullable</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="parameter-name"><code>page</code></td>
            <td>query</td>
            <td>integer</td>
            <td>1</td>
            <td>Yes</td>
            <td></td>
        </tr>
    </tbody>
</table>
