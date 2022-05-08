class Texts:
    """
    Texts used to generate documentation from OpenAPI Documentation.
    """

    contact: str
    content: str
    email: str
    content_type: str
    example: str
    links: str
    status_code: str
    name: str
    description: str
    parameter: str
    parameters: str
    parameter_location: str
    responses: str
    query: str
    type: str
    default: str
    nullable: str
    request_body: str
    no_parameters: str
    schema: str
    schema_of_the_request_body: str
    schema_of_the_response_body: str
    schemas: str
    about_schemas: str
    details: str
    external_docs: str
    required: str
    properties: str
    yes: str
    no: str
    other_accepted_types: str
    other_possible_types: str
    other_responses: str
    auto_generated_example_note: str
    license: str
    terms_of_service: str
    servers: str
    url: str
    common_responses: str
    common_responses_about: str
    security_schemes: str
    common_parameters_about: str
    scheme: str
    response_headers: str
    for_more_information: str
    tags: str

    def get_yes_no(self, value: bool) -> str:
        return self.yes if value else self.no


class EnglishTexts(Texts):
    contact = "Contact"
    license = "License"
    content = "Content"
    content_type = "Content type"
    email = "Email"
    example = "Example"
    status_code = "Status code"
    name = "Name"
    description = "Description"
    links = "Links"
    parameter = "Parameter"
    parameters = "Input parameters"
    parameter_location = "In"
    responses = "Responses"
    query = "Query"
    type = "Type"
    default = "Default"
    nullable = "Nullable"
    request_body = "Request body"
    no_parameters = "No parameters"
    schema = "Schema"
    schema_of_the_request_body = "Schema of the request body"
    schema_of_the_response_body = "Schema of the response body"
    schemas = "Schemas"
    about_schemas = "This section describes all types of objects handled by the API."
    details = "Details"
    required = "Required"
    properties = "Properties"
    yes = "Yes"
    no = "No"
    other_accepted_types = "Other accepted types"
    other_possible_types = "Other possible types"
    other_responses = "Other responses"
    auto_generated_example_note = (
        "This example has been generated automatically from the schema and it is "
        "not accurate. Refer to the schema for more information."
    )
    terms_of_service = "Terms of service"
    servers = "Servers"
    url = "URL"
    common_responses = "Common responses"
    common_responses_about = (
        "This section describes common responses that are reused across operations."
    )
    common_parameters = "Common parameters"
    common_parameters_about = (
        "This section describes common parameters that are reused across operations."
    )
    security_schemes = "Security schemes"
    scheme = "Scheme"
    response_headers = "Response headers"
    external_docs = "More documentation"
    for_more_information = "For more information"
    tags = "Tags"
