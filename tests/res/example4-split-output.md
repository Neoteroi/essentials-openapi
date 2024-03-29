<!--
This Markdown has been generated by essentials-openapi
https://github.com/Neoteroi/essentials-openapi

Most likely, it is not desirable to edit this file by hand!
-->

# Split Public API <span class="api-version">v1</span>

split Public API
<hr />
<div class="terms-of-service info-data">
    <strong>Terms of service:</strong> <a href="https://split.io/legal/terms" target="_blank" rel="noopener noreferrer">https://split.io/legal/terms</a>
</div>

## Servers

<table>
    <thead>
        <tr>
            <th>Description</th>
            <th>URL</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>https://www.neoteroi.xyz/split/api/v1</td>
            <td>
                <a href="https://www.neoteroi.xyz/split/api/v1" target="_blank" rel="noopener noreferrer">https://www.neoteroi.xyz/split/api/v1</a>
            </td>
        </tr>
    </tbody>
</table>

## <span class="api-tag">User</span>

<hr class="operation-separator" />

### <span class="http-post">POST</span> /users
Invite a user

??? note "Description"
    Invites a user to your instance. Only available for the instance owner.


**Input parameters**

<table>
    <thead>
        <tr>
            <th>Parameter</th>
            <th>In</th>
            <th>Type</th>
            <th>Default</th>
            <th>Nullable</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="parameter-name"><code>ApiKeyAuth</code></td>
            <td>header</td>
            <td>string</td>
            <td>N/A</td>
            <td>No</td>
            <td>API key</td>
        </tr>
    </tbody>
</table>
<p class="request-body-title"><strong>Request body</strong></p>



=== "application/json"
    
    
    ```json
    [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "john.doe@company.com",
            "firstName": "john",
            "lastName": "Doe",
            "isPending": true,
            "createdAt": "2022-04-13T15:42:05.901Z",
            "updatedAt": "2022-04-13T15:42:05.901Z",
            "globalRole": {
                "id": 1,
                "name": "owner",
                "scope": "global",
                "createdAt": "2022-04-13T15:42:05.901Z",
                "updatedAt": "2022-04-13T15:42:05.901Z"
            }
        }
    ]
    ```
    <span class="small-note">⚠️</span>&nbsp;<em class="small-note warning">This example has been generated automatically from the schema and it is not accurate. Refer to the schema for more information.</em>

    

    ??? hint "Schema of the request body"
        ```json
        {
            "type": "array",
            "items": {
                "$ref": "#/components/schemas/UserInformation"
            }
        }
        ```



<p class="response-title">
    <strong>Response <span class="response-code code-200">200</span>&nbsp;<span class="status-phrase">OK</span></strong>
</p>

=== "application/json"
    
    
    ```json
    [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "email": "john.doe@company.com",
            "firstName": "john",
            "lastName": "Doe",
            "isPending": true,
            "createdAt": "2022-04-13T15:42:05.901Z",
            "updatedAt": "2022-04-13T15:42:05.901Z",
            "globalRole": {
                "id": 1,
                "name": "owner",
                "scope": "global",
                "createdAt": "2022-04-13T15:42:05.901Z",
                "updatedAt": "2022-04-13T15:42:05.901Z"
            }
        }
    ]
    ```
    <span class="small-note">⚠️</span>&nbsp;<em class="small-note warning">This example has been generated automatically from the schema and it is not accurate. Refer to the schema for more information.</em>

    

    ??? hint "Schema of the response body"
        ```json
        {
            "type": "array",
            "items": {
                "$ref": "#/components/schemas/UserInformation"
            }
        }
        ```



<p class="response-title">
    <strong>Response <span class="response-code code-401">401</span>&nbsp;<span class="status-phrase">Unauthorized</span></strong>
</p>
<div class="common-response"><p>Refer to the common response description: <a href="#unauthorized" class="ref-link">Unauthorized</a>.</p></div>
<hr class="operation-separator" />

### <span class="http-get">GET</span> /users
Retrieve all users

??? note "Description"
    Retrieve all users from your instance. Only available for the instance
    owner.


**Input parameters**

