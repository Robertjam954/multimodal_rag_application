<!-- source: https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview -->

# What is Azure Document Intelligence in Foundry Tools?

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
What is Azure Document Intelligence in Foundry Tools?
Summarize this article for me
This content applies to:
v4.0 (GA)
|
Prior versions:
v3.1 (GA)
v3.0 (retiring)
v2.1 (retiring)
This content applies to:
v3.1 (GA)
|
Latest version:
v4.0 (GA)
|
Prior versions:
v3.0
v2.1
This content applies to:
v3.0 (retiring)
|
Latest versions:
v4.0 (GA)
v3.1
|
Previous version:
v2.1 (retiring)
This content applies to:
v2.1
|
Latest version:
v4.0 (GA)
Azure Document Intelligence in Foundry Tools is a cloud-based
Foundry Tools
service that you can use to build intelligent document processing solutions. Massive amounts of data, spanning various data types, are stored in forms and documents. You can use Azure Document Intelligence to effectively manage the speed at which data is collected and processed. Azure Document Intelligence is key to improved operations, informed data-driven decisions, and enlightened innovation. For information on region access, see
Product availability by region
.
Important
Document Intelligence REST API v2.1
reaches end of support on
September 15, 2027
.
Document Intelligence REST API 2022-08-31 v3.0
reaches end of support on
March 30, 2029
.
To avoid production disruption, use
Azure Document Intelligence 2024-11-30 v4.0
for all new development, and migrate existing workloads to
Azure Document Intelligence 2024-11-30 v4.0
before these retirement dates. For more information, see
Document Intelligence migration guide
.
Azure Document Intelligence in Foundry Tools is a cloud-based
Foundry Tools
service that you can use to build intelligent document processing solutions. Massive amounts of data, spanning various data types, are stored in forms and documents. You can use Azure Document Intelligence to effectively manage the speed at which data is collected and processed. Azure Document Intelligence is key to improved operations, informed data-driven decisions, and enlightened innovation. For information on region access, see
Product availability by region
.
| ✔️
Document analysis models
| ✔️
Prebuilt models
| ✔️
Custom models
|
Note
As part of Azure Content Understanding capabilities, Azure Document Intelligence provides high-accuracy and reliable deterministic extraction from structured documents.
Content Understanding also offers LLM-powered analyzers for complex, unstructured, and multimodal content.
Together, they make it easier to prepare data for intelligent agents and applications that can read, analyze, and respond to real-world content with precision and speed.
To compare both services and determine which best fits your scenario, see
Choose the right Azure AI tool for document processing
.
Document analysis models
Document analysis (general extraction) models enable text extraction from forms and documents and return structured business-ready content for your organization's action, use, or development.
Model
Description
Read
Extract printed and handwritten text.
Layout
Extract text, tables, and document structure.
Model
Description
Read
Extract printed and handwritten text.
Layout
Extract text, tables, and document structure.
General document
Extract text, structure, and key-value pairs.
Prebuilt models
You can use prebuilt models to add intelligent document processing to your apps and flows without having to train and build your own models.
Financial services and legal
Model
Description
Bank statement
Extract account information and details from bank statements.
Check
Extract relevant information from checks.
Contract
Extract agreement and party details.
Credit card
Extract payment card information.
Invoice
Extract customer and vendor details.
Pay stub
Extract pay stub details.
Receipt
Extract sales transaction details.
US tax
Model
Description
Unified US tax
Extract from any US tax forms supported.
US tax W-2
Extract taxable compensation details.
US tax 1098
Extract 1098 variation details.
US tax 1099
Extract 1099 variation details.
US tax 1040
Extract 1040 variation details.
US mortgage
Model
Description
US mortgage 1003
Extract loan application details.
US mortgage 1004
Extract information from appraisal.
US mortgage 1005
Extract information from validation of employment.
US mortgage 1008
Extract loan transmittal details.
US mortgage disclosure
Extract final closing loan terms.
Personal identification
Model
Description
Health insurance card
Extract insurance coverage details.
Identity
Extract verification details.
Marriage certificate
Extract certified marriage information.
Model
Description
Invoice
Extract customer and vendor details.
Receipt
Extract sales transaction details.
Identity
Extract identification and verification details.
Health insurance card
Extract health insurance details.
Business card
Extract business contact details.
Contract
Extract agreement and party details.
US tax W-2
Extract taxable compensation details.
US tax 1098
Extract 1098 variation details.
Custom models
Custom models are trained by using your labeled datasets to extract distinct data from forms and documents that are specific to your use cases. You can combine standalone custom models to create composed models.
Document field extraction models
✔️ Document field extraction models are trained to extract labeled fields from documents.
Model
Description
Custom neural
Extract data from mixed-type documents.
Custom template
Extract data from static layouts.
Custom composed
Extract data by using a collection of models.
Custom classification models
✔️ Custom classifiers identify document types before invoking an extraction model.
Model
Description
Custom classifier
Identify designated document types (classes) before invoking an extraction model.
Field type extraction
Document Intelligence returns extracted field values as strongly typed data. Each field in the extraction response carries a value type—such as
string
,
number
,
integer
,
date
,
time
,
phoneNumber
,
currency
, or
address
—that determines how the raw text is normalized and surfaced in the API response.
Prebuilt models
: For prebuilt models such as
prebuilt-invoice
or
prebuilt-receipt
, field schemas are defined and maintained by Microsoft. Common fields are mapped to specific types—for example,
InvoiceDate
is returned as a
date
type and
SubTotal
as a
currency
type—so normalization happens automatically without any configuration.
Custom models
: When you train a custom extraction model, you define the field schema. For each labeled field, you explicitly assign a type (
string
,
number
,
integer
, or
date
). The model then uses that type definition to auto-normalize extracted values during inference.
For the full field schema reference, see
Document Intelligence supported schema
.
Add-on capabilities
Document Intelligence supports optional features that you can enable or disable depending on the document extraction scenario:
ocr.highResolution
ocr.formula
ocr.font
ocr.barcode
Read model support for searchable PDF
Searchable PDF
queryFields
keyValuePairs
Analysis features
Model ID
Content extraction
Query fields
Paragraphs
Paragraph roles
Selection marks
Tables
Key/value pairs
Languages
Barcodes
Document analysis
Formulas*
Style font*
High resolution*
Searchable PDF
prebuilt-read
✓
✓
O
O
O
O
O
O
prebuilt-layout
✓
✓
✓
✓
✓
✓
O
O
O
O
O
O
prebuilt-contract
✓
✓
✓
✓
✓
O
O
✓
O
O
prebuilt-healthInsuranceCard.us
✓
✓
O
O
✓
O
O
O
prebuilt-idDocument
✓
✓
O
O
✓
O
O
O
prebuilt-invoice
✓
✓
✓
✓
O
O
O
✓
O
O
O
prebuilt-receipt
✓
✓
O
O
✓
O
O
O
prebuilt-marriageCertificate.us
✓
✓
✓
O
O
✓
O
O
O
prebuilt-creditCard
✓
✓
O
O
✓
O
O
O
prebuilt-check.us
✓
✓
O
O
✓
O
O
O
prebuilt-payStub.us
✓
✓
O
O
✓
O
O
O
prebuilt-bankStatement
✓
✓
O
O
✓
O
O
O
prebuilt-mortgage.us.1003
✓
✓
✓
O
O
✓
O
O
O
prebuilt-mortgage.us.1004
✓
✓
✓
O
O
✓
O
O
O
prebuilt-mortgage.us.1005
✓
✓
✓
O
O
✓
O
O
O
prebuilt-mortgage.us.1008
✓
✓
✓
O
O
✓
O
O
O
prebuilt-mortgage.us.closingDisclosure
✓
✓
✓
O
O
✓
O
O
O
prebuilt-tax.us
✓
✓
✓
O
O
✓
O
O
O
prebuilt-tax.us.w2
✓
✓
✓
O
O
✓
O
O
O
prebuilt-tax.us.w4
✓
✓
O
O
✓
O
O
O
prebuilt-tax.us.1040
(various)
✓
✓
✓
O
O
✓
O
O
O
prebuilt-tax.us.1095A
✓
✓
O
O
✓
O
O
O
prebuilt-tax.us.1095C
✓
✓
O
O
✓
O
O
O
prebuilt-tax.us.1098
✓
✓
✓
O
O
✓
O
O
O
prebuilt-tax.us.1098E
✓
✓
✓
O
O
✓
O
O
O
prebuilt-tax.us.1098T
✓
✓
✓
O
O
✓
O
O
O
prebuilt-tax.us.1099
(various)
✓
✓
✓
O
O
✓
O
O
O
prebuilt-tax.us.1099SSA
✓
✓
O
O
✓
O
O
O
{ customModelName }
✓
✓
✓
✓
✓
✓
O
O
✓
O
O
O
✓ - Enabled
O - Optional
* - Premium features incur extra costs
Models and development options
Use Document Intelligence to automate document processing in applications and workflows, enhance data-driven strategies, and enrich document search capabilities. Use the links in the table to learn more about each model and browse development options.
Read
Model ID
Description
Automation use cases
Development options
prebuilt-read
● Extract text from documents.
●
Extract data
.
● Digitizing any document
● Compliance and auditing
● Processing handwritten notes before translation
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
Layout
Model ID
Description
Automation use cases
Development options
prebuilt-layout
● Extract text and layout information from documents.
●
Extract data
.
● Document indexing and retrieval by structure
● Financial and medical report analysis
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
General document (deprecated in 2023-10-31-preview)
Model ID
Description
Automation use cases
Development options
prebuilt-document
● Extract text, layout, and key/value pairs from documents.
●
Extract data and fields
.
● Key/value pair extraction
● Form processing
● Survey data collection and analysis
●
Document Intelligence Studio
●
REST API
Return to model types
Invoice
Model ID
Description
Automation use cases
Development options
prebuilt-invoice
● Extract key information from invoices.
●
Extract data and fields
.
● Accounts payable processing
● Automated tax recording and reporting
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
Receipt
Model ID
Description
Automation use cases
Development options
prebuilt-receipt
● Extract key information from receipts.
●
Extract data and fields
.
● Receipt model v3.0 supports processing of single-page hotel receipts.
● Expense management
● Consumer behavior data analysis
● Customer loyalty program
● Merchandise return processing
● Automated tax recording and reporting
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
Identity (ID)
Model ID
Description
Automation use cases
Development options
prebuilt-idDocument
● Extract key information from passports and ID cards.
●
Document types
.
● Extract  endorsements, restrictions, and vehicle classifications from US driver's licenses.
● Know your customer (KYC) financial services guidelines compliance
● Medical account management
● Identity checkpoints and gateways
● Hotel registration
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
Check
Model ID
Description
Automation use cases
Development options
prebuilt-check
● Extract key information from checks.
●
Extract data and fields
.
● Credit management
● Automated lender management
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
Pay stub
Model ID
Description
Automation use cases
Development options
prebuilt-paystub
● Extract key information from pay stubs.
●
Extract data and fields
.
● Employee payroll detail verification
● Fraud detection for employment
● Automated tax processing
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
Bank statement
Model ID
Description
Automation use cases
Development options
prebuilt-bankStatement
● Extract key information from bank statements.
●
Extract data and fields
.
● Tax processing use cases
● Automated accounting management
● Credit-debit management
● Loan documentation processing
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
Health insurance card
Model ID
Description
Automation use cases
Development options
prebuilt-healthInsuranceCard.us
● Extract key information from US health insurance cards.
●
Extract data and fields
.
● Coverage and eligibility verification
● Predictive modeling
● Value-based analytics
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
Contract model
Model ID
Description
Development options
prebuilt-contract
● Extract contract agreement and party details.
●
Extract data and fields
.
●
Document Intelligence Studio
●
REST API
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
Credit card model
Model ID
Description
Development options
prebuilt-creditCard
● Extract contract agreement and party details.
●
Extract data and fields
.
●
Document Intelligence Studio
●
REST API
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
Marriage certificate model
Model ID
Description
Development options
prebuilt-marriageCertificate.us
● Extract contract agreement and party details.
●
Extract data and fields
.
●
Document Intelligence Studio
●
REST API
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
US mortgage 1003 form
Model ID
Description
Automation use cases
Development options
prebuilt-mortgage.us.1003
● Extract key information from 1003 loan applications.
●
Extract data and fields
.
Fannie Mae and Freddie Mac documentation requirements
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
US mortgage 1004 form
Model ID
Description
Automation use cases
Development options
prebuilt-mortgage.us.1004
● Extract key information from 1004 appraisals.
●
Extract data and fields
.
● Fannie Mae and Freddie Mac documentation requirements
● Uniform Residential Appraisal report to help lender/client with the market value of the subject property
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
US mortgage 1005 form
Model ID
Description
Automation use cases
Development options
prebuilt-mortgage.us.1005
● Extract key information from 1005 validation of employment.
●
Extract data and fields
.
● Fannie Mae and Freddie Mac documentation requirements
● Verification of employment document to determine the qualification as a prospective mortgagor
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
US mortgage 1008 form
Model ID
Description
Automation use cases
Development options
prebuilt-mortgage.us.1008
● Extract key information from Uniform Underwriting and Transmittal Summary.
●
Extract data and fields
. Loan underwriting processing by using summary data
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
US mortgage disclosure form
Model ID
Description
Automation use cases
Development options
prebuilt-mortgage.us.closingDisclosure
● Extract key information from Uniform Underwriting and Transmittal Summary.
●
Extract data and fields
.
Mortgage loan final details requirements
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
US tax W-2 model
Model ID
Description
Automation use cases
Development options
prebuilt-tax.us.w2
Extract key information from IRS US W2 tax forms (years 2018-2021).
● Automated tax document management
● Mortgage loan application processing
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
US tax 1098 (and variations) forms
Model ID
Description
Development options
prebuilt-tax.us.1098{
variation
}
Extract key information from 1098-form variations.
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
US tax 1099 (and variations) forms
Model ID
Description
Development options
prebuilt-tax.us.1099{
variation
}
Extract information from 1099-form variations.
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
US tax 1040 (and variations) forms
Model ID
Description
Development options
prebuilt-tax.us.1040{
variation
}
Extract information from 1040-form variations.
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Unified US tax forms
Model ID
Description
Development options
prebuilt-tax.us
Extract information from any of the supported US tax forms.
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Business card
Model ID
Description
Automation use cases
Development options
prebuilt-businessCard
● Extract key information from business cards.
●
Extract data and fields
.
Sales lead and marketing management
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript
Return to model types
Custom model overview
About
Description
Automation use cases
Development options
Custom model
Extract information from forms and documents into structured data based on a model created from a set of representative training document sets.
Extract distinct data from forms and documents specific to your business and use cases.
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Java SDK
●
JavaScript SDK
●
Python SDK
Return to custom model types
Custom neural
Note
To train a custom neural model, set the
buildMode
property to
neural
. For more information, see
Training a neural model
.
About
Description
Automation use cases
Development options
Custom Neural model
Extract labeled data from structured (surveys, questionnaires), semistructured (invoices, purchase orders), and unstructured documents (contracts, letters).
Extract text data, checkboxes, and tabular fields from structured and unstructured documents.
Document Intelligence Studio
●
REST API
●
C# SDK
●
Java SDK
●
JavaScript SDK
●
Python SDK
Return to custom model types
Custom template
Note
To train a custom template model, set the
buildMode
property to
template
. For more information, see
Training a template model
.
About
Description
Automation use cases
Development options
Custom Template model
Extract labeled values and fields from structured and semistructured documents.
Extract key data from highly structured documents with defined visual templates or common visual layouts and forms.
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Python SDK
●
Java SDK
●
JavaScript SDK
Return to custom model types
Custom composed
About
Description
Automation use cases
Development options
Composed custom models
A composed model is created by taking a collection of custom models and assigning them to a single model built from your form types.
Useful when you train several models and want to group them to analyze similar form types, like purchase orders
●
Document Intelligence Studio
●
REST API
●
C# SDK
●
Java SDK
●
JavaScript SDK
●
Python SDK
Return to custom model types
Custom classification model
About
Description
Automation use cases
Development options
Composed classification model
Custom classification models combine layout and language features to detect, identify, and classify documents within an input file.
● A loan application package that contains application forms, pay slips, and bank statements
● A collection of scanned invoices
●
Document Intelligence Studio
●
REST API
Return to custom model types
Azure Document Intelligence is a cloud-based
Foundry Tools
for developers to build intelligent document processing solutions. Azure Document Intelligence applies optical character recognition (OCR) based on machine learning along with document understanding technologies to extract text, tables, structure, and key/value pairs from documents. You can also label and train custom models to automate data extraction from structured, semistructured, and unstructured documents. To learn more about each model, see the concepts articles.
Model type
Model name
Document analysis model
●
Layout analysis model
Prebuilt models
●
Invoice model
●
Receipt model
●
Identity document (ID) model
●
Business card model
Custom models
●
Custom model
●
Composed model
This content applies to:
v2.1
|
Latest version:
v4.0 (GA)
Document Intelligence models and development options
Tip
For an enhanced experience and advanced model quality, try the
Document Intelligence Studio
for v4.0:
The Studio supports any model trained with v2.1 labeled data.
For more information about migrating from v2.1 to v4.0, see the
Document Intelligence migration guide
.
Note
: The v3.0 API (
2022-08-31
) reaches end of support on March 30, 2029. Migrate v3.0 workloads to v4.0 before that date.
To learn more about each model and browse the API references, use the links in the following table.
Model
Description
Development options
Layout analysis
Extraction and analysis of text, selection marks, tables, and bounding box coordinates, from forms and documents
●
Document Intelligence labeling tool
●
REST API
●
Client-library SDK
●
Document Intelligence Docker container
Custom model
Extraction and analysis of data from forms and documents specific to distinct business data and use cases
●
Document Intelligence labeling tool
●
REST API
●
Sample Labeling Tool
●
Document Intelligence Docker container
Invoice model
Automated data processing and extraction of key information from sales invoices
●
Document Intelligence labeling tool
●
REST API
●
Client-library SDK
●
Document Intelligence Docker container
Receipt model
Automated data processing and extraction of key information from sales receipts.
●
Document Intelligence labeling tool
●
REST API
●
Client-library SDK
●
Document Intelligence Docker container
Identity document (ID) model
Automated data processing and extraction of key information from US driver's licenses and international passports
●
Document Intelligence labeling tool
●
REST API
●
Client-library SDK
●
Document Intelligence Docker container
Business card model
Automated data processing and extraction of key information from business cards
●
Document Intelligence labeling tool
●
REST API
●
Client-library SDK
●
Document Intelligence Docker container
Data privacy and security
As with all Foundry Tools, developers who use Document Intelligence should be aware of Microsoft policies on customer data. For more information, see
Data, privacy, and security for Document Intelligence
.
Version support and retirement
The following table summarizes Document Intelligence API version support:
Version
Status
End of support
v4.0 (2024-11-30)
GA — current
No announced date
v3.1 (2023-07-31)
GA — previous
No announced date
v3.0 (2022-08-31)
GA — retiring
March 30, 2029
v2.1
GA — retiring
September 15, 2027
To avoid production disruption, migrate to v4.0 before the retirement dates above. For migration guidance, see the
Document Intelligence migration guide
.
Related content
Choose a Document Intelligence model
.
Process your own forms and documents with
Document Intelligence Studio
.
Finish a
Document Intelligence quickstart
, and then create a document processing app in the development language of your choice.
Process your own forms and documents with the
Document Intelligence Sample Labeling tool
.
Finish a
Document Intelligence quickstart
, and then create a document processing app in the development language of your choice.
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