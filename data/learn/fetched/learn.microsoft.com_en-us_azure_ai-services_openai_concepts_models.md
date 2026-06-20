<!-- source: https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models -->

# Foundry Models sold by Azure

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
Foundry Models sold by Azure
Summarize this article for me
Microsoft Foundry Models in the model catalog comprise two main categories, namely
Foundry Models sold by Azure
and
Foundry Models from partners and community
.
This article lists a selection of Foundry Models sold by Azure, along with their capabilities,
deployment types
, and regions of availability, excluding deprecated and retired models. Foundry Models sold by Azure are also referred to as
Direct from Azure Models
or
Azure Direct Models
.
Models sold by Azure are also hosted by Azure and operated by Azure as part of the Foundry Models service. They include all Azure OpenAI models and specific,
selected models from top providers
. These models are billed through your Azure subscription, covered by Azure service-level agreements, and supported by Microsoft. To see a list of Foundry Models that are supported by the Foundry Agent Service, see
Models supported by Agent Service
, and for a list of Foundry Models from partners, see
Foundry Models from partners and community
.
Tip
Use the tabs at the top of this page to switch between
Azure OpenAI models
and
Other model collections
from providers like Cohere, DeepSeek, Meta, Mistral AI, and xAI.
Azure OpenAI in Microsoft Foundry models
Azure OpenAI is powered by a diverse set of models with different capabilities and price points. Model availability varies by region and cloud.
To see
region availability for Azure OpenAI in Microsoft Foundry models grouped by deployment category
, see
Region availability for Foundry Models sold by Azure
.
For
Azure Government model availability
, refer to
Azure OpenAI in Azure Government
.
Model highlights
Models
Description
GPT-chat-latest (preview)
NEW
gpt-chat-latest
Preview
GPT-5.5 series
NEW
gpt-5.5
GPT-5.4 series
gpt-5.4-mini
,
gpt-5.4-nano
,
gpt-5.4
,
gpt-5.4-pro
GPT-5.3 series
gpt-5.3-chat
,
gpt-5.3-codex
GPT-5.2 series
gpt-5.2-codex
,
gpt-5.2
,
gpt-5.2-chat
Preview
GPT-5.1 series
gpt-5.1
,
gpt-5.1-chat
Preview
,
gpt-5.1-codex
,
gpt-5.1-codex-mini
Sora
NEW
sora-2
GPT-5 series
gpt-5
,
gpt-5-mini
,
gpt-5-nano
,
gpt-5-chat
Preview
gpt-oss
open-weight reasoning models
codex-mini
Fine-tuned version of
o4-mini
.
GPT-4.1 series
gpt-4.1
,
gpt-4.1-mini
,
gpt-4.1-nano
computer-use-preview
An experimental model trained for use with the Responses API computer use tool.
o-series models
Reasoning models
with advanced problem solving and increased focus and capability.
GPT-4o, GPT-4o mini, and GPT-4 Turbo
Capable Azure OpenAI models with multimodal versions, which can accept both text and images as input.
Embeddings
A set of models that can convert text into numerical vector form to facilitate text similarity.
Image generation
A series of models that can generate original images from natural language.
Video generation
A model that can generate original video scenes from text instructions.
Audio
A series of models for speech to text, translation, and text to speech. GPT-4o audio models support either low latency
speech in, speech out
conversational interactions or audio generation.
GPT-chat-latest
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Capabilities
Model ID
Description
Context Window
Max Output Tokens
Training Data (up to)
gpt-chat-latest
(2026-05-28)
Preview
-
Reasoning
- Chat Completions API.
-
Responses API
.
- Structured outputs
- Functions, tools, and parallel tool calling.
128,000
Input: 111,616
Output: 16,384
16,384
August 2025
gpt-chat-latest
(2026-05-05)
Preview
-
Reasoning
- Chat Completions API.
-
Responses API
.
- Structured outputs
- Functions, tools, and parallel tool calling.
128,000
Input: 111,616
Output: 16,384
16,384
August 2025
Note
You might also see this model referred to by OpenAI as GPT-5.5 Instant or in the OpenAI API as
chat-latest
. In Microsoft Foundry, the product name for this release is
gpt-chat-latest
. The model continues to follow the existing
Preview lifecycle
and standard notice periods. The team is also evaluating ways to simplify how customers access continuously updated models over time, but current behavior remains unchanged as that work continues.
GPT-5.5
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Capabilities
Model ID
Description
Context Window
Max Output Tokens
Training Data (up to)
gpt-5.5
(2026-04-24)
-
Reasoning
-
Responses API
.
- Chat Completions API.
- Structured outputs.
- Text and image processing.
- Functions, tools, and parallel tool calling.
-
Computer use
-
Full summary of capabilities
.
1,050,000 br>
Input: 922,000
Output: 128,000
128,000
December 2025
Note
Some
quota tiers
will require quota requests for
gpt-5.5
to be able to deploy this model. Tier 5 and Tier 6 subscriptions have quota by default.
GPT-5.4
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Capabilities
Model ID
Description
Context Window
Max Output Tokens
Training Data (up to)
gpt-5.4
(2026-03-05)
-
Reasoning
-
Responses API
.
- Chat Completions API.
- Structured outputs.
- Text and image processing.
- Functions, tools, and parallel tool calling.
-
Computer use
-
Full summary of capabilities
.
1,050,000
128,000
August 2025
gpt-5.4-pro
(2026-03-05)
-
Reasoning
-
Responses API
.
- Text and image processing.
- Functions & tools
-
Full summary of capabilities
.
1,050,000
128,000
August 2025
gpt-5.4-mini
(2026-03-17)
-
Reasoning
-
Responses API
.
- Chat Completions API.
- Structured outputs.
- Text and image processing.
- Functions, tools, and parallel tool calling.
-
Computer use
-
Full summary of capabilities
.
400,000
Input: 272,000
Output: 128,000
128,000
August 2025
gpt-5.4-nano
(2026-03-17)
-
Reasoning
-
Responses API
.
- Chat Completions API.
- Structured outputs.
- Text and image processing.
- Functions, tools, and parallel tool calling.
-
Full summary of capabilities
.
400,000
Input: 272,000
Output: 128,000
128,000
August 2025
GPT-5.3
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Capabilities
Model ID
Description
Context Window
Max Output Tokens
Training Data (up to)
gpt-5.3-codex
(2026-02-24)
-
Reasoning
-
Responses API
.
- Structured outputs.
- Text and image processing.
- Functions, tools, and parallel tool calling.
-
Full summary of capabilities
.
- Optimized for
Codex CLI & Codex VS Code extension
400,000
Input: 272,000
Output: 128,000
128,000
August 2025
gpt-5.3-chat
(2026-03-03)
Preview
- Chat Completions API.
-
Responses API
.
- Structured outputs
- Functions, tools, and parallel tool calling.
128,000
Input: 111,616
Output: 16,384
16,384
August 2025
GPT-5.2
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Capabilities
Model ID
Description
Context Window
Max Output Tokens
Training Data (up to)
gpt-5.2-codex
(2026-01-14)
-
Reasoning
-
Responses API
.
- Structured outputs.
- Text and image processing.
- Functions, tools, and parallel tool calling.
-
Full summary of capabilities
.
- Optimized for
Codex CLI & Codex VS Code extension
400,000
Input: 272,000
Output: 128,000
128,000
gpt-5.2
(2025-12-11)
-
Reasoning
- Chat Completions API.
-
Responses API
.
- Structured outputs.
- Text and image processing.
- Functions, tools, and parallel tool calling.
-
Full summary of capabilities
.
400,000
Input: 272,000
Output: 128,000
128,000
August 2025
gpt-5.2-chat
(2025-12-11)
Preview
- Chat Completions API.
-
Responses API
.
- Structured outputs
- Functions, tools, and parallel tool calling.
128,000
Input: 111,616
Output: 16,384
16,384
August 2025
gpt-5.2-chat
(2026-02-10)
Preview
- Chat Completions API.
-
Responses API
.
- Structured outputs
- Functions, tools, and parallel tool calling.
128,000
Input: 111,616
Output: 16,384
16,384
August 2025
Caution
We don't recommend using preview models in production. We'll upgrade all deployments of preview models to either future preview versions or to the latest stable, generally available version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.
GPT-5.1
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Capabilities
Model ID
Description
Context Window
Max Output Tokens
Training Data (up to)
gpt-5.1
(2025-11-13)
-
Reasoning
- Chat Completions API.
-
Responses API
.
- Structured outputs.
- Text and image processing.
- Functions, tools, and parallel tool calling.
-
Full summary of capabilities
.
400,000
Input: 272,000
Output: 128,000
128,000
September 30, 2024
gpt-5.1-chat
(2025-11-13)
Preview
-
Reasoning
- Chat Completions API.
-
Responses API
.
- Structured outputs
- Functions, tools, and parallel tool calling.
128,000
Input: 111,616
Output: 16,384
16,384
September 30, 2024
gpt-5.1-codex
(2025-11-13)
-
Responses API
only.
- Text and image processing
- Structured outputs.
- Functions, tools, and parallel tool calling.
-
Full summary of capabilities
- Optimized for
Codex CLI & Codex VS Code extension
400,000
Input: 272,000
Output: 128,000
128,000
September 30, 2024
gpt-5.1-codex-mini
(2025-11-13)
-
Responses API
only.
- Text and image processing
- Structured outputs.
- Functions, tools, and parallel tool calling.
-
Full summary of capabilities
- Optimized for
Codex CLI & Codex VS Code extension
400,000
Input: 272,000
Output: 128,000
128,000
September 30, 2024
gpt-5.1-codex-max
(2025-12-04)
-
Responses API
only.
- Text and image processing
- Structured outputs.
- Functions, tools, and parallel tool calling.
-
Full summary of capabilities
- Optimized for
Codex CLI & Codex VS Code extension
400,000
Input: 272,000
Output: 128,000
128,000
September 30, 2024
Caution
We don't recommend using preview models in production. We'll upgrade all deployments of preview models to either future preview versions or to the latest stable, generally available version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.
Important
gpt-5.1
reasoning_effort
defaults to
none
. When upgrading from previous reasoning models to
gpt-5.1
, keep in mind that you may need to update your code to explicitly pass a
reasoning_effort
level if you want reasoning to occur.
gpt-5.1-chat
adds built-in reasoning capabilities. Like other
reasoning models
it does not support parameters like
temperature
. If you upgrade from using
gpt-5-chat
(which is not a reasoning model) to
gpt-5.1-chat
make sure you remove any custom parameters like
temperature
from your code which are not supported by reasoning models.
gpt-5.1-codex-max
adds support for setting
reasoning_effort
to
xhigh
. Reasoning effort
none
is not supported with
gpt-5.1-codex-max
.
GPT-5
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Capabilities
Model ID
Description
Context Window
Max Output Tokens
Training Data (up to)
gpt-5
(2025-08-07)
-
Reasoning
- Chat Completions API.
-
Responses API
.
- Structured outputs.
- Text and image processing.
- Functions, tools, and parallel tool calling.
-
Full summary of capabilities
.
400,000
Input: 272,000
Output: 128,000
128,000
September 30, 2024
gpt-5-mini
(2025-08-07)
-
Reasoning
- Chat Completions API.
-
Responses API
.
- Structured outputs.
- Text and image processing.
- Functions, tools, and parallel tool calling.
-
Full summary of capabilities
.
400,000
Input: 272,000
Output: 128,000
128,000
May 31, 2024
gpt-5-nano
(2025-08-07)
-
Reasoning
- Chat Completions API.
-
Responses API
.
- Structured outputs.
- Text and image processing.
- Functions, tools, and parallel tool calling.
-
Full summary of capabilities
.
400,000
Input: 272,000
Output: 128,000
128,000
May 31, 2024
gpt-5-chat
(2025-08-07)
Preview
- Chat Completions API.
-
Responses API
.
-
Input
: Text/Image
-
Output
: Text only
128,000
16,384
September 30, 2024
gpt-5-chat
(2025-10-03)
Preview
1
- Chat Completions API.
-
Responses API
.
-
Input
: Text/Image
-
Output
: Text only
128,000
16,384
September 30, 2024
gpt-5-codex
(2025-09-11)
-
Responses API
only.
-
Input
: Text/Image
-
Output
: Text only
- Structured outputs.
- Text and image processing.
- Functions, tools, and parallel tool calling.
-
Full summary of capabilities
- Optimized for
Codex CLI & Codex VS Code extension
400,000
Input: 272,000
Output: 128,000
128,000
-
gpt-5-pro
(2025-10-06)
-
Reasoning
-
Responses API
.
- Structured outputs.
- Text and image processing.
- Functions and tools
-
Full summary of capabilities
.
400,000
Input: 272,000
Output: 128,000
128,000
September 30, 2024
Note
1
gpt-5-chat
version
2025-10-03
introduces a significant enhancement focused on emotional intelligence and mental health capabilities. This upgrade integrates specialized datasets and refined response strategies to improve the model's ability to:
Understand and interpret emotional context
more accurately, enabling nuanced and empathetic interactions.
Provide supportive, responsible responses
in conversations related to mental health, ensuring sensitivity and adherence to best practices.
These improvements aim to make GPT-5-chat more context-aware, human-centric, and reliable in scenarios where emotional tone and well-being considerations are critical.
Caution
We don't recommend using preview models in production. We'll upgrade all deployments of preview models to either future preview versions or to the latest stable, generally available version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.
gpt-oss
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Capabilities
Model ID
Description
Context Window
Max Output Tokens
Training Data (up to)
gpt-oss-120b
1
(Preview)
- Text in/text out only
- Chat Completions API
- Streaming
- Function calling
- Structured outputs
- Reasoning
- Available for deployment
1
and via
managed compute
131,072
131,072
May 31, 2024
gpt-oss-20b
(Preview)
- Text in/text out only
- Chat Completions API
- Streaming
- Function calling
- Structured outputs
- Reasoning
- Available via
managed compute
and
Foundry Local
131,072
131,072
May 31, 2024
1
Unlike other Azure OpenAI models
gpt-oss-120b
requires a
Foundry project
to deploy the model.
Deploy with code
```
az cognitiveservices account deployment create \
  --name "Foundry-project-resource" \
  --resource-group "test-rg" \
  --deployment-name "gpt-oss-120b" \
  --model-name "gpt-oss-120b" \
  --model-version "1" \
  --model-format "OpenAI-OSS" \
  --sku-capacity 10 \
  --sku-name "GlobalStandard"

```
GPT-4.1 series
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Capabilities
Model ID
Description
Context window
Max output tokens
Training data (up to)
gpt-4.1
(2025-04-14)
- Text and image input
- Text output
- Chat completions API
- Responses API
- Streaming
- Function calling
- Structured outputs (chat completions)
- 1,047,576
- 300,000 (standard & provisioned managed deployments)
- 128,000 (batch deployments)
32,768
May 31, 2024
gpt-4.1-nano
(2025-04-14)
- Text and image input
- Text output
- Chat completions API
- Responses API
- Streaming
- Function calling
- Structured outputs (chat completions)
- 1,047,576
- 300,000 (standard & provisioned managed deployments)
- 128,000 (batch deployments)
32,768
May 31, 2024
gpt-4.1-mini
(2025-04-14)
- Text and image input
- Text output
- Chat completions API
- Responses API
- Streaming
- Function calling
- Structured outputs (chat completions)
- 1,047,576
- 300,000 (standard & provisioned managed deployments)
- 128,000 (batch deployments)
32,768
May 31, 2024
Known issue
A known issue is affecting all GPT 4.1 series models. Large tool or function call definitions that exceed 300,000 tokens will result in failures, even though the 1 million token context limit of the models wasn't reached.
The errors can vary based on API call and underlying payload characteristics.
Here are the error messages for the Chat Completions API:
Error code: 400 - {'error': {'message': "This model's maximum context length is 300000 tokens. However, your messages resulted in 350564 tokens (100 in the messages, 350464 in the functions). Please reduce the length of the messages or functions.", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}
Error code: 400 - {'error': {'message': "Invalid 'tools[0].function.description': string too long. Expected a string with maximum length 1048576, but got a string with length 2778531 instead.", 'type': 'invalid_request_error', 'param': 'tools[0].function.description', 'code': 'string_above_max_length'}}
Here's the error message for the Responses API:
Error code: 500 - {'error': {'message': 'The server had an error processing your request. Sorry about that! You can retry your request, or contact us through an Azure support request at: https://go.microsoft.com/fwlink/?linkid=2213926 if you keep seeing this error. (Please include the request ID d2008353-291d-428f-adc1-defb5d9fb109 in your email.)', 'type': 'server_error', 'param': None, 'code': None}}
computer-use-preview
An experimental model trained for use with the
Responses API
computer use tool.
It can be used with third-party libraries to allow the model to control mouse and keyboard input, while getting context from screenshots of the current environment.
Caution
We don't recommend using preview models in production. We'll upgrade all deployments of preview models to either future preview versions or to the latest stable, generally available version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.
Registration is required to access
computer-use-preview
. Access is granted based on Microsoft's eligibility criteria. Customers who have access to other limited access models still need to request access for this model.
To request access, go to
computer-use-preview
limited access model application
. When access is granted, you need to create a deployment for the model.
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Capabilities
Model ID
Description
Context window
Max output tokens
Training data (up to)
computer-use-preview
(2025-03-11)
Specialized model for use with the
Responses API
computer use tool
- Tools
- Streaming
- Text (input/output)
- Image (input)
8,192
1,024
October 2023
o-series models
The Azure OpenAI o-series models are designed to tackle reasoning and problem-solving tasks with increased focus and capability. These models spend more time processing and understanding the user's request, making them exceptionally strong in areas like science, coding, and math, compared to previous iterations.
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Capabilities
Model ID
Description
Max request (tokens)
Training data (up to)
codex-mini
(2025-05-16)
Fine-tuned version of
o4-mini
.
-
Responses API
.
- Structured outputs.
- Text and image processing.
- Functions and tools.
Full summary of capabilities
.
Input: 200,000
Output: 100,000
May 31, 2024
o3-pro
(2025-06-10)
-
Responses API
.
- Structured outputs.
- Text and image processing.
- Functions and tools.
Full summary of capabilities
.
Input: 200,000
Output: 100,000
May 31, 2024
o4-mini
(2025-04-16)
-
New
reasoning model, offering
enhanced reasoning abilities
.
- Chat Completions API.
-
Responses API
.
- Structured outputs.
- Text and image processing.
- Functions and tools.
Full summary of capabilities
.
Input: 200,000
Output: 100,000
May 31, 2024
o3
(2025-04-16)
-
New
reasoning model, offering
enhanced reasoning abilities
.
- Chat Completions API.
-
Responses API
.
- Structured outputs.
- Text and image processing.
- Functions, tools, and parallel tool calling.
Full summary of capabilities
.
Input: 200,000
Output: 100,000
May 31, 2024
o3-mini
(2025-01-31)
-
Enhanced reasoning abilities
.
- Structured outputs.
- Text-only processing.
- Functions and tools.
Input: 200,000
Output: 100,000
October 2023
o1
(2024-12-17)
-
Enhanced reasoning abilities
.
- Structured outputs.
- Text and image processing.
- Functions and tools.
Input: 200,000
Output: 100,000
October 2023
o1-preview
1
(2024-09-12)
Older preview version.
Input: 128,000
Output: 32,768
October 2023
o1-mini
2
(2024-09-12)
A faster and more cost-efficient option in the o1 series, ideal for coding tasks that require speed and lower resource consumption.
- Global Standard deployment available by default.
- Standard (regional) deployments are currently only available for select customers who received access as part of the
o1-preview
limited access release.
Input: 128,000
Output: 65,536
October 2023
1
o1-preview
is available only for customers who were granted access as part of the original limited access.
2
o1-mini
is currently available to all customers for Global Standard deployment. Select customers were granted standard (regional) deployment access to
o1-mini
as part of the
o1-preview
limited access release. At this time, access to
o1-mini
standard (regional) deployments isn't being expanded.
o3-deep-research
is currently only available with Foundry Agent Service. To learn more, see the
Deep Research tool guidance
.
To learn more about advanced o-series models, see
Getting started with reasoning models
.
GPT-4o and GPT-4 Turbo
GPT-4o integrates text and images in a single model, which enables it to handle multiple data types simultaneously. This multimodal approach enhances accuracy and responsiveness in human-computer interactions. GPT-4o matches GPT-4 Turbo in English text and coding tasks while offering superior performance in non-English language tasks and vision tasks, setting new benchmarks for AI capabilities.
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
GPT-4 and GPT-4 Turbo models
These models can be used only with the Chat Completions API.
See
Model versions
to learn about how Azure OpenAI handles model version upgrades. See
Working with models
to learn how to view and configure the model version settings of your GPT-4 deployments.
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Capabilities
Model ID
Description
Max request (tokens)
Training data (up to)
gpt-4o
(2024-11-20)
GPT-4o (Omni)
- Structured outputs.
- Text and image processing.
- JSON Mode.
- Parallel function calling.
- Enhanced accuracy and responsiveness.
- Parity with English text and coding tasks compared to GPT-4 Turbo with Vision.
- Superior performance in non-English languages and in vision tasks.
- Enhanced creative writing ability.
Input: 128,000
Output: 16,384
October 2023
gpt-4o
(2024-08-06)
GPT-4o (Omni)
- Structured outputs.
- Text and image processing.
- JSON Mode.
- Parallel function calling.
- Enhanced accuracy and responsiveness.
- Parity with English text and coding tasks compared to GPT-4 Turbo with Vision.
- Superior performance in non-English languages and in vision tasks.
Input: 128,000
Output: 16,384
October 2023
gpt-4o-mini
(2024-07-18)
GPT-4o mini
- Fast, inexpensive, capable model ideal for replacing GPT-3.5 Turbo series models.
- Text and image processing.
- JSON Mode.
- Parallel function calling.
Input: 128,000
Output: 16,384
October 2023
gpt-4o
(2024-05-13)
GPT-4o (Omni)
- Text and image processing.
- JSON Mode.
- Parallel function calling.
- Enhanced accuracy and responsiveness.
- Parity with English text and coding tasks compared to GPT-4 Turbo with Vision.
- Superior performance in non-English languages and in vision tasks.
Input: 128,000
Output: 4,096
October 2023
gpt-4
1
(turbo-2024-04-09)
GPT-4 Turbo with Vision
New generally available model.
- Replacement for all previous GPT-4 preview models (
vision-preview
,
1106-Preview
,
0125-Preview
).
-
Feature availability
is currently different, depending on the method of input and the deployment type.
Input: 128,000
Output: 4,096
December 2023
1
The provisioned version of
gpt-4
version
turbo-2024-04-09
is currently limited to text only. For more information on provisioned deployments, see
Provisioned guidance
.
Caution
We don't recommend that you use preview models in production. We'll upgrade all deployments of preview models to either future preview versions or to the latest stable, generally available version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.
Embeddings
text-embedding-3-large
is the latest and most capable embedding model. You can't upgrade between embeddings models. To move from using
text-embedding-ada-002
to
text-embedding-3-large
, you need to generate new embeddings.
text-embedding-3-large
text-embedding-3-small
text-embedding-ada-002
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Capabilities
OpenAI reports that testing shows that both the large and small third generation embeddings models offer better average multi-language retrieval performance with the
MIRACL
benchmark. They still maintain performance for English tasks with the
MTEB
benchmark.
Evaluation benchmark
text-embedding-ada-002
text-embedding-3-small
text-embedding-3-large
MIRACL average
31.4
44.0
54.9
MTEB average
61.0
62.3
64.6
The third generation embeddings models support reducing the size of the embedding via a new
dimensions
parameter. Typically, larger embeddings are more expensive from a compute, memory, and storage perspective. When you can adjust the number of dimensions, you gain more control over overall cost and performance. The
dimensions
parameter isn't supported in all versions of the OpenAI 1.x Python library. To take advantage of this parameter, we recommend that you upgrade to the latest version:
pip install openai --upgrade
.
OpenAI's MTEB benchmark testing found that even when the third generation model's dimensions are reduced to less than the 1,536 dimensions of
text-embeddings-ada-002
, performance remains slightly better.
These models can be used only with Embedding API requests.
Model ID
Max request (tokens)
Output dimensions
Training data (up to)
text-embedding-ada-002
(version 2)
8,192
1,536
Sep 2021
text-embedding-ada-002
(version 1)
2,046
1,536
Sep 2021
text-embedding-3-large
8,192
3,072
Sep 2021
text-embedding-3-small
8,192
1,536
Sep 2021
Note
When you send an array of inputs for embedding, the maximum number of input items in the array per call to the embedding endpoint is 2,048.
Image generation models
The image generation models generate images from text prompts that the user provides. Image generation models include
gpt-image-1
,
gpt-image-1-mini
,
gpt-image-1.5
, and
gpt-image-2
.
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Model ID
Max request (characters)
gpt-image-1
4,000
gpt-image-1-mini
4,000
gpt-image-1.5
4,000
Video generation models
Sora is an AI model from OpenAI that can create realistic and imaginative video scenes from text instructions. Sora is in preview.
Video generation models include
sora
and
sora-2
.
Model ID
Max Request (characters)
sora
4,000
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
Audio models
Audio models in Azure OpenAI are available via the
realtime
,
completions
, and
audio
APIs.
For model availability across all regions, grouped by deployment category, see
Region availability for Foundry Models sold by Azure
.
GPT-4o audio models
The GPT-4o audio models are part of the GPT-4o model family and support either low-latency,
speech in, speech out
conversational interactions or audio generation.
Caution
We don't recommend using preview models in production. We'll upgrade all deployments of preview models to either future preview versions or to the latest stable, generally available version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.
Details about maximum request tokens and training data are available in the following table:
Model ID
Description
Max request (tokens)
Training data (up to)
gpt-4o-mini-audio-preview
(2024-12-17)
Preview
Audio model for audio and text generation.
Input: 128,000
Output: 16,384
September 2023
gpt-4o-audio-preview
(2024-12-17)
Audio model for audio and text generation.
Input: 128,000
Output: 16,384
September 2023
gpt-4o-realtime-preview
(2025-06-03)
Audio model for real-time audio processing.
Input: 32,000
Output: 4,096
October 2023
gpt-4o-realtime-preview
(2024-12-17)
Audio model for real-time audio processing.
Input: 16,000
Output: 4,096
October 2023
gpt-4o-mini-realtime-preview
(2024-12-17)
Preview
Audio model for real-time audio processing.
Input: 128,000
Output: 4,096
October 2023
gpt-audio
(2025-08-28)
gpt-audio-mini
(2025-10-06)
Audio model for audio and text generation.
Input: 128,00
Output: 16,384
October 2023
gpt-realtime
(2025-08-28) (GA)
gpt-realtime-mini
(2025-10-06)
gpt-realtime-mini
(2025-12-15)
Audio model for real-time audio processing.
Input: 32,00
Output: 4,096
October 2023
gpt-audio-1.5
(2026-02-23)
Audio model for audio and text generation.
Input: 128,00
Output: 16,384
September 2024
gpt-realtime-1.5
(2026-02-23)
Audio model for real-time audio processing.
Input: 32,00
Output: 4,096
September 2024
gpt-realtime-2
(2026-05-07)
Audio model for real-time audio processing.
Input: 32,000
Output: 4,096
September 2024
Audio API
The audio models via the
/audio
API can be used for speech to text, translation, and text to speech.
Speech-to-text models
Model ID
Description
Max request (audio file size)
whisper
General-purpose speech recognition model.
25 MB
gpt-4o-transcribe
(2025-03-20)
Preview
Speech-to-text model powered by GPT-4o.
25 MB
gpt-4o-mini-transcribe
(2025-03-20)
Preview
Speech-to-text model powered by GPT-4o mini.
25 MB
gpt-4o-transcribe-diarize
(2025-10-15)
Preview
Speech-to-text model with automatic speech recognition.
25 MB
gpt-4o-mini-transcribe
(2025-12-15)
Preview
Speech-to-text model with automatic speech recognition. Improved transcription accuracy and robustness.
25 MB
Speech translation models
Model ID
Description
Max request (audio file size)
whisper
General-purpose speech recognition model.
25 MB
Text-to-speech models (preview)
Model ID
Description
tts
Preview
Text-to-speech model optimized for speed.
tts-hd
Preview
Text-to-speech model optimized for quality.
gpt-4o-mini-tts
(2025-03-20)
Text-to-speech model powered by GPT-4o mini.
You can guide the voice to speak in a specific style or tone.
gpt-4o-mini-tts
(2025-12-15)
Text-to-speech model powered by GPT-4o mini.
You can guide the voice to speak in a specific style or tone.
Fine-tuning models
The following models are supported for fine-tuning:
Model ID
Standard regions
Global
Developer
Methods
Status
Modality
gpt-4o-mini
(2024-07-18)
North Central US
Sweden Central
✅
✅
SFT
GA
Text to text
gpt-4o
(2024-08-06)
East US2
North Central US
Sweden Central
✅
✅
SFT, DPO
GA
Text and vision to text
gpt-4.1
(2025-04-14)
North Central US
Sweden Central
✅
✅
SFT, DPO
GA
Text and vision to text
gpt-4.1-mini
(2025-04-14)
North Central US
Sweden Central
✅
✅
SFT, DPO
GA
Text to text
gpt-4.1-nano
(2025-04-14)
North Central US
Sweden Central
✅
✅
SFT, DPO
GA
Text to text
o4-mini
(2025-04-16)
East US2
Sweden Central
✅
❌
RFT
GA
Text to text
gpt-5
(2025-08-07)
North Central US
Sweden Central
✅
✅
RFT
GA
*
Text to text
Ministral-3B
(2411)
Not supported
✅
❌
SFT
Public preview
Text to text
Qwen-32B
Not supported
✅
❌
SFT
Public preview
Text to text
Llama-3.3-70B-Instruct
Not supported
✅
❌
SFT
Public preview
Text to text
gpt-oss-20b
Not supported
✅
❌
SFT
Public preview
Text to text
*
GPT-5 support for reinforcement fine-tuning is generally available, but access is gated and available by invitation only. Contact your Microsoft account team if you're interested in enrollment.
Or you can fine-tune a previously fine-tuned model, formatted as
base-model.ft-{jobid}
.
Note
Open-source models (Ministral-3B, Qwen-32B, Llama-3.3-70B-Instruct, gpt-oss-20b) are only supported on Foundry resources and in the new Foundry UI.
Note
Global training provides
more affordable
training per token, but doesn't offer
data residency
. It's currently available to Foundry resources in the following regions:
Australia East
Brazil South
Canada Central
Canada East
East US
East US2
France Central
Germany West Central
Italy North
Japan East
(no vision support)
Korea Central
North Central US
Norway East
Poland Central
(no 4.1-nano support)
Southeast Asia
South Africa North
South Central US
South India
Spain Central
Sweden Central
Switzerland West
Switzerland North
UK South
West Europe
West US
West US3
Assistants (preview)
For Assistants, you need a combination of a supported model and a supported region. Certain tools and capabilities require the latest models. The following models are available in the Assistants API, SDK, and Foundry. The following table is for standard deployment. For information on provisioned throughput unit availability, see
Provisioned throughput models
. The listed models and regions can be used with both Assistants v1 and v2. You can use
Global Standard models
if they're supported in the following regions.
Region
gpt-4o, 2024-05-13
gpt-4o, 2024-08-06
gpt-4o-mini, 2024-07-18
gpt-4, 0613
gpt-4, 1106-Preview
gpt-4, 0125-Preview
gpt-4, turbo-2024-04-09
gpt-4-32k, 0613
gpt-35-turbo, 0613
gpt-35-turbo, 1106
gpt-35-turbo, 0125
gpt-35-turbo-16k, 0613
australiaeast
-
-
-
✅
✅
-
-
✅
✅
✅
✅
✅
eastus
✅
✅
✅
-
-
✅
✅
-
✅
-
✅
✅
eastus2
✅
✅
✅
-
✅
-
✅
-
✅
-
✅
✅
francecentral
-
-
-
✅
✅
-
-
✅
✅
✅
-
✅
japaneast
-
-
-
-
-
-
-
-
✅
-
✅
✅
norwayeast
-
-
-
-
✅
-
-
-
-
-
-
-
southindia
-
-
-
-
✅
-
-
-
-
✅
✅
-
swedencentral
✅
✅
✅
✅
✅
-
✅
✅
✅
✅
-
✅
uksouth
-
-
-
-
✅
✅
-
-
✅
✅
✅
✅
westus
✅
✅
✅
-
✅
-
✅
-
-
✅
✅
-
westus3
✅
✅
✅
-
✅
-
✅
-
-
-
✅
-
Model retirement
For the latest information on model retirements, refer to the
Model retirement schedule
.
Related content
Foundry Models from partners and community
Model retirement and deprecation
Learn more about working with Azure OpenAI models
Learn more about Azure OpenAI
Learn more about fine-tuning Azure OpenAI models
Black Forest Labs models sold by Azure
Black Forest Labs (BFL) FLUX models bring state-of-the-art image generation to Microsoft Foundry, enabling you to generate and edit high-quality images from text prompts and reference images. FLUX models support a range of capabilities including text-to-image generation, multi-reference image editing, and in-context generation and editing.
You can run these models through the BFL service provider API and through the
images/generations and images/edits endpoints
.
To work with FLUX models in Foundry, see
Deploy and use FLUX models in Microsoft Foundry
.
Model
Type & API endpoint
Capabilities
Deployment type (region availability)
FLUX.2-flex
Image generation
-
BFL service provider API
:
<resource-name>/providers/blackforestlabs/v1/flux-2-flex
-
Input:
text and image (32,000 tokens and up to 10 images
i
)
-
Output:
One Image
-
Tool calling:
No
-
Response formats:
Image (PNG and JPG)
-
Key features:
Fine-grained control; multi-reference support for up to 10 images
-
Additional parameters:
guidance
: Controls how closely the output follows the prompt. Minimum: 1.5, maximum: 10, default: 4.5. Higher = closer prompt adherence.
steps
: Number of inference steps. Maximum: 50, default: 50.  Higher = more detail, slower.
- Global standard (all regions)
FLUX.2-pro
Image generation
-
BFL service provider API
:
<resource-name>/providers/blackforestlabs/v1/flux-2-pro
-
Input:
text and image (32,000 tokens and up to 8 images
ii
)
-
Output:
One Image
-
Tool calling:
No
-
Response formats:
Image (PNG and JPG)
-
Key features:
Multi-reference support for up to 8 images; more grounded in real-world knowledge; greater output flexibility; enhanced performance
-
Additional parameters:
(In provider-specific API only)
Supports all parameters.
- Global standard (all regions)
FLUX.1-Kontext-pro
Image generation
-
Image API
:
https://<resource-name>/openai/deployments/{deployment-id}/images/generations
and
https://<resource-name>/openai/deployments/{deployment-id}/images/edits
-
BFL service provider API
:
<resource-name>/providers/blackforestlabs/v1/flux-kontext-pro?api-version=preview
-
Input:
text and image (5,000 tokens and 1 image)
-
Output:
One Image
-
Tool calling:
No
-
Response formats:
Image (PNG and JPG)
-
Key features:
Character consistency, advanced editing
-
Additional parameters:
(In provider-specific API only)
seed
,
aspect ratio
,
input_image
,
prompt_unsampling
,
safety_tolerance
,
output_format
- Global standard (all regions)
FLUX-1.1-pro
Image generation
-
Image API
:
https://<resource-name>/openai/deployments/{deployment-id}/images/generations
-
BFL service provider API
:
<resource-name>/providers/blackforestlabs/v1/flux-pro-1.1?api-version=preview
-
Input:
text (5,000 tokens and 1 image)
-
Output:
One Image
-
Tool calling:
No
-
Response formats:
Image (PNG and JPG)
-
Key features:
Fast inference speed, strong prompt adherence, competitive pricing, scalable generation
-
Additional parameters:
(In provider-specific API only)
width
,
height
,
prompt_unsampling
,
seed
,
safety_tolerance
,
output_format
- Global standard (all regions)
i,ii
Support for
multiple reference images
is available for FLUX.2 [pro] (Preview) and FLUX.2 [flex] (Preview) by using the API, but
not
in the playground.
Cohere models sold by Azure
The Cohere family of models includes various models optimized for different use cases, including chat completions, rerank/text classification, and embeddings. Cohere models are optimized for various use cases that include reasoning, summarization, and question answering.
Model
Type
Capabilities
Deployment type (region availability)
Cohere-rerank-v4.0-pro
text classification (rerank)
-
Input:
text
-
Output:
text
-
Languages:
en
,
fr
,
es
,
it
,
de
,
pt-br
,
ja
,
zh-cn
,
ar
,
vi
,
hi
,
ru
,
id
, and
nl
-
Tool calling:
No
-
Response formats:
JSON
- Global standard (all regions)
- Managed compute
Cohere-rerank-v4.0-fast
text classification (rerank)
-
Input:
text
-
Output:
text
-
Languages:
en
,
fr
,
es
,
it
,
de
,
pt-br
,
ja
,
zh-cn
,
ar
,
vi
,
hi
,
ru
,
id
, and
nl
-
Tool calling:
No
-
Response formats:
JSON
- Global standard (all regions)
- Managed compute
Cohere-command-a
chat-completion
-
Input:
text (131,072 tokens)
-
Output:
text (8,182 tokens)
-
Languages:
en
,
fr
,
es
,
it
,
de
,
pt-br
,
ja
,
ko
,
zh-cn
, and
ar
-
Tool calling:
Yes
-
Response formats:
Text, JSON
- Global standard (all regions)
embed-v-4-0
embeddings
-
Input:
text (512 tokens) and images (2MM pixels)
-
Output:
Vector (256, 512, 1024, 1536 dim.)
-
Languages:
en
,
fr
,
es
,
it
,
de
,
pt-br
,
ja
,
ko
,
zh-cn
, and
ar
- Global standard (all regions)
DeepSeek models sold by Azure
The DeepSeek family of models includes several reasoning models, which excel at reasoning tasks by using a step-by-step training process, such as language, scientific reasoning, and coding tasks.
Model
Type
Capabilities
Deployment type (region availability)
DeepSeek-V4-Pro
Preview
chat-completion
(with reasoning content)
-
Input:
text (1,000,000 tokens)
-
Output:
text (384,000 tokens)
-
Languages:
en
and
zh
-
Tool calling:
No
-
Response formats:
Text, JSON
- Global standard (all regions)
DeepSeek-V4-Flash
Preview
chat-completion
(with reasoning content)
-
Input:
text (1,000,000 tokens)
-
Output:
text (384,000 tokens)
-
Languages:
en
and
zh
-
Tool calling:
No
-
Response formats:
Text, JSON
- Global standard (all regions)
DeepSeek-V3.2-Speciale
chat-completion
(with reasoning content)
-
Input:
text (128,000 tokens)
-
Output:
text (128,000 tokens)
-
Languages:
en
and
zh
-
Tool calling:
No
-
Response formats:
Text, JSON
- Global standard (all regions)
DeepSeek-V3.2
chat-completion
(with reasoning content)
-
Input:
text (128,000 tokens)
-
Output:
text (128,000 tokens)
-
Languages:
en
and
zh
-
Tool calling:
No
-
Response formats:
Text, JSON
- Global standard (all regions)
DeepSeek-V3.1
chat-completion
(with reasoning content)
-
Input:
text (131,072 tokens)
-
Output:
text (131,072 tokens)
-
Languages:
en
and
zh
-
Tool calling:
Yes
-
Response formats:
Text, JSON
- Global standard (all regions)
DeepSeek-R1-0528
chat-completion
(with reasoning content)
-
Input:
text (163,840 tokens)
-
Output:
text (163,840 tokens)
-
Languages:
en
and
zh
-
Tool calling:
No
-
Response formats:
Text
- Global standard (all regions)
- Global provisioned (all regions)
DeepSeek-V3-0324
chat-completion
-
Input:
text (131,072 tokens)
-
Output:
text (131,072 tokens)
-
Languages:
en
and
zh
-
Tool calling:
Yes
-
Response formats:
Text, JSON
- Global standard (all regions)
- Global provisioned (all regions)
DeepSeek-R1
chat-completion
(with reasoning content)
-
Input:
text (163,840 tokens)
-
Output:
text (163,840 tokens)
-
Languages:
en
and
zh
-
Tool calling:
No
-
Response formats:
Text
- Global standard (all regions)
- Global provisioned (all regions)
Meta models sold by Azure
Meta Llama models and tools are a collection of pretrained and fine-tuned generative AI text and image reasoning models. Meta models range in scale to include:
Small language models (SLMs) like 1B and 3B Base and Instruct models for on-device and edge inferencing
Mid-size large language models (LLMs) like 7B, 8B, and 70B Base and Instruct models
High-performance models like Meta Llama 3.1-405B Instruct for synthetic data generation and distillation use cases.
Model
Type
Capabilities
Deployment type (region availability)
Llama-4-Maverick-17B-128E-Instruct-FP8
chat-completion
-
Input:
text and images (1M tokens)
-
Output:
text (1M tokens)
-
Languages:
ar
,
en
,
fr
,
de
,
hi
,
id
,
it
,
pt
,
es
,
tl
,
th
, and
vi
-
Tool calling:
No
-
Response formats:
Text
- Global standard (all regions)
Llama-3.3-70B-Instruct
chat-completion
-
Input:
text (128,000 tokens)
-
Output:
text (8,192 tokens)
-
Languages:
en
,
de
,
fr
,
it
,
pt
,
hi
,
es
, and
th
-
Tool calling:
No
-
Response formats:
Text
- Global standard (all regions)
- Global provisioned (all regions)
Several Meta models are also available
from partners and community
.
Microsoft models sold by Azure
Microsoft models include various model groups such as Model Router, MAI models, Phi models, healthcare AI models, and more. Several Microsoft models are also available
from partners and community
.
To work with MAI image models in Foundry, see
Deploy and use MAI image models in Microsoft Foundry
.
Model
Type
Capabilities
Deployment type (region availability)
MAI-Image-2.5-Flash
Preview
Image-to-Image and Text-to-Image. See
API endpoints
for details.
-
Input:
text, image (JPEG or PNG format for image editing workflows)
-
Output:
One image
-
Context length
: 32,000 tokens
-
Tool calling:
No
-
Response formats:
Image (PNG)
-
Languages:
en
-
Key features:
High-quality text-to-image generation; Image editing that supports precise, surgical edits without disrupting the rest of the image; Capability to generate realistic imagery with consistent visual structure. Well suited for tasks such as concept visualization, creative content generation, image editing workflows, and production design.
-
Parameters:
width
,
height
,
prompt
Minimum 768×768 pixels; maximum total pixel count 1,048,576 (equivalent to 1024×1024). Either dimension can exceed 1024 as long as the total pixel count stays within the limit (for example, 768×1365 is a valid size).
- Global standard (West Central US, East US, West US, West Europe, Sweden Central, South India, UAE North)
MAI-Image-2.5
Preview
Image-to-Image and Text-to-Image. See
API endpoints
for details.
-
Input:
text, image (JPEG or PNG format for image editing workflows)
-
Output:
One image
-
Context length
: 32,000 tokens
-
Tool calling:
No
-
Response formats:
Image (PNG)
-
Languages:
en
-
Key features:
High-quality text-to-image generation; Image editing that supports precise, surgical edits without disrupting the rest of the image; Capability to generate realistic imagery with consistent visual structure. Well suited for tasks such as concept visualization, creative content generation, image editing workflows, and production design.
-
Parameters:
width
,
height
,
prompt
Minimum 768×768 pixels; maximum total pixel count 1,048,576 (equivalent to 1024×1024). Either dimension can exceed 1024 as long as the total pixel count stays within the limit (for example, 768×1365 is a valid size).
- Global standard (West Central US, East US, West US, West Europe, Sweden Central, South India, UAE North)
MAI-Image-2e
Preview
Text-to-Image. See
API endpoint
for details.
-
Input:
text
-
Output:
One image
-
Context length
: 32,000 tokens
-
Tool calling:
No
-
Response formats:
Image (PNG)
-
Languages:
en
-
Key features:
High-quality text-to-image generation; photorealistic image synthesis with consistent visual structure; well suited for product imagery, marketing visuals, brand assets, and commercial creative workflows.
-
Parameters:
width
,
height
,
prompt
Minimum 768×768 pixels; maximum total pixel count 1,048,576 (equivalent to 1024×1024). Either dimension can exceed 1024 as long as the total pixel count stays within the limit (for example, 768×1365 is a valid size).
- Global standard (West Central US, East US, West US, West Europe, Sweden Central, South India, UAE North)
MAI-Image-2
Preview
Text-to-Image. See
API endpoint
for details.
-
Input:
text
-
Output:
One image
-
Context length
: 32,000 tokens
-
Tool calling:
No
-
Response formats:
Image (PNG)
-
Languages:
en
-
Key features:
High-quality text-to-image generation; photorealistic image synthesis with consistent visual structure; well suited for product imagery, marketing visuals, brand assets, and commercial creative workflows.
-
Parameters:
width
,
height
,
prompt
Minimum 768×768 pixels; maximum total pixel count 1,048,576 (equivalent to 1024×1024). Either dimension can exceed 1024 as long as the total pixel count stays within the limit (for example, 768×1365 is a valid size).
- Global standard (West Central US, East US, West US, West Europe, Sweden Central, South India, UAE North)
model-router
1
chat-completion
More details in
Model router overview
.
-
Input:
text, image
-
Output:
text (max output tokens varies
2
)
Context window:
200,000
3
-
Languages:
en
- Global standard (East US 2, Sweden Central)
- Data Zone standard
4
(East US 2, Sweden Central)
1
Model router version
2025-11-18
. Earlier versions (
2025-08-07
and
2025-05-19
) are also available.
2
Max output tokens
varies for underlying models in the model router. For example, 32,768 (
GPT-4.1 series
), 100,000 (
o4-mini
), 128,000 (
gpt-5 reasoning models
), and 16,384 (
gpt-5-chat
).
3
Larger
context windows
are compatible with
some
of the underlying models of the Model Router. That means an API call with a larger context succeeds only if the prompt gets routed to one of such models. Otherwise, the call fails.
4
Billing for
Data Zone Standard
model router deployments begins no earlier than November 1, 2025.
Mistral models sold by Azure
Model
Type
Capabilities
Deployment type (region availability)
mistral-document-ai-2512
Image-to-Text
-
Input:
image or PDF pages (30 pages, max 30MB PDF file)
-
Output:
text
-
Languages:
en
-
Tool calling:
no
-
Response formats:
Text, JSON, Markdown
- Global standard (all regions)
- Data zone standard (US and EU)
Mistral-Large-3
chat-completion
-
Input:
text, image
-
Output:
text
-
Languages:
en
,
fr
,
de
,
es
,
it
,
pt
,
nl
,
zh
,
ja
,
ko
, and
ar
-
Tool calling:
Yes
-
Response formats:
Text, JSON
- Global standard (all regions)
- Data zone standard (US and EU)
Several Mistral models are also available
from partners and community
.
Moonshot AI models sold by Azure
Moonshot AI models include Kimi K2.6 (Preview) and Kimi K2.5 (Preview), multimodal reasoning models that accept text and image input.
Model
Type
Capabilities
Deployment type (region availability)
Kimi-K2.6
Preview
chat-completion
(with reasoning content)
-
Input:
text and image (262,144 tokens)
-
Output:
text (262,144 tokens)
-
Languages:
en
and
zh
-
Tool calling:
Yes
-
Response formats:
Text
- Global standard (all regions)
Kimi-K2.5
Preview
chat-completion
(with reasoning content)
-
Input:
text and image (262,144 tokens)
-
Output:
text (262,144 tokens)
-
Languages:
en
and
zh
-
Tool calling:
Yes
-
Response formats:
Text
- Global standard (all regions)
See
this model collection in the Foundry portal
.
xAI models sold by Azure
xAI's Grok models in Foundry Models include a diverse set of reasoning and non-reasoning models designed for enterprise use cases such as data extraction, coding, text summarization, and agentic applications.
Registration is required for access to
grok-code-fast-1
(Preview) and
grok-4
.
Model
Type
Capabilities
Deployment type (region availability)
grok-4.3
Preview
chat-completion
-
Input:
text (200,000 tokens)
-
Output:
text (8,192 tokens)
-
Languages:
en
-
Tool calling:
yes
-
Response formats:
text
- Global standard (all regions)
grok-4-20-reasoning
Preview
chat-completion
-
Input:
text (262,000 tokens)
-
Output:
text (8,192 tokens)
-
Languages:
en
-
Tool calling:
yes
-
Response formats:
text
- Global standard (all regions)
grok-4-20-non-reasoning
Preview
chat-completion
-
Input:
text (262,000 tokens)
-
Output:
text (8,192 tokens)
-
Languages:
en
-
Tool calling:
yes
-
Response formats:
text
- Global standard (all regions)
grok-4.1-fast-reasoning
chat-completion
-
Input:
text, image (128,000 tokens)
-
Output:
text (128,000 tokens)
-
Languages:
en
-
Tool calling:
yes
-
Response formats:
text
- Global standard (all regions)
grok-4.1-fast-non-reasoning
chat-completion
-
Input:
text, image (128,000 tokens)
-
Output:
text (128,000 tokens)
-
Languages:
en
-
Tool calling:
yes
-
Response formats:
text
- Global standard (all regions)
grok-4
chat-completion
-
Input:
text (262,000 tokens)
-
Output:
text (8,192 tokens)
-
Languages:
en
-
Tool calling:
yes
-
Response formats:
text
- Global standard (all regions)
grok-code-fast-1
chat-completion
-
Input:
text (256,000 tokens)
-
Output:
text (8,192 tokens)
-
Languages:
en
-
Tool calling:
yes
-
Response formats:
text
- Global standard (all regions)
Model region availability by deployment type
Microsoft Foundry provides customers with choices on the hosting structure that fits their business and usage patterns. The service offers two main deployment categories:
Standard
: Has a global deployment option, routing traffic globally to provide higher throughput.
Provisioned
: Also has a global deployment option, allowing customers to purchase and deploy provisioned throughput units across Azure global infrastructure.
Other deployment categories like
batch
are also available. To learn about all available model deployment types, see
Deployment types for Microsoft Foundry Models
.
Global Standard
Global Provisioned managed
Data Zone Standard
Global Standard model availability
Region
FLUX.2-flex
FLUX.2-pro
FLUX.1-Kontext-pro
FLUX-1.1-pro
Cohere-rerank-v4.0-pro
Cohere-rerank-v4.0-fast
cohere-command-a
embed-v-4-0
DeepSeek-V3.2-Speciale
DeepSeek-V3.2
DeepSeek-V3.1
DeepSeek-R1-0528
DeepSeek-V3-0324
DeepSeek-R1
Llama-4-Maverick-17B-128E-Instruct-FP8
Llama-3.3-70B-Instruct
MAI-Image-2
model-router
mistral-document-ai-2512
mistral-document-ai-2505
Mistral-Large-3
Kimi-K2.5
grok-4-1-fast-reasoning
grok-4-1-fast-non-reasoning
grok-4-fast-reasoning
grok-4-fast-non-reasoning
grok-3
grok-3-mini
australiaeast
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
brazilsouth
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
canadacentral
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
canadaeast
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
centralus
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
eastus
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
eastus2
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
francecentral
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
germanywestcentral
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
italynorth
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
japaneast
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
japanwest
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
koreacentral
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
northcentralus
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
norwayeast
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
polandcentral
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
southafricanorth
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
southcentralus
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
southindia
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
spaincentral
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
swedencentral
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
switzerlandnorth
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
switzerlandwest
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
uaenorth
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
uksouth
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
westcentralus
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
westeurope
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
westus
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
westus2
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
westus3
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
-
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
Global Provisioned managed model availability
Region
DeepSeek-R1-0528
DeepSeek-V3-0324
DeepSeek-R1
Llama-3.3-70B-Instruct
australiaeast
✅
✅
✅
✅
brazilsouth
✅
✅
✅
✅
canadacentral
✅
✅
✅
✅
canadaeast
✅
✅
✅
✅
centralus
✅
✅
✅
✅
eastus
✅
✅
✅
✅
eastus2
✅
✅
✅
✅
francecentral
✅
✅
✅
✅
germanywestcentral
✅
✅
✅
✅
italynorth
✅
✅
✅
✅
japaneast
✅
✅
✅
✅
japanwest
✅
✅
✅
✅
koreacentral
✅
✅
✅
✅
northcentralus
✅
✅
✅
✅
norwayeast
✅
✅
✅
✅
polandcentral
✅
✅
✅
✅
southafricanorth
✅
✅
✅
✅
southcentralus
✅
✅
✅
✅
southindia
✅
✅
✅
✅
spaincentral
✅
✅
✅
✅
swedencentral
✅
✅
✅
✅
switzerlandnorth
✅
✅
✅
✅
switzerlandwest
✅
✅
✅
✅
uaenorth
✅
✅
✅
✅
uksouth
✅
✅
✅
✅
westcentralus
✅
✅
✅
✅
westeurope
✅
✅
✅
✅
westus
✅
✅
✅
✅
westus2
✅
✅
✅
✅
westus3
✅
✅
✅
✅
Data Zone Standard model availability
Region
FLUX.2-pro
FLUX.1-Kontext-pro
FLUX-1.1-pro
model-router
mistral-document-ai-2512
mistral-document-ai-2505
Mistral-Large-3
grok-4-1-fast-reasoning
grok-4-1-fast-non-reasoning
grok-4-fast-reasoning
grok-4-fast-non-reasoning
grok-3
grok-3-mini
centralus
✅
✅
✅
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
eastus
✅
✅
✅
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
eastus2
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
✅
francecentral
✅
✅
✅
-
✅
✅
✅
-
-
-
-
-
-
germanywestcentral
✅
✅
✅
-
✅
✅
✅
-
-
-
-
-
-
italynorth
✅
✅
✅
-
✅
✅
✅
-
-
-
-
-
-
northcentralus
✅
✅
✅
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
polandcentral
✅
✅
✅
-
✅
✅
✅
-
-
-
-
-
-
southcentralus
✅
✅
✅
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
spaincentral
✅
✅
✅
-
✅
✅
✅
-
-
-
-
-
-
swedencentral
✅
✅
✅
✅
✅
✅
✅
-
-
-
-
-
-
westcentralus
✅
✅
✅
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
westeurope
✅
✅
✅
-
✅
✅
✅
-
-
-
-
-
-
westus
✅
✅
✅
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
westus2
✅
✅
✅
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
westus3
✅
✅
✅
-
✅
✅
✅
✅
✅
✅
✅
✅
✅
Related content
Foundry Models from partners and community
Model deprecation and retirement for Foundry Models
Deployment overview for Foundry Models
Add and configure models to Foundry Models
Deployment types in Foundry Models
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