<table>
    <thead>
        <tr>
            <th>Parameter</th>
            <th>In</th>
            <th>Type</th>
            <th>Default</th>
            <th>Nullable</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="parameter-name"><code>ApiKeyAuth</code></td>
            <td>header</td>
            <td>string</td>
            <td>N/A</td>
            <td>No</td>
            <td>API key</td>
        </tr>
        <tr>
            <td class="parameter-name"><code>cursor</code></td>
            <td>query</td>
            <td>string</td>
            <td></td>
            <td>No</td>
            <td>Paginate through users by setting the cursor parameter to a nextCursor attribute returned by a previous request's response. Default value fetches the first "page" of the collection. See pagination for more detail.</td>
        </tr>
        <tr>
            <td class="parameter-name"><code>limit</code></td>
            <td>query</td>
            <td>number</td>
            <td>100</td>
            <td>No</td>
            <td>The maximum number of items to return.</td>
        </tr>
    </tbody>
</table>

<p class="response-title">
    <strong>Response <span class="response-code code-200">200</span>&nbsp;<span class="status-phrase">OK</span></strong>
</p>

=== "application/json"
    
    
    ```json
    {
        "data": [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "john.doe@company.com",
                "firstName": "john",
                "lastName": "Doe",
                "isPending": true,
                "createdAt": "2022-04-13T15:42:05.901Z",
                "updatedAt": "2022-04-13T15:42:05.901Z",
                "globalRole": {
                    "id": 1,
                    "name": "owner",
                    "scope": "global",
                    "createdAt": "2022-04-13T15:42:05.901Z",
                    "updatedAt": "2022-04-13T15:42:05.901Z"
                }
            }
        ],
        "nextCursor": "MTIzZTQ1NjctZTg5Yi0xMmQzLWE0NTYtNDI2NjE0MTc0MDA"
    }
    ```
    <span class="small-note">⚠️</span>&nbsp;<em class="small-note warning">This example has been generated automatically from the schema and it is not accurate. Refer to the schema for more information.</em>

    

    ??? hint "Schema of the response body"
        ```json
        {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {
                        "$ref": "#/components/schemas/UserInformation"
                    }
                },
                "nextCursor": {
                    "type": "string",
                    "description": "Paginate through users by setting the cursor parameter to a nextCursor attribute returned by a previous request. Default value fetches the first \"page\" of the collection.",
                    "nullable": true,
                    "example": "MTIzZTQ1NjctZTg5Yi0xMmQzLWE0NTYtNDI2NjE0MTc0MDA"
                }
            }
        }
        ```



<p class="response-title">
    <strong>Response <span class="response-code code-401">401</span>&nbsp;<span class="status-phrase">Unauthorized</span></strong>
</p>
<div class="common-response"><p>Refer to the common response description: <a href="#unauthorized" class="ref-link">Unauthorized</a>.</p></div>

<hr class="operation-separator" />

### <span class="http-get">GET</span> /users/<span class="route-param">{identifier}</span>
Get user by ID/Email

??? note "Description"
    Retrieve a user from your instance. Only available for the instance owner.


**Input parameters**

<table>
    <thead>
        <tr>
            <th>Parameter</th>
            <th>In</th>
            <th>Type</th>
            <th>Default</th>
            <th>Nullable</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="parameter-name"><code>ApiKeyAuth</code></td>
            <td>header</td>
            <td>string</td>
            <td>N/A</td>
            <td>No</td>
            <td>API key</td>
        </tr>
        <tr>
            <td class="parameter-name"><code>identifier</code></td>
            <td>path</td>
            <td>string</td>
            <td></td>
            <td>No</td>
            <td>The ID or email of the user.</td>
        </tr>
    </tbody>
</table>

<p class="response-title">
    <strong>Response <span class="response-code code-200">200</span>&nbsp;<span class="status-phrase">OK</span></strong>
</p>
<div class="common-response"><p>Refer to the common response description: <a href="#userinformation" class="ref-link">UserInformation</a>.</p></div>

<p class="response-title">
    <strong>Response <span class="response-code code-401">401</span>&nbsp;<span class="status-phrase">Unauthorized</span></strong>
</p>
<div class="common-response"><p>Refer to the common response description: <a href="#unauthorized" class="ref-link">Unauthorized</a>.</p></div>
<hr class="operation-separator" />

### <span class="http-delete">DELETE</span> /users/<span class="route-param">{identifier}</span>
Delete user by ID/Email

??? note "Description"
    Deletes a user from your instance. Only available for the instance owner.


**Input parameters**

