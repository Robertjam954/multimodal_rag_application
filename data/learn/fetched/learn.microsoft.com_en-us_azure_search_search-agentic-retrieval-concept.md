<!-- source: https://learn.microsoft.com/en-us/azure/search/search-agentic-retrieval-concept -->

# Agentic retrieval in Azure AI Search

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
Agentic retrieval in Azure AI Search
Summarize this article for me
Note
Some agentic retrieval features are generally available in the 2026-04-01 REST API via programmatic access. The Azure portal and Microsoft Foundry portal continue to provide preview-only access to all agentic retrieval features. For migration guidance, including a breakdown of what's generally available and what remains in preview, see
Migrate agentic retrieval code to the latest version
.
If you choose to use a preview REST API, you can access agentic retrieval capabilities that aren't yet generally available. Preview features are provided without a service-level agreement and aren't recommended for production workloads. For more information, see
Supplemental Terms of Use for Microsoft Azure Previews
.
Important
These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the
Microsoft Product Terms
, the
Microsoft Products and Services Data Protection Addendum
("DPA"), and the
Supplemental Terms of Use for Microsoft Azure Previews
.
The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the
Azure AI Search Transparency Note
.
In Azure AI Search,
agentic retrieval
is a multi-query pipeline designed for complex questions posed by users or agents in chat and copilot apps. It's intended for
retrieval-augmented generation
(RAG) patterns and agent-to-agent workflows.
Here's what it does:
Can use a large language model (LLM) to break down a complex query into smaller, focused subqueries for better coverage over proprietary and external content. Subqueries can include chat history for extra context.
Runs subqueries in parallel. Each subquery is semantically reranked to promote the most relevant matches.
Combines the best results into a unified response that an LLM can use to generate grounded answers.
Can return source references and an activity log alongside the merged content, so you can use just the grounding data or pass it to an LLM for a full answer.
This high-performance pipeline helps you generate high-quality grounding data or answers for your chat application, with the ability to answer complex questions quickly.
Why use agentic retrieval?
There are two use cases for agentic retrieval. First, it powers
Foundry IQ
in the Microsoft Foundry portal by providing the knowledge layer for agent solutions. Second, it's the basis for custom agentic solutions you build using the Azure AI Search APIs.
Use agentic retrieval when you want to provide agents and apps with the most relevant content for answering harder questions, drawing on chat context, your proprietary content, and external sources.
Agentic retrieval adds latency compared to a single-query pipeline, but it handles query complexity that a single query can't. For example, it can handle:
Questions with multiple asks, such as "find me a hotel near the beach, with airport transportation, and that's within walking distance of vegetarian restaurants."
Questions that depend on earlier context in the conversation.
Queries that benefit from rewriting, using synonym maps and LLM-generated paraphrasing to expand coverage across your content.
Spelling mistakes.
Architecture and workflow
The agentic retrieval process works as follows:
Workflow initiation:
Your application calls a knowledge base with a retrieve action that provides a query and conversation history.
Query planning:
At
low
and
medium
retrieval reasoning effort, the knowledge base sends your query and conversation history to an LLM, which generates focused subqueries. At
minimal
effort, this step is skipped and queries are issued directly to knowledge sources. Reasoning effort defaults to
low
and is configured on the knowledge base.
Query execution:
The knowledge base sends the subqueries to your knowledge sources. All subqueries run simultaneously and can be keyword, vector, or hybrid search. Each subquery undergoes semantic reranking to find the most relevant matches. References are extracted and retained for citation purposes.
Result synthesis:
The system combines all results into a unified response. Merged content is always returned. Source references and an execution activity log are optional.
Components
For all agentic retrieval scenarios, a knowledge base and at least one knowledge source are required. Other components are optional and depend on your configuration.
Component
Service
Role
Knowledge base
Azure AI Search
Orchestrates the pipeline, managing knowledge sources and query parameters.
Knowledge source
Azure AI Search
Defines the content used in the pipeline. Can be indexed (backed by a search index on your service) or remote (content retrieved at query time from an external platform).
Search index
Azure AI Search
Stores searchable content (text and vectors) with a semantic configuration. Determines which query types run and which optimizations apply. Required for indexed knowledge sources only.
Semantic ranker
Azure AI Search
Used internally by the agentic retrieval pipeline to rerank results for relevance (L2 reranking).
LLM
Azure OpenAI
Plans queries and selects knowledge sources. Used at
low
and
medium
retrieval reasoning effort only. Bypassed at
minimal
effort.
Integration requirements
Your application drives the pipeline by calling the knowledge base and handling the response. The pipeline returns grounding data that you can pass to an LLM for answer generation or use directly in your conversation interface. For implementation details, see
Tutorial: Build an end-to-end agentic retrieval solution
.
Availability and pricing
Agentic retrieval is available in
select regions
. Knowledge sources and knowledge bases also have
maximum limits
that vary by pricing tier and retrieval reasoning effort.
Billing
Agentic retrieval incurs charges from two services:
Azure AI Search
bills for retrieval tokens consumed during subquery execution and semantic ranking. The free plan (default) provides a monthly token allowance. The standard plan enables pay-as-you-go pricing after the free allowance is consumed. For more information, see
Enable or disable agentic retrieval billing
.
Azure OpenAI
bills for input and output tokens used in LLM-based query planning and
answer synthesis
. Pricing is always pay-as-you-go and based on the model you assign to the knowledge base. Charges appear on your Azure OpenAI bill. For rates, see
Azure OpenAI pricing
.
The following table compares billing between the classic single-query pipeline and the agentic retrieval multi-query pipeline. In the classic pipeline, the billable component is
semantic ranker
.
Aspect
Classic pipeline
Agentic retrieval
Unit
Query based
Token based
Cost per unit
Uniform cost per query
Variable cost per token (depends on reasoning effort)
Cost estimation
Estimate query count
Estimate token usage
Free allowance
Monthly free query allowance
Monthly free token allowance
Example: Estimate costs
This example helps illustrate the cost estimation process for query planning and query execution, but not answer synthesis. Your costs could be lower. For current rates, see
Azure AI Search pricing
and
Azure OpenAI pricing
.
To estimate the query plan costs as pay-as-you-go in Azure OpenAI, let's assume gpt-4o-mini:
15 cents for 1 million input tokens.
60 cents for 1 million output tokens.
2,000 input tokens for average chat conversation size.
350 tokens for average output plan size.
Estimated billing costs for query execution
To estimate agentic retrieval token counts, start with an idea of what an average document in your index looks like. For example, you might approximate:
10,000 chunks, where each chunk is one to two paragraphs of a PDF.
500 tokens per chunk.
Each subquery reranks up to 50 chunks.
On average, there are three subqueries per query plan.
Calculating price of execution
Assume we make 2,000 agentic retrievals with three subqueries per plan. This gives us about 6,000 total queries.
Rerank 50 chunks per subquery, which is 300,000 total chunks.
Average chunk is 500 tokens, so the total tokens for reranking is 150 million.
Given a hypothetical price of 0.022 per token, $3.30 is the total cost for reranking in US dollars.
Moving on to query plan costs: 2,000 input tokens multiplied by 2,000 agentic retrievals equal 4 million input tokens for a total of 60 cents.
Estimate the output costs based on an average of 350 tokens. If we multiply 350 by 2,000 agentic retrievals, we get 700,000 output tokens total for a total of 42 cents.
Putting it all together, you'd pay about $3.30 for agentic retrieval in Azure AI Search, 60 cents for input tokens in Azure OpenAI, and 42 cents for output tokens in Azure OpenAI, for $1.02 for query planning total. The combined cost for the full execution is $4.32.
Tips for controlling costs
Review the activity log in the response to find out what queries were issued to which sources and the parameters used. You can reissue those queries against your indexes and use a public tokenizer to estimate tokens and compare to API-reported usage. Precise reconstruction of a query or response isn't guaranteed however. Factors include the type of knowledge source, such as public web data or a remote SharePoint knowledge source that's predicated on a user identity, which can affect query reproduction.
Reduce the number of knowledge sources (indexes); consolidating content can lower fan-out and token volume.
Lower the reasoning effort to reduce LLM usage during query planning and query expansion (iterative search).
Organize content so the most relevant information can be found with fewer sources and documents (for example, curated summaries or tables).
How to get started
To create an agentic retrieval solution, you can use the Azure portal, Microsoft Foundry (new) portal, REST APIs, or an equivalent Azure SDK package.
Quickstarts
How-to guides
Tutorials
Code samples
REST API references
Demos
Quickstart: Agentic retrieval in the Azure portal
Quickstart: Agentic retrieval
(C#, Java, JavaScript, Python, TypeScript, REST)
The following articles cover core pipeline setup. For all how-to guides, see the table of contents.
Create a search index for agentic retrieval
Create a knowledge source
(links to how-to guide for each knowledge source kind)
Create a knowledge base
Query a knowledge base using the retrieve action or MCP endpoint
Tutorial: Build an end-to-end agentic retrieval solution
Quickstart-Agentic-Retrieval: Python
Quickstart-Agentic-Retrieval: .NET
Quickstart-Agentic-Retrieval: REST
End-to-end with Azure AI Search and Foundry Agent Service
Knowledge Sources
Knowledge Bases
Knowledge Retrieval
Azure OpenAI Demo
has been updated to use agentic retrieval.
Next step
Quickstart: Agentic retrieval
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