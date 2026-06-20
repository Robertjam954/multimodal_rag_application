<!-- source: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/sdk-overview -->

# Microsoft Foundry SDKs and Endpoints

Table of contents
Exit editor mode
Note
Access to this page requires authorization. You can try
signing in
or
changing directories
.
Access to this page requires authorization. You can try
changing directories
.
Microsoft Foundry SDKs and Endpoints
Summarize this article for me
A Foundry resource provides unified access to models, agents, and tools. This article explains which SDK and endpoint to use for your scenario.
The
Foundry SDK
is a thin-client SDK that exposes all of the Foundry project APIs through a single project endpoint. Higher-level SDKs build on it — for example, the Agent Framework
foundry
package depends on the Foundry SDK to access Foundry models, tools, and project configuration.
SDK
What it's for
Endpoint
Foundry SDK
Thin-client SDK over all Foundry project APIs. Access to Foundry Models and platform tools (file search, code interpreter, web search, memory, SharePoint, WorkIQ, Fabric IQ, MCP).
https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
Agent Framework
Hosted agents and multi-agent systems build using code. The
foundry
package depends on the Foundry SDK for project access. Run in your own process.
Responses API in the project endpoint, via
FoundryChatClient
.
OpenAI SDK
Full OpenAI API surface, including embeddings. Best latency and maximum OpenAI compatibility.
https://<resource-name>.openai.azure.com/openai/v1
Anthropic SDK
Anthropic Claude models deployed in Foundry.
https://<resource-name>.services.ai.azure.com/anthropic
Foundry Tools SDKs
Prebuilt solutions (Vision, Speech, Content Safety, and more).
Tool-specific endpoints.
Choose your SDK
:
Use
Foundry SDK
when building apps with agents, evaluations, or Foundry-specific features
Use
Agent Framework
when building hosted agents or multi-agent systems in code using the Responses API
Use
OpenAI SDK
when maximum OpenAI compatibility or lowest latency is required, when generating embeddings, or when using Foundry direct models via Chat Completions
Use
Anthropic SDK
when working with Anthropic Claude models deployed in Foundry
Use
Foundry Tools SDKs
when working with specific AI services (Vision, Speech, Language, etc.)
Note
Resource types:
A Foundry resource provides all endpoints previously listed. An Azure OpenAI resource provides only the
/openai/v1
endpoint.
Authentication:
Samples here use Microsoft Entra ID (
DefaultAzureCredential
). API keys work on
/openai/v1
. Pass the key as
api_key
instead of a token provider.
Prerequisites
An Azure account with an active subscription. If you don't have one, create a
free Azure account, which includes a free trial subscription
.
Have one of the following Azure RBAC roles to create and manage Foundry resources:
Foundry User
(least-privilege role for development)
Important
The Foundry RBAC roles were recently renamed.
Foundry User
,
Foundry Owner
,
Foundry Account Owner
, and
Foundry Project Manager
were previously named Azure AI User, Azure AI Owner, Azure AI Account Owner, and Azure AI Project Manager. You might still see the previous names in some places while the rename rolls out. The role IDs and core permissions are unchanged by the rename.
Foundry Project Manager
(for managing Foundry projects)
Contributor
or
Owner
(for subscription-level permissions)
For details on each role's permissions, see
Role-based access control for Microsoft Foundry
.
Install the required language runtimes, global tools, and VS Code extensions as described in
Prepare your development environment
.
Important
Before starting, make sure your development environment is ready.
This article focuses on
scenario-specific steps
like SDK installation, authentication, and running sample code.
Verify prerequisites
Before proceeding, confirm:
Azure subscription is active:
az account show
You have the required RBAC role: Check Azure portal → Foundry resource → Access control (IAM)
Language runtime installed:
Python:
python --version
(≥3.8)
Language runtime installed:
Node.js:
node --version
(≥18)
Language runtime installed:
.NET:
dotnet --version
(≥6.0)
Language runtime installed:
Java:
java --version
(≥11)
Foundry SDK
The Foundry SDK is a thin-client SDK that gives you access to all of the Foundry project APIs through a single project endpoint:
```
https://<resource-name>.services.ai.azure.com/api/projects/<project-name>

```
It's the foundation other Foundry-aware SDKs build on. For example, the Agent Framework
foundry
package takes a dependency on the Foundry SDK and uses it to access Foundry functionality — you don't need to wire up the project endpoint or OpenAI-compatible client yourself when you use
FoundryChatClient
.
Note
If your organization uses a custom subdomain, replace
<resource-name>
with
<your-custom-subdomain>
in the endpoint URL.
This approach simplifies application configuration. Instead of managing multiple endpoints, you configure one.
Install the SDK
SDK Version
Portal Version
Status
Python Package
2.x
Foundry (new)
Stable
azure-ai-projects>=2.0.0
1.x
Foundry (classic)
Stable
azure-ai-projects==1.0.0
The
Azure AI Projects client library for Python
is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.
Run this command to install the packages for Foundry projects.
```
pip install "azure-ai-projects>=2.0.0"

```
SDK Version
Portal Version
Status
Java Package
2.0.0
Foundry (new)
Stable
azure-ai-projects
azure-ai-agents
SDK Version
Portal Version
Status
JavaScript Package
2.0.1
Foundry (new)
Stable
@azure/ai-projects
1.0.1
Foundry classic
Stable
@azure/ai-projects
SDK Version
Portal Version
Status
.NET Package
2.0.0 (GA)
Foundry (new)
Stable
Azure.AI.Projects
Azure.AI.Projects.Agents
Azure.AI.Extensions.OpenAI
1.1.0 (GA)
Foundry classic
Stable
Azure.AI.Projects
Important
Don't install
Azure.AI.Projects.OpenAI
(preview) alongside
Azure.AI.Extensions.OpenAI
(GA). Both packages define the same types in different namespaces, which causes ambiguous reference errors. Use only
Azure.AI.Extensions.OpenAI
for agent scenarios.
The
Azure AI Projects client library for Java
is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.
Add these packages to your installation for Foundry projects.
```
package com.azure.ai.agents;

import com.azure.core.util.Configuration;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

```
The
Azure AI Projects client library for JavaScript
is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.
Run this command to install the JavaScript packages for Foundry projects.
```
npm install @azure/ai-projects @azure/identity dotenv

```
The
Azure AI Projects client library for .NET
is a unified library that enables you to use multiple client libraries together by connecting to a single project endpoint.
Run these commands to add the required packages to your .NET project.
```
dotnet add package Azure.AI.Projects
dotnet add package Azure.AI.Projects.Agents
dotnet add package Azure.AI.Extensions.OpenAI
dotnet add package Azure.Identity

```
Using the Foundry SDK
The SDK exposes two client types because Foundry and OpenAI have different API shapes:
Project client
– Use for Foundry-native operations where OpenAI has no equivalent. Examples: listing connections, retrieving project properties, enabling tracing.
OpenAI-compatible client
– Use for Foundry functionality that builds on OpenAI concepts. The Responses API, agents, evaluations, and fine-tuning all use OpenAI-style request/response patterns. This client targets the Responses API in your project endpoint, which gives you access to Foundry Models from the catalog (including non-Azure-OpenAI direct models) plus platform tools — standard OpenAI tools like file search, code interpreter, and web search, alongside Foundry-exclusive tools like memory, SharePoint, WorkIQ, Fabric IQ, and MCP servers. The project endpoint serves this traffic on the
/openai
route.
Most apps use both clients. Use the project client for setup and configuration, then use the OpenAI-compatible client for running agents, evaluations, and calling models (including Foundry direct models).
Create a project client:
```
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project_client = AIProjectClient(
  endpoint="https://<resource-name>.services.ai.azure.com/api/projects/<project-name>",
  credential=DefaultAzureCredential())

```
Create an OpenAI-compatible client from your project:
```
with project_client.get_openai_client() as openai_client:
    response = openai_client.responses.create(
        model="gpt-5.2",
        input="What is the size of France in square miles?",
    )
    print(f"Response output: {response.output_text}")

```
Expected output
:
```
Response output: France has an area of approximately 213,011 square miles (551,695 square kilometers).

```
Create a project client:
```
import com.azure.ai.projects.ProjectsClient;
import com.azure.ai.projects.ProjectsClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;

String endpoint = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";

ProjectsClient projectClient = new ProjectsClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(endpoint)
    .buildClient();
```**Create and use an OpenAI-compatible client from your project:**
```java
OpenAIClient openAIClient = projectClient.getOpenAIClient();

```
Create a project client:
```
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import "dotenv/config";

const projectEndpoint = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";
const deploymentName = "gpt-5.2";
const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());

```
Create an OpenAI-compatible client from your project:
```
const openAIClient = await project.getOpenAIClient();
const response = await openAIClient.responses.create({
    model: deploymentName,
    input: "What is the size of France in square miles?",
});
console.log(`Response output: ${response.output_text}`);

```
Create a project client:
```
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;

string endpoint = "https://<resource-name>.services.ai.azure.com/api/projects/<project-name>";

AIProjectClient projectClient = new(
    endpoint: new Uri(endpoint), 
    tokenProvider: new DefaultAzureCredential());

```
Create an OpenAI-compatible client from your project:
```
var responseClient = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForModel("gpt-5.2");
var response = responseClient.CreateResponse("What is the speed of light?");
Console.WriteLine(response.GetOutputText());

```
What you can do with the Foundry SDK
Access Foundry Models
, including Azure OpenAI
Use the Foundry Agent Service
Run batch evaluations
Enable app tracing
Fine-tune a model
Get endpoints and keys for Foundry Tools, local orchestration, and more
Troubleshooting
Authentication errors
If you see
DefaultAzureCredential failed to retrieve a token
:
Verify Azure CLI is authenticated
:
```
az account show
az login  # if not logged in

```
Check RBAC role assignment
:
Confirm you have at least the Foundry User role on the Foundry project
Important
The Foundry RBAC roles were recently renamed.
Foundry User
,
Foundry Owner
,
Foundry Account Owner
, and
Foundry Project Manager
were previously named Azure AI User, Azure AI Owner, Azure AI Account Owner, and Azure AI Project Manager. You might still see the previous names in some places while the rename rolls out. The role IDs and core permissions are unchanged by the rename.
See
Assign Azure roles
For managed identity in production
:
Ensure the managed identity has the appropriate role assigned
See
Configure managed identities
Endpoint configuration errors
If you see
Connection refused
or
404 Not Found
:
Verify resource and project names
match your actual deployment
Check endpoint URL format
: Should be
https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
For custom subdomains
: Replace
<resource-name>
with your custom subdomain
SDK version mismatches
If code samples fail with
AttributeError
or
ModuleNotFoundError
:
Check SDK version
:
```
pip show azure-ai-projects  # Python
npm list @azure/ai-projects  # JavaScript
dotnet list package  # .NET

```
Reinstall with correct version flags
: See installation commands in each language section above
OpenAI SDK
Use the OpenAI SDK when you want the full OpenAI API surface, the best latency, and maximum compatibility with existing OpenAI clients. This endpoint exposes the Responses API on Azure OpenAI directly and provides access to Azure OpenAI models and Foundry direct models, including embeddings, chat completions, and image generation. It doesn't provide access to Foundry-specific features like agents, evaluations, or Foundry-exclusive platform tools — for those, use the Responses API in your project endpoint through the
Foundry SDK
.
Tip
Use the OpenAI SDK endpoint for
generating embeddings
. The project endpoint used by the Foundry SDK doesn't currently route embedding requests.
The following snippet shows how to use the Azure OpenAI
/openai/v1
endpoint directly.
```
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

client = OpenAI(  
  base_url = "https://<resource-name>.openai.azure.com/openai/v1/",  
  api_key=token_provider,
)

response = client.responses.create(
    model="model_deployment_name",
    input= "What is the size of France in square miles?" 
)

print(response.model_dump_json(indent=2)) 

```
Expected output
:
```
{
  "id": "resp_abc123",
  "object": "response",
  "created": 1234567890,
  "model": "gpt-5.2",
  "output_text": "France has an area of approximately 213,011 square miles (551,695 square kilometers)."
}

```
For more information, see
Azure OpenAI supported programming languages
The following snippet shows how to use the Azure OpenAI
/openai/v1
endpoint directly.
```
import com.azure.identity.AuthenticationUtil;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;

import java.util.function.Supplier;

DefaultAzureCredential tokenCredential = new DefaultAzureCredentialBuilder().build();
String endpoint = "https://<resource-name>.openai.azure.com/openai/v1";
String deploymentName = "gpt-5.2";
Supplier<String> bearerTokenSupplier = AuthenticationUtil.getBearerTokenSupplier(
        tokenCredential, "https://ai.azure.com/.default");
OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
        .baseUrl(endpoint)
        .credential(BearerTokenCredential.create(bearerTokenSupplier))
        .build();

ResponseCreateParams responseCreateParams = ResponseCreateParams.builder()
        .input("What is the speed of light?")
        .model(deploymentName) 
        .build();

Response response = openAIClient.responses().create(responseCreateParams);

System.out.println("Response output: " + response.getOutputText());

```
For more information on using the OpenAI SDK, see
Azure OpenAI supported programming languages
```
const endpoint = "https://<resource-name>.openai.azure.com/openai/v1";
const scope = "https://ai.azure.com/.default";
const azureADTokenProvider = getBearerTokenProvider(new DefaultAzureCredential(), scope);
const client = new OpenAI({ baseURL: endpoint, apiKey: azureADTokenProvider });
const response = await client.responses.create({
        model: deploymentName,
        input: "What is the size of France in square miles?",
    });
console.log(`Response output: ${response.output_text}`);

```
For more information on using the OpenAI SDK, see
Azure OpenAI supported programming languages
Install the OpenAI package:
Run this command to add the OpenAI client library to your .NET project.
```
dotnet add package OpenAI
```When it succeeds, the .NET CLI confirms that it installed the `OpenAI` package.