<table>
    <thead>
        <tr>
            <th>Parameter</th>
            <th>In</th>
            <th>Type</th>
            <th>Default</th>
            <th>Nullable</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="parameter-name"><code>ApiKeyAuth</code></td>
            <td>header</td>
            <td>string</td>
            <td>N/A</td>
            <td>No</td>
            <td>API key</td>
        </tr>
        <tr>
            <td class="parameter-name"><code>identifier</code></td>
            <td>path</td>
            <td>string</td>
            <td></td>
            <td>No</td>
            <td>The ID or email of the user.</td>
        </tr>
        <tr>
            <td class="parameter-name"><code>transferId</code></td>
            <td>query</td>
            <td>string</td>
            <td></td>
            <td>No</td>
            <td>ID of the user to transfer workflows and credentials to. Must not be equal to the to-be-deleted user.</td>
        </tr>
    </tbody>
</table>

<p class="response-title">
    <strong>Response <span class="response-code code-200">200</span>&nbsp;<span class="status-phrase">OK</span></strong>
</p>
<div class="common-response"><p>Refer to the common response description: <a href="#userinformation" class="ref-link">UserInformation</a>.</p></div>

<p class="response-title">
    <strong>Response <span class="response-code code-401">401</span>&nbsp;<span class="status-phrase">Unauthorized</span></strong>
</p>
<div class="common-response"><p>Refer to the common response description: <a href="#unauthorized" class="ref-link">Unauthorized</a>.</p></div>




---
## Schemas


### Error

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
            <td><span class="string-type">string</span></td>
        </tr>
        <tr>
            <td><code>description</code></td>
            <td><span class="string-type">string</span></td>
        </tr>
        <tr>
            <td><code>message</code></td>
            <td><span class="string-type">string</span></td>
        </tr>
    </tbody>
</table>



### RoleInformation

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>createdAt</code></td>
            <td><span class="string-type">string</span>(<span class="date-time-format format">date-time</span>)</td>
        </tr>
        <tr>
            <td><code>id</code></td>
            <td><span class="number-type">number</span></td>
        </tr>
        <tr>
            <td><code>name</code></td>
            <td><span class="string-type">string</span></td>
        </tr>
        <tr>
            <td><code>scope</code></td>
            <td><span class="string-type">string</span></td>
        </tr>
        <tr>
            <td><code>updatedAt</code></td>
            <td><span class="string-type">string</span>(<span class="date-time-format format">date-time</span>)</td>
        </tr>
    </tbody>
</table>



### UserDetailsResponse

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>data</code></td>
            <td>Array&lt;<a href="#userinformation" class="ref-link">UserInformation</a>&gt;</td>
        </tr>
        <tr>
            <td><code>nextCursor</code></td>
            <td><span class="string-type">string</span>&#124; <span class="null-type">null</span></td>
        </tr>
    </tbody>
</table>



### UserInformation

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>createdAt</code></td>
            <td><span class="string-type">string</span>(<span class="date-time-format format">date-time</span>)</td>
        </tr>
        <tr>
            <td><code>email</code></td>
            <td><span class="string-type">string</span>(<span class="email-format format">email</span>)</td>
        </tr>
        <tr>
            <td><code>firstName</code></td>
            <td><span class="string-type">string</span></td>
        </tr>
        <tr>
            <td><code>globalRole</code></td>
            <td><a href="#roleinformation" class="ref-link">RoleInformation</a></td>
        </tr>
        <tr>
            <td><code>id</code></td>
            <td><span class="string-type">string</span></td>
        </tr>
        <tr>
            <td><code>isPending</code></td>
            <td><span class="boolean-type">boolean</span></td>
        </tr>
        <tr>
            <td><code>lastName</code></td>
            <td><span class="string-type">string</span></td>
        </tr>
        <tr>
            <td><code>updatedAt</code></td>
            <td><span class="string-type">string</span>(<span class="date-time-format format">date-time</span>)</td>
        </tr>
    </tbody>
</table>



## Common responses

This section describes common responses that are reused across operations.



### NotFound
The specified resource was not found.

<p class="message-separator"></p>

=== "application/json"
    
    
    ```json
    {
        "code": "string",
        "message": "string",
        "description": "string"
    }
    ```
    <span class="small-note">⚠️</span>&nbsp;<em class="small-note warning">This example has been generated automatically from the schema and it is not accurate. Refer to the schema for more information.</em>

    

    ??? hint "Schema of the response body"
        ```json
        {
            "required": [
                "code",
                "description",
                "message"
            ],
            "type": "object",
            "properties": {
                "code": {
                    "type": "string"
                },
                "message": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                }
            }
        }
        ```






### Unauthorized
Unauthorized

<p class="message-separator"></p>

