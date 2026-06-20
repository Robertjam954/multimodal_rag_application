<!-- source: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstart -->

# Quickstart: Create a new agent (classic)

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
Quickstart: Create a new agent (classic)
Summarize this article for me
Note
This document refers to the Microsoft Foundry (classic) portal.
Agents (classic) are now deprecated and will be retired on March 31, 2027. Use the new agents in the generally available
Microsoft Foundry Agents Service
. Follow the
migration guide
to update your workloads.
Note
This quickstart is for the previous version of agents. See the
quickstart for Microsoft Foundry
to use the new version of the API.
Foundry Agent Service allows you to create AI agents tailored to your needs through custom instructions and augmented by advanced tools like code interpreter, and custom functions.
Prerequisites
An Azure subscription -
Create one for free
.
Ensure that the individual creating the account and project has the
Foundry Account Owner
role at the subscription scope, which will grant the necessary permissions for creating the project
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
Alternatively, having the
Contributor
or
Owner
role at the subscription level will allow the creation of the project
Once the project is created, ensure that the individual creating the agent within the project has the
Foundry User
role at the project level
Important
The Microsoft Foundry portal only supports basic agent setup at this time. If you want to perform a standard agent setup, see the
Environment setup
article to learn about more.
Create a Foundry account and project in Foundry portal
To create an account and project in Foundry, follow these steps:
Go to Foundry. If you are in a project, select Foundry at the top left of the page to go to the Home page.
Use the Agent getting started creation flow for the fastest experience. Click
Create an agent
.
Enter a name for the project. If you want to customize the default values, select
Advanced options
.
Select
Create
.
Wait for your resources to be provisioned.
An account and project (child resource of your account) will be created.
The gpt-4o model will automatically be deployed
A default agent will be created
Once complete, you will land directly in the agent playground and you can start creating agents. You can give your agent instructions on what to do and how to do it. For example:
"You are a helpful agent that can answer questions about geography."
Then you can start chatting with your agent.
Note
If you are getting permission error when trying to configure or create agents ensure you have the
Foundry User
on the project.
|
Reference documentation
|
Samples
|
Library source code
|
Package (NuGet)
|
Prerequisites
A set up agent environment
Assign the
Foundry User
RBAC role
to each team member who needs to create or edit agents using the SDK or Agent Playground
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
This role must be assigned at the project scope
Minimum required permissions:
agents/*/read
,
agents/*/action
,
agents/*/delete
Configure and run an agent
Create a .NET Console project.
```
dotnet new console

```
Install the .NET package to your project. For example if you're using the .NET CLI, run the following command.
```
dotnet add package Azure.AI.Agents.Persistent
dotnet add package Azure.Identity

```
Next, to authenticate your API requests and run the program, use the
az login
command to sign into your Azure subscription.
```
az login

```
Use the following code to create and run an agent. To run this code, you will need to get the endpoint for your project. This string is in the format:
https://<AIFoundryResourceName>.services.ai.azure.com/api/projects/<ProjectName>
Important
Starting in May 2025, the Azure AI Agent Service uses an endpoint for
Foundry projects
instead of the connection string that was previously used for hub-based projects. If you're using a hub-based project, you won't be able to use the current versions of the SDK and REST API. For more information, see
SDK usage with hub-based projects
.
You can find your endpoint in the
overview
for your project in the
Microsoft Foundry portal
, under
Libraries
>
Foundry
.
Set this endpoint in an environment variable named
ProjectEndpoint
.
You also need your model's deployment name. You can find it in
Models + Endpoints
in the left navigation menu.
Save the name of your model deployment name as an environment variable named
ModelDeploymentName
.
```
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using System.Diagnostics;

var projectEndpoint = System.Environment.GetEnvironmentVariable("ProjectEndpoint");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("ModelDeploymentName");



//Create a PersistentAgentsClient and PersistentAgent.
PersistentAgentsClient client = new(projectEndpoint, new DefaultAzureCredential());

//Give PersistentAgent a tool to execute code using CodeInterpreterToolDefinition.
PersistentAgent agent = client.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "My Test Agent",
    instructions: "You politely help with math questions. Use the code interpreter tool when asked to visualize numbers.",
    tools: [new CodeInterpreterToolDefinition()]
);

//Create a thread to establish a session between Agent and a User.
PersistentAgentThread thread = client.Threads.CreateThread();

//Ask a question of the Agent.
client.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "Hi, Agent! Draw a graph for a line with a slope of 4 and y-intercept of 9.");

//Have Agent begin processing user's question with some additional instructions associated with the ThreadRun.
ThreadRun run = client.Runs.CreateRun(
    thread.Id,
    agent.Id,
    additionalInstructions: "Please address the user as Jane Doe. The user has a premium account.");

//Poll for completion.
do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = client.Runs.GetRun(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress
    || run.Status == RunStatus.RequiresAction);

//Get the messages in the PersistentAgentThread. Includes Agent (Assistant Role) and User (User Role) messages.
Pageable<PersistentThreadMessage> messages = client.Messages.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending);

//Display each message and open the image generated using CodeInterpreterToolDefinition.
foreach (PersistentThreadMessage threadMessage in messages)
{
    foreach (MessageContent content in threadMessage.ContentItems)
    {
        switch (content)
        {
            case MessageTextContent textItem:
                Console.WriteLine($"[{threadMessage.Role}]: {textItem.Text}");
                break;
            case MessageImageFileContent imageFileContent:
                Console.WriteLine($"[{threadMessage.Role}]: Image content file ID = {imageFileContent.FileId}");
                BinaryData imageContent = client.Files.GetFileContent(imageFileContent.FileId);
                string tempFilePath = Path.Combine(AppContext.BaseDirectory, $"{Guid.NewGuid()}.png");
                File.WriteAllBytes(tempFilePath, imageContent.ToArray());
                client.Files.DeleteFile(imageFileContent.FileId);

                ProcessStartInfo psi = new()
                {
                    FileName = tempFilePath,
                    UseShellExecute = true
                };
                Process.Start(psi);
                break;
        }
    }
}

//If you want to delete your agent, uncomment the following lines:
//client.Threads.DeleteThread(threadId: thread.Id);
//client.Administration.DeleteAgent(agentId: agent.Id);

```
|
Reference documentation
|
Samples
|
Library source code
|
Package (PyPi)
|
Prerequisites
A set up agent environment
Assign the
Foundry User
RBAC role
to each team member who needs to create or edit agents using the SDK or Agent Playground
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
This role must be assigned at the project scope
Minimum required permissions:
agents/*/read
,
agents/*/action
,
agents/*/delete
Configure and run an agent
Run the following commands to install the python packages.
```
pip install azure-ai-projects
pip install azure-identity

```
Next, to authenticate your API requests and run the program, use the
az login
command to sign into your Azure subscription.
```
az login

```
Use the following code to create and run an agent. To run this code, you will need to get the endpoint for your project. This string is in the format:
https://<AIFoundryResourceName>.services.ai.azure.com/api/projects/<ProjectName>
Important
Starting in May 2025, the Azure AI Agent Service uses an endpoint for
Foundry projects
instead of the connection string that was previously used for hub-based projects. If you're using a hub-based project, you won't be able to use the current versions of the SDK and REST API. For more information, see
SDK usage with hub-based projects
.
You can find your endpoint in the
overview
for your project in the
Microsoft Foundry portal
, under
Libraries
>
Foundry
.
Set this endpoint as an environment variable named
PROJECT_ENDPOINT
.
You also need your model's deployment name. You can find it in
Models + Endpoints
in the left navigation menu.
Save the name of your model deployment name as an environment variable named
MODEL_DEPLOYMENT_NAME
.
```
import os
from pathlib import Path
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool

# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=os.getenv("PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential(),  
    # Use Azure Default Credential for authentication
)

with project_client:

    code_interpreter = CodeInterpreterTool()

    agent = project_client.agents.create_agent(
        model=os.getenv("MODEL_DEPLOYMENT_NAME"),  # Model deployment name
        name="my-agent",  # Name of the agent
        instructions="""You politely help with math questions. 
        Use the Code Interpreter tool when asked to visualize numbers.""",  
        # Instructions for the agent
        tools=code_interpreter.definitions,  # Attach the tool
        tool_resources=code_interpreter.resources,  # Attach tool resources
    )
    print(f"Created agent, ID: {agent.id}")

    # Create a thread for communication
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    question = """Draw a graph for a line with a slope of 4 
    and y-intercept of 9 and provide the file to me?"""

    # Add a message to the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",  # Role of the message sender
        content=question,  # Message content
    )
    print(f"Created message, ID: {message['id']}")

    # Create and process an agent run
    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,
        additional_instructions="""Please address the user as Jane Doe.
        The user has a premium account.""",
    )

    print(f"Run finished with status: {run.status}")

    # Check if the run failed
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Fetch and log all messages
    messages = project_client.agents.messages.list(thread_id=thread.id)
    print(f"Messages: {messages}")

    for message in messages:
        print(f"Role: {message.role}, Content: {message.content}")
        for this_content in message.content:
            print(f"Content Type: {this_content.type}, Content Data: {this_content}")
            if this_content.text.annotations:
                for annotation in this_content.text.annotations:
                    print(f"Annotation Type: {annotation.type}, Text: {annotation.text}")
                    print(f"Start Index: {annotation.start_index}")
                    print(f"End Index: {annotation.end_index}")
                    print(f"File ID: {annotation.file_path.file_id}")
                    # Save every image file in the message
                    file_id = annotation.file_path.file_id
                    file_name = f"{file_id}_image_file.png"
                    project_client.agents.files.save(file_id=file_id, file_name=file_name)
                    print(f"Saved image file to: {Path.cwd() / file_name}")
    #Uncomment these lines to delete the agent when done
    #project_client.agents.delete_agent(agent.id)
    #print("Deleted agent")

```
|
Reference documentation
|
Samples
|
Library source code
|
Package (npm)
|
Prerequisites
A set up agent environment
Assign the
Foundry User
RBAC role
to each team member who needs to create or edit agents using the SDK or Agent Playground
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
This role must be assigned at the project scope
Minimum required permissions:
agents/*/read
,
agents/*/action
,
agents/*/delete
Node.js LTS
Configure and run an agent
Key objects in this code include:
AgentsClient
First, initialize a new TypeScript project by running:
```
npm init -y
npm pkg set type="module"

```
Run the following commands to install the npm packages required.
```
npm install @azure/ai-agents @azure/identity
npm install @types/node typescript --save-dev

```
Next, to authenticate your API requests and run the program, use the
az login
command to sign into your Azure subscription.
```
az login

```
Use the following code to answer the math question
I need to solve the equation '3x + 11 = 14'. Can you help me?
. To run this code, you'll need to get the endpoint for your project. This string is in the format:
https://<AIFoundryResourceName>.services.ai.azure.com/api/projects/<ProjectName>
You can find your endpoint in the
overview
for your project in the
Microsoft Foundry portal
, under
Libraries
>
Foundry
.
Set this endpoint as an environment variable named
PROJECT_ENDPOINT
in a
.env
file.
You also need your model's deployment name. You can find it in
Models + Endpoints
in the left navigation menu.
Save the name of your model deployment name as an environment variable named
MODEL_DEPLOYMENT_NAME
.
Important
This quickstart code uses environment variables for sensitive configuration. Never commit your
.env
file to version control by making sure
.env
is listed in your
.gitignore
file.
Remember: If you accidentally commit sensitive information, consider those credentials compromised and rotate them immediately.
Create a tsconfig.json file with the following content:
```
{
  "compilerOptions": {
    "module": "nodenext",
    "target": "esnext",
    "types": ["node"],
    "lib": ["esnext"],
    "sourceMap": true,
    "declaration": true,
    "declarationMap": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "strict": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "noUncheckedSideEffectImports": true,
    "moduleDetection": "force",
    "skipLibCheck": true,
  }
}

```
Next, create an
index.ts
file and paste in the following code:
```
import { AgentsClient } from "@azure/ai-agents";
import { DefaultAzureCredential } from "@azure/identity";

const projectEndpoint = process.env["PROJECT_ENDPOINT"] || "<project endpoint>";
const modelDeploymentName = process.env["MODEL_DEPLOYMENT_NAME"] || "gpt-4o";

export async function main(): Promise<void> {
  // Create an Azure AI Client
  const client = new AgentsClient(projectEndpoint, new DefaultAzureCredential());

  // Create an agent
  const agent = await client.createAgent(modelDeploymentName, {
    name: "my-agent",
    instructions: "You are a helpful agent specialized in math. When providing mathematical explanations, use plain text formatting with simple characters like +, -, *, / for operations. Do not use LaTeX formatting with backslashes or special notation. Make your explanations clear and easy to read in a terminal.",
  });
  console.log(`Created agent, agent ID : ${agent.id}`);

  // Create a thread
  const thread = await client.threads.create();
  console.log(`Created thread, thread ID : ${thread.id}`);

  // List all threads for the agent
  const threads = client.threads.list();
  console.log(`Threads for agent ${agent.id}:`);
  for await (const t of threads) {
    console.log(`Thread ID: ${t.id} created at: ${t.createdAt}`);
  }

  // Create a message
  const message = await client.messages.create(thread.id, "user", "I need to solve the equation `3x + 11 = 14`. Can you help me?");
  console.log(`Created message, message ID : ${message.id}`);

  // Create and poll a run
  console.log("Creating run...");
  const run = await client.runs.createAndPoll(thread.id, agent.id, {
    pollingOptions: {
      intervalInMs: 2000,
    },
    onResponse: (response): void => {
      const parsedBody =
        typeof response.parsedBody === "object" && response.parsedBody !== null
          ? response.parsedBody
          : null;
      const status = parsedBody && "status" in parsedBody ? parsedBody.status : "unknown";
      console.log(`Received response with status: ${status}`);
    },
  });
  console.log(`Run finished with status: ${run.status}`);

  const messagesIterator = client.messages.list(thread.id);
  console.log("\n\n========================================================");
  console.log("=================== CONVERSATION RESULTS ===================");
  console.log("========================================================\n");
  
  // Collect all messages first
  const messages = [];
  for await (const m of messagesIterator) {
    messages.push(m);
  }
  
  // Reverse the order of messages (or sort by timestamp if available)
  messages.reverse();
  
  // Display messages in the new order
  for (const m of messages) {
    if (m.role === "user") {
      console.log(`\n❓ USER QUESTION: ${
        Array.isArray(m.content) && m.content[0]?.type === "text" && 'text' in m.content[0]
          ? m.content[0].text.value
          : JSON.stringify(m.content)
      }`);
    } else if (m.role === "assistant") {
      console.log("\n🤖 ASSISTANT'S ANSWER:");
      console.log("--------------------------------------------------");
      
      // Extract and print the text content in a more readable format
      if (m.content && Array.isArray(m.content)) {
        for (const content of m.content) {
          if (content.type === "text" && 'text' in content) {
            console.log(content.text?.value);
          } else {
            console.log(content);
          }
        }
      } else {
        console.log(JSON.stringify(m.content, null, 2));
      }
      console.log("--------------------------------------------------\n");
    }
  }
  
  console.log("\n========================================================");
  console.log("====================== END OF RESULTS ======================");
  console.log("========================================================\n");

  // Clean up
  await client.threads.delete(thread.id);
  await client.deleteAgent(agent.id);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});

```
Run the code using
npx tsx -r dotenv/config index.ts
. This code answers the question
I need to solve the equation '3x + 11 = 14'. Can you help me?
. Responses aren't deterministic, your output will look similar to the below output:
```
Created agent, agent ID : asst_X4yDNWrdWKb8LN0SQ6xlzhWk
Created thread, thread ID : thread_TxqZcHL2BqkNWl9dFzBYMIU6
Threads for agent asst_X4yDNWrdWKb8LN0SQ6xlzhWk:
...
Created message, message ID : msg_R0zDsXdc2UbfsNXvS1zeS6hk
Creating run...
Received response with status: queued
Received response with status: in_progress
Received response with status: completed
Run finished with status: completed

========================================================
=================== CONVERSATION RESULTS ===================
========================================================

❓ USER QUESTION: I need to solve the equation `3x + 11 = 14`. Can you help me?

🤖 ASSISTANT'S ANSWER:
--------------------------------------------------
Certainly! Let's solve the equation step by step:

We have:
3x + 11 = 14

### Step 1: Eliminate the constant (+11) on the left-hand side.
Subtract 11 from both sides:
3x + 11 - 11 = 14 - 11
This simplifies to:
3x = 3

We have:
3x + 11 = 14

### Step 1: Eliminate the constant (+11) on the left-hand side.
Subtract 11 from both sides:
3x + 11 - 11 = 14 - 11
This simplifies to:
3x = 3

### Step 2: Solve for x.
Divide both sides by 3:
3x / 3 = 3 / 3
This simplifies to:
x = 1

### Final Answer:
x = 1
--------------------------------------------------

========================================================
====================== END OF RESULTS ======================
========================================================

```
Full
sample source code
available.
|
Reference documentation
|
Samples
|
Library source code
|
Package (Maven)
|
Prerequisites
A set up agent environment
Assign the
Foundry User
RBAC role
to each team member who needs to create or edit agents using the SDK or Agent Playground
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
This role must be assigned at the project scope
Minimum required permissions:
agents/*/read
,
agents/*/action
,
agents/*/delete
Configure and run an agent
First, create a New Java console project. You'll need the following dependencies to run the code:
```
<dependencies>
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-ai-agents-persistent</artifactId>
        <version>1.0.0-beta.2</version>
    </dependency>
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-identity</artifactId>
        <version>1.17.0-beta.1</version>
    </dependency>
</dependencies>

```
Next, to authenticate your API requests and run the program, use the
az login
command to sign into your Azure subscription.
```
az login

```
Use the following code to create and run an agent. To run this code, you'll need to get the endpoint for your project. This string is in the format:
https://<AIFoundryResourceName>.services.ai.azure.com/api/projects/<ProjectName>
Important
Starting in May 2025, the Azure AI Agent Service uses an endpoint for
Foundry projects
instead of the connection string that was previously used for hub-based projects. If you're using a hub-based project, you won't be able to use the current versions of the SDK and REST API. For more information, see
SDK usage with hub-based projects
.
You can find your endpoint in the
overview
for your project in the
Microsoft Foundry portal
, under
Libraries
>
Foundry
.
Set this endpoint in an environment variable named
PROJECT_ENDPOINT
.
You also need your model's deployment name. You can find it in
Models + Endpoints
in the left navigation menu.
Save the name of your model deployment name as an environment variable named
MODEL_DEPLOYMENT_NAME
.
Code example
```
package com.example.agents;

import com.azure.ai.agents.persistent.MessagesClient;
import com.azure.ai.agents.persistent.PersistentAgentsAdministrationClient;
import com.azure.ai.agents.persistent.PersistentAgentsClient;
import com.azure.ai.agents.persistent.PersistentAgentsClientBuilder;
import com.azure.ai.agents.persistent.RunsClient;
import com.azure.ai.agents.persistent.ThreadsClient;
import com.azure.ai.agents.persistent.models.CodeInterpreterToolDefinition;
import com.azure.ai.agents.persistent.models.CreateAgentOptions;
import com.azure.ai.agents.persistent.models.CreateRunOptions;
import com.azure.ai.agents.persistent.models.MessageImageFileContent;
import com.azure.ai.agents.persistent.models.MessageRole;
import com.azure.ai.agents.persistent.models.MessageTextContent;
import com.azure.ai.agents.persistent.models.PersistentAgent;
import com.azure.ai.agents.persistent.models.PersistentAgentThread;
import com.azure.ai.agents.persistent.models.RunStatus;
import com.azure.ai.agents.persistent.models.ThreadMessage;
import com.azure.ai.agents.persistent.models.ThreadRun;
import com.azure.ai.agents.persistent.models.MessageContent;
import com.azure.core.http.rest.PagedIterable;
import com.azure.identity.DefaultAzureCredentialBuilder;
import java.util.Arrays;

public class AgentSample {

    public static void main(String[] args) {
        // variables for authenticating requests to the agent service 
        String projectEndpoint = System.getenv("PROJECT_ENDPOINT");
        String modelName = System.getenv("MODEL_DEPLOYMENT_NAME");

        // initialize clients to manage various aspects of agent runtime
        PersistentAgentsClientBuilder clientBuilder = new PersistentAgentsClientBuilder()
            .endpoint(projectEndpoint)
            .credential(new DefaultAzureCredentialBuilder().build());
        PersistentAgentsClient agentsClient = clientBuilder.buildClient();
        PersistentAgentsAdministrationClient administrationClient = agentsClient.getPersistentAgentsAdministrationClient();
        ThreadsClient threadsClient = agentsClient.getThreadsClient();
        MessagesClient messagesClient = agentsClient.getMessagesClient();
        RunsClient runsClient = agentsClient.getRunsClient();
        
        
        String agentName = "my-agent"; // the name of the agent
        CreateAgentOptions createAgentOptions = new CreateAgentOptions(modelName)
            .setName(agentName)
            .setInstructions("You are a helpful agent") // system instructions
            .setTools(Arrays.asList(new CodeInterpreterToolDefinition()));
        PersistentAgent agent = administrationClient.createAgent(createAgentOptions);

        PersistentAgentThread thread = threadsClient.createThread();
        ThreadMessage createdMessage = messagesClient.createMessage(
            thread.getId(),
            MessageRole.USER,
            "I need to solve the equation `3x + 11 = 14`. Can you help me?"); // The message to the agent

        try {
            //run the agent
            CreateRunOptions createRunOptions = new CreateRunOptions(thread.getId(), agent.getId())
                .setAdditionalInstructions("");
            ThreadRun threadRun = runsClient.createRun(createRunOptions);
            // wait for the run to complete before printing the message
            waitForRunCompletion(thread.getId(), threadRun, runsClient);
            printRunMessages(messagesClient, thread.getId());
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        } finally {
            //cleanup - uncomment these lines if you want to delete the agent
            //threadsClient.deleteThread(thread.getId());
            //administrationClient.deleteAgent(agent.getId());
        }
    }

    // A helper function to print messages from the agent
    public static void printRunMessages(MessagesClient messagesClient, String threadId) {

        PagedIterable<ThreadMessage> runMessages = messagesClient.listMessages(threadId);
        for (ThreadMessage message : runMessages) {
            System.out.print(String.format("%1$s - %2$s : ", message.getCreatedAt(), message.getRole()));
            for (MessageContent contentItem : message.getContent()) {
                if (contentItem instanceof MessageTextContent) {
                    System.out.print((((MessageTextContent) contentItem).getText().getValue()));
                } else if (contentItem instanceof MessageImageFileContent) {
                    String imageFileId = (((MessageImageFileContent) contentItem).getImageFile().getFileId());
                    System.out.print("Image from ID: " + imageFileId);
                }
                System.out.println();
            }
        }
    }

    // a helper function to wait until a run has completed running
    public static void waitForRunCompletion(String threadId, ThreadRun threadRun, RunsClient runsClient)
        throws InterruptedException {

        do {
            Thread.sleep(500);
            threadRun = runsClient.getRun(threadId, threadRun.getId());
        }
        while (
            threadRun.getStatus() == RunStatus.QUEUED
                || threadRun.getStatus() == RunStatus.IN_PROGRESS
                || threadRun.getStatus() == RunStatus.REQUIRES_ACTION);

        if (threadRun.getStatus() == RunStatus.FAILED) {
            System.out.println(threadRun.getLastError().getMessage());
        }
    }
}

```
|
Reference documentation
|
Prerequisites
A set up agent environment
Assign the
Foundry User
RBAC role
to each team member who needs to create or edit agents using the SDK or Agent Playground
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
This role must be assigned at the project scope
Minimum required permissions:
agents/*/read
,
agents/*/action
,
agents/*/delete
Configure and run an agent
To authenticate your API requests, use the
az login
command to sign into your Azure subscription.
```
az login

```
Next, you'll need to fetch the Entra ID token to provide as authorization to the API calls. Fetch the token using the CLI command:
```
az account get-access-token --resource 'https://ai.azure.com' | jq -r .accessToken | tr -d '"'

```
Set the access token as an environment variable named
AGENT_TOKEN
.
To successfully make REST API calls to Foundry Agent Service, you will need to use your project's endpoint:
https://<your_ai_service_name>.services.ai.azure.com/api/projects/<your_project_name>
For example, your endpoint will look something like:
https://exampleaiservice.services.ai.azure.com/api/projects/project
Set this endpoint as an environment variable named
AZURE_AI_FOUNDRY_PROJECT_ENDPOINT
.
Note
For
api-version
parameter, the GA API version is
2025-05-01
and the latest preview API version is
2025-05-15-preview
. You must use the preview API for tools that are in preview.
Consider making your API version an environment variable, such as
$API_VERSION
.
Create an agent
Note
With Azure AI Agents Service the
model
parameter requires model deployment name. If your model deployment name is different than the underlying model name, then you would adjust your code to
"model": "{your-custom-model-deployment-name}"
.
```
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=2025-05-01 \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "You are a helpful agent.",
    "name": "my-agent",
    "tools": [{"type": "code_interpreter"}],
    "model": "gpt-4o-mini"
  }'

```
Create a thread
```
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=2025-05-01 \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''

```
Add a user question to the thread
```
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=2025-05-01 \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "I need to solve the equation `3x + 11 = 14`. Can you help me?"
    }'

```
Run the thread
```
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs?api-version=2025-05-01 \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'

```
Retrieve the status of the run
```
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=2025-05-01 \
  -H "Authorization: Bearer $AGENT_TOKEN"

```
Retrieve the agent response
```
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=2025-05-01 \
  -H "Authorization: Bearer $AGENT_TOKEN"

```
Next steps
Learn about the
tools
you can use to extend your agents' capabilities, such as accessing the web, provide grounding information, and more.
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