This snippet configures `DefaultAzureCredential`, builds `OpenAIClientOptions`, and creates a `ResponsesClient` for the Azure OpenAI v1 endpoint.
```csharp
using Azure.Identity;
using OpenAI;
using OpenAI.Responses;
using System.ClientModel.Primitives;

#pragma warning disable OPENAI001

const string directModelEndpoint  = "https://<resource-name>.openai.azure.com/openai/v1/";
const string deploymentName = "gpt-5.2";    

BearerTokenPolicy tokenPolicy = new(
     new DefaultAzureCredential(),
     "https://ai.azure.com/.default");

OpenAIClient openAIClient = new(
     authenticationPolicy: tokenPolicy,
     options: new OpenAIClientOptions()
     {
         Endpoint = new($"{directModelEndpoint}"),
     });
ResponsesClient client = openAIClient.GetResponsesClient();

CreateResponseOptions options = new()
 {
     Model = deploymentName,
     InputItems = { ResponseItem.CreateUserMessageItem("What is the size of France in square miles?") },
     Temperature = (float)0.7,
 };

var modelDirectResponse = client.CreateResponse(options);

Console.WriteLine($"[ASSISTANT]: {modelDirectResponse.Value.GetOutputText()}");
#pragma warning restore OPENAI001

```
For more information on using the OpenAI SDK, see
Azure OpenAI supported programming languages
Anthropic SDK
Use the Anthropic SDK to work with Anthropic Claude models deployed in Foundry. Claude models use a separate
/anthropic
endpoint and the Anthropic Messages API, not the OpenAI-compatible endpoint.
The Anthropic endpoint appends
/anthropic
to your resource URL:
```
https://<resource-name>.services.ai.azure.com/anthropic

```
The Messages API is available at:
```
https://<resource-name>.services.ai.azure.com/anthropic/v1/messages

```
```
from anthropic import AnthropicFoundry
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

client = AnthropicFoundry(
    azure_ad_token_provider=token_provider,
    base_url="https://<resource-name>.services.ai.azure.com/anthropic",
)

message = client.messages.create(
    model="claude-sonnet-4-6",  # Replace with your deployment name
    messages=[
        {"role": "user", "content": "What are 3 things to visit in Seattle?"}
    ],
    max_tokens=1048,
)

print(message.content)

```
The Anthropic SDK doesn't provide a native C# client. Use the REST API with
HttpClient
to call Claude models.
```
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using Azure.Identity;

string endpoint = "https://<resource-name>.services.ai.azure.com/anthropic/v1/messages";
string deploymentName = "claude-sonnet-4-6"; // Replace with your deployment name

var credential = new DefaultAzureCredential();
var token = await credential.GetTokenAsync(
    new Azure.Core.TokenRequestContext(["https://ai.azure.com/.default"]));

using var httpClient = new HttpClient();
httpClient.DefaultRequestHeaders.Authorization =
    new AuthenticationHeaderValue("Bearer", token.Token);
httpClient.DefaultRequestHeaders.Add("anthropic-version", "2023-06-01");

var requestBody = new
{
    model = deploymentName,
    messages = new[] { new { role = "user", content = "What are 3 things to visit in Seattle?" } },
    max_tokens = 1048
};

var response = await httpClient.PostAsync(
    endpoint,
    new StringContent(JsonSerializer.Serialize(requestBody), Encoding.UTF8, "application/json"));

string result = await response.Content.ReadAsStringAsync();
Console.WriteLine(result);

```
```
import AnthropicFoundry from '@anthropic-ai/foundry-sdk';
import { getBearerTokenProvider, DefaultAzureCredential } from "@azure/identity";

const tokenProvider = getBearerTokenProvider(
    new DefaultAzureCredential(),
    'https://ai.azure.com/.default');

const client = new AnthropicFoundry({
    azureADTokenProvider: tokenProvider,
    baseURL: "https://<resource-name>.services.ai.azure.com/anthropic",
    apiVersion: "2023-06-01"
});

const message = await client.messages.create({
    model: "claude-sonnet-4-6", // Replace with your deployment name
    messages: [{ role: "user", content: "What are 3 things to visit in Seattle?" }],
    max_tokens: 1048,
});

console.log(message);

```
The Anthropic SDK doesn't provide a native Java client. Use the REST API with
HttpClient
to call Claude models.
```
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.core.credential.TokenRequestContext;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

String endpoint = "https://<resource-name>.services.ai.azure.com/anthropic/v1/messages";
String deploymentName = "claude-sonnet-4-6"; // Replace with your deployment name

var credential = new DefaultAzureCredentialBuilder().build();
var token = credential.getToken(
    new TokenRequestContext().addScopes("https://ai.azure.com/.default")).block();

String requestBody = """
    {
        "model": "%s",
        "messages": [{"role": "user", "content": "What are 3 things to visit in Seattle?"}],
        "max_tokens": 1048
    }
    """.formatted(deploymentName);

HttpClient httpClient = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(endpoint))
    .header("Authorization", "Bearer " + token.getToken())
    .header("Content-Type", "application/json")
    .header("anthropic-version", "2023-06-01")
    .POST(HttpRequest.BodyPublishers.ofString(requestBody))
    .build();

HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
System.out.println(response.body());

```
For more information, see
Use Anthropic Claude models in Microsoft Foundry
.
Agent Framework
Microsoft Agent Framework
is an open-source SDK (Python and .NET) for building agents and multi-agent systems in code. It's the recommended path for
Hosted agents (preview)
on Microsoft Foundry.
Run your code as a Hosted agent
The main story for code-based agents in Foundry is
Hosted agents (preview)
. Write your agent with Agent Framework, package it as a container image or zip of your source code, and let Foundry run it with a managed endpoint, automatic scaling on isolated Micro VMs, a dedicated Microsoft Entra agent identity, session-level state, and end-to-end observability.
Hosted agents are the recommended path when you want a Foundry-managed, network-addressable endpoint that other apps or agents can call. See
Deploy your first Hosted agent
.
Build agents in code outside Foundry with the Responses API
If you're hosting your agent outside of Foundry — in your own process or infrastructure — you can also use Agent Framework to call the
Responses API in your project endpoint
directly. Agent Framework connects through the
FoundryChatClient
provider, which targets:
```
{project_endpoint}/openai/v1/responses

```
Going through the project endpoint — instead of a resource-level OpenAI endpoint — gives your agent:
Foundry models from the catalog (Azure OpenAI and Foundry direct models) through one API.
Platform tools beyond the OpenAI tool set, including file search, code interpreter, memory, web search, MCP servers, SharePoint, WorkIQ, and Fabric IQ.
Project-scoped data, On-Behalf-Of (OBO) tool authentication, and the project's tracing, content filters, and identity configuration.
This pattern is additive to Hosted agents, not an alternative — the same Agent Framework code can call the Responses API from your own process today and be packaged as a Hosted agent later when you want a Foundry-managed endpoint. See
Quickstart: Build agents using the Responses API
.
For a full comparison of agent types and hosting choices, see
What is Microsoft Foundry Agent Service?
.
Foundry Tools SDKs
Foundry Tools (formerly Azure AI Services) are prebuilt point solutions with dedicated SDKs. Use the following endpoints to work with Foundry Tools.
Which endpoint should you use?
Choose an endpoint based on your needs:
Use the Azure AI Services endpoint to access Computer Vision, Content Safety, Document Intelligence, Language, Translation, and Token Foundry Tools.
Foundry Tools endpoint:
https://<your-resource-name>.cognitiveservices.azure.com/
Note
Endpoints use either your resource name or a custom subdomain. If your organization set up a custom subdomain, replace
your-resource-name
with
your-custom-subdomain
in all endpoint examples.
If your workloads use retiring Azure AI Language features—for example, sentiment analysis, key phrase extraction, summarization, entity linking, CLU, or CQA—plan to migrate to Microsoft Foundry alternatives. For new development, consider using the Foundry SDK or the OpenAI-compatible endpoint as described earlier in this article. See
Migrate from Language Studio to Microsoft Foundry
.
For Speech and Translation Foundry Tools, use the endpoints in the following tables. Replace placeholders with your resource information.
Speech Endpoints
Foundry Tool
Endpoint
Speech to Text (Standard)
https://<YOUR-RESOURCE-REGION>.stt.speech.microsoft.com
Text to Speech (Neural)
https://<YOUR-RESOURCE-REGION>.tts.speech.microsoft.com
Custom Voice
https://<YOUR-RESOURCE-NAME>.cognitiveservices.azure.com/
Translation Endpoints
Foundry Tool
Endpoint
Text Translation
https://api.cognitive.microsofttranslator.com/
Document Translation
https://<YOUR-RESOURCE-NAME>.cognitiveservices.azure.com/
Language Endpoints
Foundry Tool
Endpoint
Text analysis
https://<YOUR-RESOURCE-NAME>.cognitiveservices.azure.com
Important
On March 20, 2027, Azure Language Studio will retire and migrate to Microsoft Foundry; all capabilities and future enhancements will be available in Microsoft Foundry.
On March 31, 2029, the following Azure Language capabilities will retire (end of support). Before that date, users should migrate existing workloads and onboard new projects to
Microsoft Foundry models
for enhanced natural language understanding and simplified application integration:
Key Phrase Extraction
Sentiment Analysis and Opinion Mining
Custom Text Classification
Conversational Language Understanding (CLU)
Custom Question Answering (CQA)
Orchestration Workflow
Summarization (extractive and abstractive, for documents and conversations)
Entity Linking
Core features with continued support: Language Detection, PII Detection, Text Analytics for Health, Prebuilt NER, and Custom NER.
For migration options, see
Migrate from Language Studio to Microsoft Foundry
.
C# supported Foundry Tools
Foundry Tool
Description
Quickstarts and reference documentation
Speech
Add speech to text, text to speech, translation, and speaker recognition capabilities to applications.
•
Speech to text quickstart
•
Text to speech quickstart
•
Speech translation quickstart
•
Speech SDK for .NET
•
Speech NuGet package (Speech CLI)
Language
Build applications with natural language understanding capabilities. Supported features: Language Detection, PII Detection, Text Analytics for Health, Prebuilt NER, and Custom NER.
Retiring March 31, 2029
: Sentiment Analysis and Opinion Mining, Key Phrase Extraction, Summarization, Entity Linking, CQA, and CLU.
•
Custom question answering (CQA) quickstart
(retiring March 31, 2029)
•
Entity linking quickstart
(retiring March 31, 2029)
•
Language detection quickstart
•
Key Phrase extraction quickstart
(retiring March 31, 2029)
•
Detecting named entities (NER) quickstart
•
Detect Personally Identifiable Information (PII) quickstart
•
Sentiment analysis and opinion mining quickstart
(retiring March 31, 2029)
•
Using text, document and conversation summarization quickstart
(retiring March 31, 2029)
•
Using Text Analytics for health quickstart
•
Language SDK for .NET (text analysis)
•
Language NuGet package (text analysis)
•
Language SDK for .NET (Question Answering)
•
Language NuGet package (question answering)
•
Migrate from Language Studio to Microsoft Foundry
for guidance on migrating workloads with retiring features
Translator
Use AI-powered translation technology to translate more than 100 in-use, at-risk, and endangered languages and dialects.
•
Translator SDK for .NET (text)
•
Translator NuGet package (text)
•
Translator SDK for .NET (batch)
•
Translator NuGet package (batch)
Azure AI Search
Bring AI-powered cloud search to your mobile and web apps.
•
Use agentic retrieval quickstart
•
Vector search quickstart
•
Classic generative search (RAG) using grounding data quickstart
•
Full-text search quickstart
•
Semantic ranking quickstart
•
Chat with Azure OpenAI models using your own data quickstart
•
Azure AI Search SDK for .NET
•
Azure AI Search NuGet package
Content Safety
Detect harmful content in applications and services.
•
Analyze text content quickstart
•
Use a text blocklist quickstart
•
Analyze image content quickstart
•
Content Safety SDK for .NET
•
Content Safety NuGet package
Document Intelligence
Turn documents into intelligent data-driven solutions.
•
Document Intelligence quickstart
•
Document Intelligence SDK for .NET
•
Document Intelligence NuGet package
Vision
Analyze content in digital images and rich media assets.
•
Azure Vision in Foundry Tools v3.2 GA Read quickstart
•
Image Analysis quickstart
•
Use the Face service quickstart
•
Vision SDK for .NET
•
Vision NuGet package
Java supported Foundry Tools
Foundry Tool
Description
Quickstarts and reference documentation
Speech
Add speech to text, text to speech, translation, and speaker recognition capabilities to applications.
•
Speech to text quickstart
•
Text to speech quickstart
•
Speech translation quickstart
•
Speech SDK for Java
•
Speech Maven package
Language
Build applications with natural language understanding capabilities. Supported features: Language Detection, PII Detection, Text Analytics for Health, Prebuilt NER, and Custom NER.
Retiring March 31, 2029
: Sentiment Analysis and Opinion Mining, Key Phrase Extraction, Summarization, Entity Linking, CQA, and CLU.
•
Entity linking quickstart
(retiring March 31, 2029)
•
Language detection quickstart
•
Key Phrase extraction quickstart
(retiring March 31, 2029)
•
Detecting named entities (NER) quickstart
•
Detect Personally Identifiable Information (PII) quickstart
•
Sentiment analysis and opinion mining quickstart
(retiring March 31, 2029)
•
Using text, document and conversation summarization quickstart
(retiring March 31, 2029)
•
Using Text Analytics for health quickstart
•
Language SDK for Java (text analysis)
•
Language Maven package
•
Migrate from Language Studio to Microsoft Foundry
for guidance on migrating workloads with retiring features
Translator
Use AI-powered translation technology to translate more than 100 in-use, at-risk, and endangered languages and dialects.
•
Translator SDK for Java (text)
•
Translator Maven package (text)
Azure AI Search
Bring AI-powered cloud search to your mobile and web apps.
•
Use agentic retrieval quickstart
•
Vector search quickstart
•
Classic generative search (RAG) using grounding data quickstart
•
Full-text search quickstart
•
Semantic ranking quickstart
•
Chat with Azure OpenAI models using your own data quickstart
•
Azure AI Search SDK for Java
•
Azure AI Search Maven package
Content Safety
Detect harmful content in applications and services.
•
Analyze text content quickstart
•
Use a text blocklist quickstart
•
Analyze image content quickstart
•
Content Safety SDK for Java
•
Content Safety Maven package
Document Intelligence
Turn documents into intelligent data-driven solutions.
•
Document Intelligence quickstart
•
Document Intelligence SDK for Java
•
Document Intelligence Maven package
Vision
Analyze content in digital images and rich media assets.
•
Image Analysis quickstart
•
Use the Face service quickstart
•
Vision SDK for Java
•
Vision Maven package
JavaScript supported Foundry Tools
Foundry Tool
Description
Quickstarts and reference documentation
Speech
Add speech to text, text to speech, translation, and speaker recognition capabilities to applications.
•
Speech to text quickstart
•
Text to speech quickstart
•
Speech translation quickstart
•
Speech SDK for JavaScript
•
Speech npm package
Language
Build applications with natural language understanding capabilities. Supported features: Language Detection, PII Detection, Text Analytics for Health, Prebuilt NER, and Custom NER.
Retiring March 31, 2029
: Sentiment Analysis and Opinion Mining, Key Phrase Extraction, Summarization, Entity Linking, CQA, and CLU.
•
Entity linking quickstart
(retiring March 31, 2029)
•
Language detection quickstart
•
Key Phrase extraction quickstart
(retiring March 31, 2029)
•
Detecting named entities (NER) quickstart
•
Detect Personally Identifiable Information (PII) quickstart
•
Sentiment analysis and opinion mining quickstart
(retiring March 31, 2029)
•
Using text, document and conversation summarization quickstart
(retiring March 31, 2029)
•
Using Text Analytics for health quickstart
•
Language SDK for JavaScript (text analysis)
•
Language npm package
•
Migrate from Language Studio to Microsoft Foundry
for guidance on migrating workloads with retiring features
Translator
Use AI-powered translation technology to translate more than 100 in-use, at-risk, and endangered languages and dialects.
•
Translator SDK for JavaScript (text)
•
Translator npm package (text)
Azure AI Search
Bring AI-powered cloud search to your mobile and web apps.
•
Use agentic retrieval quickstart
•
Vector search quickstart
•
Classic generative search (RAG) using grounding data quickstart
•
Full-text search quickstart
•
Semantic ranking quickstart
•
Chat with Azure OpenAI models using your own data quickstart
•
Azure AI Search SDK for JavaScript
•
Azure AI Search npm package
Content Safety
Detect harmful content in applications and services.
•
Analyze text content quickstart
•
Use a text blocklist quickstart
•
Analyze image content quickstart
•
Content Safety npm package
Document Intelligence
Turn documents into intelligent data-driven solutions.
•
Document Intelligence quickstart
•
Document Intelligence SDK for JavaScript
•
Document Intelligence npm package
Vision
Analyze content in digital images and rich media assets.
•
Azure Vision in Foundry Tools v3.2 GA Read quickstart
•
Image Analysis quickstart
•
Use the Face service quickstart
•
Vision SDK for JavaScript
•
Vision npm package
Python supported Foundry Tools
Foundry Tool
Description
Quickstarts and reference documentation
Speech
Add speech to text, text to speech, translation, and speaker recognition capabilities to applications.
•
Speech to text quickstart
•
Text to speech quickstart
•
Speech translation quickstart
•
Speech SDK for Python
•
Speech PyPi package
Language
Build applications with natural language understanding capabilities. Supported features: Language Detection, PII Detection, Text Analytics for Health, Prebuilt NER, and Custom NER.
Retiring March 31, 2029
: Sentiment Analysis and Opinion Mining, Key Phrase Extraction, Summarization, Entity Linking, CQA, and CLU.
•
Custom question answering (CQA) quickstart
(retiring March 31, 2029)
•
Entity linking quickstart
(retiring March 31, 2029)
•
Language detection quickstart
•
Key Phrase extraction quickstart
(retiring March 31, 2029)
•
Detect named entities (NER) quickstart
•
Detect Personally Identifiable Information (PII) quickstart
•
Sentiment analysis and opinion mining quickstart
(retiring March 31, 2029)
•
Using text, document and conversation summarization quickstart
(retiring March 31, 2029)
•
Using Text Analytics for health quickstart
•
Language SDK for Python (text analysis)
•
Language PyPi package (text analysis)
•
Language SDK for Python (question answering)
•
Language PyPi package (question answering)
•
Language SDK for Python (language conversations)
(retiring March 31, 2029)
•
Language PyPi package (language conversations)
(retiring March 31, 2029)
•
Migrate from Language Studio to Microsoft Foundry
for guidance on migrating workloads with retiring features
Translator
Use AI-powered translation technology to translate more than 100 in-use, at-risk, and endangered languages and dialects.
•
Translator SDK for Python (text)
•
Translator PyPi package (text)
•
Translator SDK for Python (batch)
•
Translator PyPi package (batch)
Azure AI Search
Bring AI-powered cloud search to your mobile and web apps.
•
Connect to a search service quickstart
•
Use agentic retrieval quickstart
•
Vector search quickstart
•
Classic generative search (RAG) using grounding data quickstart
•
Full-text search quickstart
•
Semantic ranking quickstart
•
Chat with Azure OpenAI models using your own data quickstart
•
Azure AI Search SDK for Python
•
Azure AI Search PyPi package
Content Safety
Detect harmful content in applications and services.
•
Analyze text content quickstart
•
Use a text blocklist quickstart
•
Analyze image content quickstart
•
Content Safety SDK for Python
•
Content Safety PyPi package
Document Intelligence
Turn documents into intelligent data-driven solutions.
•
Document Intelligence quickstart
•
Document Intelligence SDK for Python
•
Document Intelligence PyPi package
Vision
Analyze content in digital images and rich media assets.
•
Azure Vision in Foundry Tools v3.2 GA Read quickstart
•
Image Analysis quickstart
•
Use the Face service quickstart
•
Vision SDK for Python
•
Vision PyPi package
Feedback
Was this page helpful?
Yes
No
No
Need help with this topic?
Want to try using Ask Learn to clarify or guide you through this topic?
Ask Learn
Ask Learn
Suggest a fix?
Additional resources