=== "application/json"
    
    
    ```json
    {
        "code": "string",
        "message": "string",
        "description": "string"
    }
    ```
    <span class="small-note">⚠️</span>&nbsp;<em class="small-note warning">This example has been generated automatically from the schema and it is not accurate. Refer to the schema for more information.</em>

    

    ??? hint "Schema of the response body"
        ```json
        {
            "required": [
                "code",
                "description",
                "message"
            ],
            "type": "object",
            "properties": {
                "code": {
                    "type": "string"
                },
                "message": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                }
            }
        }
        ```






### UserInformation
Operation successful.

<p class="message-separator"></p>

=== "application/json"
    
    
    ```json
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "email": "john.doe@company.com",
        "firstName": "john",
        "lastName": "Doe",
        "isPending": true,
        "createdAt": "2022-04-13T15:42:05.901Z",
        "updatedAt": "2022-04-13T15:42:05.901Z",
        "globalRole": {
            "id": 1,
            "name": "owner",
            "scope": "global",
            "createdAt": "2022-04-13T15:42:05.901Z",
            "updatedAt": "2022-04-13T15:42:05.901Z"
        }
    }
    ```
    <span class="small-note">⚠️</span>&nbsp;<em class="small-note warning">This example has been generated automatically from the schema and it is not accurate. Refer to the schema for more information.</em>

    

    ??? hint "Schema of the response body"
        ```json
        {
            "required": [
                "email"
            ],
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "readOnly": true,
                    "example": "123e4567-e89b-12d3-a456-426614174000"
                },
                "email": {
                    "type": "string",
                    "format": "email",
                    "example": "john.doe@company.com"
                },
                "firstName": {
                    "maxLength": 32,
                    "type": "string",
                    "description": "User's first name",
                    "readOnly": true,
                    "example": "john"
                },
                "lastName": {
                    "maxLength": 32,
                    "type": "string",
                    "description": "User's last name",
                    "readOnly": true,
                    "example": "Doe"
                },
                "isPending": {
                    "type": "boolean",
                    "description": "Whether the user finished setting up their account in response to the invitation (true) or not (false).",
                    "readOnly": true
                },
                "createdAt": {
                    "type": "string",
                    "description": "Time the user was created.",
                    "format": "date-time",
                    "readOnly": true
                },
                "updatedAt": {
                    "type": "string",
                    "description": "Last time the user was updated.",
                    "format": "date-time",
                    "readOnly": true
                },
                "globalRole": {
                    "$ref": "#/components/schemas/RoleInformation"
                }
            }
        }
        ```






## Common parameters

This section describes common parameters that are reused across operations.



### UserIdentifier

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
            <td class="parameter-name"><code>identifier</code></td>
            <td>path</td>
            <td>string</td>
            <td></td>
            <td>No</td>
            <td></td>
        </tr>
    </tbody>
</table>



### Cursor

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
            <td class="parameter-name"><code>cursor</code></td>
            <td>query</td>
            <td>string</td>
            <td></td>
            <td>No</td>
            <td></td>
        </tr>
    </tbody>
</table>



### includeRole

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
            <td class="parameter-name"><code>includeRole</code></td>
            <td>query</td>
            <td>boolean</td>
            <td></td>
            <td>No</td>
            <td></td>
        </tr>
    </tbody>
</table>



### Limit

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
            <td class="parameter-name"><code>limit</code></td>
            <td>query</td>
            <td>number</td>
            <td>100</td>
            <td>No</td>
            <td></td>
        </tr>
    </tbody>
</table>



### ExecutionId

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
            <td class="parameter-name"><code>executionId</code></td>
            <td>path</td>
            <td>number</td>
            <td></td>
            <td>No</td>
            <td></td>
        </tr>
    </tbody>
</table>



### WorkflowId

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
            <td class="parameter-name"><code>workflowId</code></td>
            <td>path</td>
            <td>number</td>
            <td></td>
            <td>No</td>
            <td></td>
        </tr>
    </tbody>
</table>



## Security schemes

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Scheme</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        
        <tr>
            <td>ApiKeyAuth</td>
            <td>apiKey</td>
            <td></td>
            <td></td>
        </tr>
        
    </tbody>
</table>

## Tags

| Name | Description             |
| ---- | ----------------------- |
| User | Operations about users. |


## More documentation

split API documentation

<hr /><div class="external-docs info-data">
    <strong>For more information:</strong> <a href="https://www.neoteroi.xyz/" target="_blank" rel="noopener noreferrer">https://www.neoteroi.xyz/</a>
</div>
