<!-- source: https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry -->

# What is Microsoft Foundry?

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
What is Microsoft Foundry?
Summarize this article for me
Microsoft Foundry
is a unified Azure platform-as-a-service offering for enterprise AI operations, model builders, and application development. This foundation combines production-grade infrastructure with friendly interfaces, enabling developers to focus on building applications rather than managing infrastructure.
Microsoft Foundry unifies agents, models, and tools under a single management grouping with built-in enterprise-readiness capabilities including tracing, monitoring, evaluations, and customizable enterprise setup configurations. The platform provides streamlined management through unified role-based access control (RBAC), networking, and policies under one Azure resource provider namespace.
Tip
Coming from Azure OpenAI?
Upgrade your Azure OpenAI resource to a Foundry resource
while preserving your endpoint, API keys, and existing state.
Using hub-based projects? Hub-based projects are accessible in the
Foundry (classic) portal
. New investments are focused on Foundry projects in the new portal.
Evolution of Foundry
Foundry consolidates several previous Azure AI services and tools into a unified platform. The following table maps previous concepts to their current equivalents. For detailed guidance on transitioning, see
Navigate from classic to the new experience
.
Dimension
Previous
Current
Brand
Azure AI Studio / Azure AI Foundry
Microsoft Foundry
Brand
Azure AI Services
Foundry Tools
Portal
Foundry (classic)
Foundry
Agent API
Assistants API (Agents v0.5/v1)
Responses API (Agents v2)
API versioning
Monthly
api-version
params
v1 stable routes (
/openai/v1/
)
Resource model
Hub + Azure OpenAI + Azure AI Services
Foundry resource (single, with projects)
SDKs & endpoints
Multiple packages (
azure-ai-inference
,
azure-ai-generative
,
azure-ai-ml
,
AzureOpenAI()
) against 5+ endpoints
Unified project client (
azure-ai-projects
2.x) +
OpenAI()
against one project endpoint.
Terminology
Threads, Messages, Runs, Assistants
Conversations, Items, Responses, Agent Versions
Your first API call
Get started now
—
Quickstart: Build with models and agents
|
Open Foundry portal
|
Get an Azure account
Send a prompt and get a response from a model in a few lines of code:
Python
C#
TypeScript
Java
REST API
```
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Create project and openai clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Run a responses API call
response = openai.responses.create(
    model="gpt-5-mini",
    input="What is the size of France in square miles?",
)
print(f"Response output: {response.output_text}")

```
```
using Azure.Identity;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using OpenAI.Responses;

#pragma warning disable OPENAI001

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var ProjectEndpoint = "your_project_endpoint";

// Create project client to call Foundry API
AIProjectClient projectClient = new(
    endpoint: new Uri(ProjectEndpoint),
    tokenProvider: new DefaultAzureCredential());

// Run a responses API call
ProjectResponsesClient responseClient = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForModel("gpt-5-mini"); 
ResponseResult response = await responseClient.CreateResponseAsync(
    "What is the size of France in square miles?");
Console.WriteLine(response.GetOutputText());

```
```
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";

async function main(): Promise<void> {
    // Create project and openai clients to call Foundry API
    const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
    const openai = project.getOpenAIClient();

    // Run a responses API call
    const response = await openai.responses.create({
        model: "gpt-5-mini",
        input: "What is the size of France in square miles?",
    });
    console.log(`Response output: ${response.output_text}`);
}

main().catch(console.error);

```
```
package com.azure.ai.agents;

import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

public class CreateResponse {
    public static void main(String[] args) {
        // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
        String ProjectEndpoint = "your_project_endpoint";

        // Create responses client to call Foundry API
        ResponsesClient responsesClient = new AgentsClientBuilder()
                .credential(new DefaultAzureCredentialBuilder().build())
                .endpoint(ProjectEndpoint)
                .buildResponsesClient();

        // Run a responses API call
        ResponseCreateParams responseRequest = new ResponseCreateParams.Builder()
                .input("What is the size of France in square miles?")
                .model("gpt-5-mini")
                .build();
        Response response = responsesClient.getResponseService().create(responseRequest);
        System.out.println(response.output());
    }
}

```
Replace
YOUR-FOUNDRY-RESOURCE-NAME
with your values:
```
curl -X POST https://YOUR-FOUNDRY-RESOURCE-NAME.services.ai.azure.com/api/projects/YOUR-PROJECT-NAME/openai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AZURE_AI_AUTH_TOKEN" \
-d '{
        "model": "gpt-5.1-mini",
        "input": "What is the size of France in square miles?"
}'

```
For the full walkthrough, see the
Microsoft Foundry quickstart
.
Available models
Foundry gives you access to over 1,900 models from Microsoft, OpenAI, Anthropic, Mistral, xAI, Meta, DeepSeek, Hugging Face, and more. The following table highlights popular model families to help you choose a starting point.
Model family
Best for
GPT-5
Most capable — complex reasoning, multi-step tasks, and multimodal scenarios
GPT-4.1
Best balance of capability and cost for production workloads
GPT-4.1 mini
Fastest — low-latency, high-throughput scenarios
Claude
Advanced reasoning, code generation, and multimodal tasks
Grok
Reasoning, coding, and data extraction
Mistral
Code generation, multilingual, and general-purpose chat
DeepSeek-R1
Open-weight reasoning at scale
Phi-4
Small language model — on-device or resource-constrained environments
Meta Llama
Open models — customization and fine-tuning
For help choosing between models, see the
GPT-5 vs GPT-4.1 model choice guide
. Browse the full catalog in the
Foundry Models overview
.
What's new
Foundry is evolving fast. Here are some of the latest additions:
Model routing with the Responses API
— Use a single API to route to any model automatically or by name.
A2A agent endpoints (preview)
— Expose agents as Agent2Agent endpoints so other agents can discover and call them.
Instant access (preview)
— Call any supported model by name without creating a deployment first.
Voice agents (preview)
— Build voice-enabled agents with hosted agents.
Routines (preview)
— Automate multi-step agent workflows with reusable routines.
Fabric IQ (preview)
— Connect agents to Microsoft Fabric data.
Work IQ (preview)
— Connect agents to Microsoft 365 content.
See
What's new in Microsoft Foundry
for the full list.
Choose your path
Foundry supports multiple developer surfaces. Use the following table to find the right starting point for your scenario.
I want to...
Start here
Call a model from code
Quickstart: Your first API call
Build an agent with tools and memory
Agent Service overview
Explore models in the browser
Foundry portal playgrounds
Deploy and manage models at scale
Foundry Models overview
Develop in VS Code
Foundry for VS Code
Set up governance and security
Foundry Control Plane
Who is Foundry for?
Microsoft Foundry serves three primary audiences:
Application developers
building AI-powered products with agents, models, and tools. Start with the
quickstart
.
ML engineers and data scientists
who
fine-tune models
,
run evaluations
, and
manage model deployments
.
IT administrators and platform engineers
who govern AI resources, enforce policies, and manage access across teams. See
security
and governance and
Foundry Control Plane
.
Key capabilities
Build agents
Multi-agent orchestration
— Build collaborative agent behavior and complex workflow execution using SDKs for C# and Python.
Tool catalog
— Connect over 1,400 tools through public and private catalogs.
Memory
— Retain and recall contextual information across interactions without requiring repeated input.
Foundry IQ knowledge integration
— Ground agent responses in enterprise or web content with citation-backed answers.
Publishing
— Publish agents to Microsoft 365, Teams, BizChat, or containerized deployments.
Operate and govern
Real-time observability
— Monitor performance and governance with built-in metrics and model tracking.
Centralized AI asset management
— Manage all agents, models, and tools from the
Operate
section, including agents registered from other clouds.
Enterprise controls
— Full authentication support for MCP and A2A, AI gateway integration, and Azure Policy integration.
Microsoft Foundry API and SDKs
The
Microsoft Foundry API
provides a consistent contract for building agentic applications across different model providers.
SDK client libraries
are available for:
Python
C#
JavaScript/TypeScript
Java
The
Microsoft Foundry for VS Code Extension
helps you explore models and develop agents directly in your development environment.
Foundry portal
The
Microsoft Foundry portal
is where you manage projects, deploy models, build agents, and monitor your AI assets. To use the current version, make sure the
New Foundry
toggle in the banner is set to on.
Tip
See
Find features in the Foundry portal
if you're used to the Foundry (classic) portal and not sure where to find things now.
For details on switching between projects or finding resources created in Foundry (classic), see
Find features in the Foundry portal
.
Pricing and billing
The platform is free to use and explore. Pricing occurs at the deployment level. Each product within Foundry (models, agents, tools) has its own billing model and price.
Using Foundry also incurs costs associated with the underlying services. To learn more, read
Plan and manage costs for Foundry Tools
.
Use the
Total Economic Impact calculator for Foundry
to estimate your return on investment.
Region availability
Foundry is available in most regions where Foundry Tools are available. For more information, see
region support for Microsoft Foundry
.
How to get access
You need an
Azure account
. Then sign in to
Microsoft Foundry
.
Related content
Quickstart: Get started with Microsoft Foundry
Quickstart: Set up Foundry resources
Instant access to models in Microsoft Foundry (preview)
Create a project
Get started with an AI template
Use the Microsoft Foundry Skill in coding agents
What's new in Microsoft Foundry documentation?
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