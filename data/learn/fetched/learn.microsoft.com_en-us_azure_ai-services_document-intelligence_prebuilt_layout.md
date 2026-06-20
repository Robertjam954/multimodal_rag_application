<!-- source: https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/layout -->

# What is the Document Intelligence layout model?

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
What is the Document Intelligence layout model?
Summarize this article for me
This content applies to:
v4.0 (GA)
|
Prior versions:
v3.1 (GA)
v3.0 (retiring)
v2.1 (retiring)
The Azure Document Intelligence in Foundry Tools layout model is an advanced document-analysis API based on machine learning. The model is available in the Document Intelligence cloud. You can use it to take documents in various formats and return structured data representations of the documents. The model combines an enhanced version of the powerful
optical character recognition (OCR)
capabilities with deep learning models to extract text, tables, selection marks, and document structure.
Document structure layout analysis
Document structure layout analysis is the process of analyzing a document to extract regions of interest and their interrelationships. The goal is to extract text and structural elements from the page to build better semantic understanding models. There are two types of roles in a document layout:
Geometric roles
: Text, tables, figures, and selection marks are examples of geometric roles.
Logical roles
: Titles, headings, and footers are examples of logical roles of texts.
The following illustration shows the typical components in an image of a sample page.
Development options
Document Intelligence v4.0: 2024-11-30 (GA) supports the following tools, applications, and libraries.
Feature
Resources
Model ID
Layout model
•
Document Intelligence Studio
•
REST API
•
C# SDK
•
Python SDK
•
Java SDK
•
JavaScript SDK
prebuilt-layout
Supported languages
For a complete list of supported languages, see
Language support: Document analysis models
.
Supported file types
Document Intelligence v4.0: 2024-11-30 (GA) layout model supports the following file formats:
Model
PDF
Image:
JPEG/JPG, PNG, BMP, TIFF, HEIF
Office:
Word (DOCX), Excel (XLS), PowerPoint (PPTX), HTML
Layout
✔
✔
✔
Input requirements
Photos and scans
: For best results, provide one clear photo or high-quality scan per document.
PDFs and TIFFs
: For PDFs and TIFFs, up to 2,000 pages can be processed. (With a free-tier subscription, only the first two pages are processed.)
Password locks
: If your PDFs are password-locked, you must remove the lock before submission.
File size
: The file size for analyzing documents is 500 MB for the paid (S0) tier and 4 MB for the free (F0) tier.
Image dimensions
: The image dimensions must be between 50 pixels x 50 pixels and 10,000 pixels x 10,000 pixels.
Text height
: The minimum height of the text to be extracted is 12 pixels for a 1024 x 768 pixel image. This dimension corresponds to about 8-point text at 150 dots per inch.
Custom model training
: The maximum number of pages for training data is 500 for the custom template model and 50,000 for the custom neural model.
Custom extraction model training
: The total size of training data is 50 MB for the template model and 1 GB for the neural model.
Custom classification model training
: The total size of training data is 1 GB with a maximum of 10,000 pages. For 2024-11-30 (GA), the total size of training data is 2 GB with a maximum of 10,000 pages.
Office file types (DOCX, XLSX, PPTX)
: The maximum string length limit is 8 million characters.
For more information on model usage, quotas, and service limits, see
Service limits
.
Get started with the layout model
See how data, including text, tables, table headers, selection marks, and structure information, is extracted from documents by using Document Intelligence. You need the following resources:
An Azure subscription. You can
create one for free
.
A
Document Intelligence instance
in the Azure portal. You can use the free pricing tier (F0) to try the service. After your resource deploys, select
Go to resource
to get your key and endpoint.
After you retrieve your key and endpoint, use the following development options to build and deploy your Document Intelligence applications.
REST API
Client libraries
Document Intelligence Studio
Document Intelligence REST API
Get started: Document Intelligence Studio
C# SDK
Python SDK
Java SDK
JavaScript
Document Intelligence Studio
Get started: Document Intelligence Studio
Data extraction
The layout model extracts structural elements from your documents. The following structural elements are described in the remainder of this article along with guidance on how to extract them from your document input:
Pages
Paragraphs
Text, lines, and words
Selection marks
Tables
Output response to markdown
Figures
Sections
Run the sample layout document analysis within
Document Intelligence Studio
. Then go to the results tab and access the full JSON output.
Pages
The
pages
collection is a list of pages within the document. Each page is represented sequentially within the document and includes the orientation angle, which indicates if the page is rotated, and the width and height (dimensions in pixels). The page units in the model output are computed as shown in the following table.
File format
Computed page unit
Total pages
Images (JPEG/JPG, PNG, BMP, HEIF)
Each image = 1 page unit.
Total images
PDF
Each page in the PDF = 1 page unit.
Total pages in the PDF
TIFF
Each image in the TIFF = 1 page unit.
Total images in the TIFF
Word (DOCX)
Up to 3,000 characters = 1 page unit. Embedded or linked images aren't supported.
Total pages of up to 3,000 characters each
Excel (XLSX)
Each worksheet = 1 page unit. Embedded or linked images aren't supported.
Total worksheets
PowerPoint (PPTX)
Each slide = 1 page unit. Embedded or linked images aren't supported.
Total slides
HTML
Up to 3,000 characters = 1 page unit. Embedded or linked images aren't supported.
Total pages of up to 3,000 characters each
Sample code
Output
```
# Analyze pages.
for page in result.pages:
print(f"----Analyzing layout from page #{page.page_number}----")
print(f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}")


```
View samples on GitHub.
```
"pages": [
    {
        "pageNumber": 1,
        "angle": 0,
        "width": 915,
        "height": 1190,
        "unit": "pixel",
        "words": [],
        "lines": [],
        "spans": []
    }
]

```
Extract selected pages
For large multipage documents, use the
pages
query parameter to indicate specific page numbers or page ranges for text extraction.
Paragraphs
The layout model extracts all identified blocks of text in the
paragraphs
collection as a top-level object under
analyzeResults
. Each entry in this collection represents a text block and includes the extracted text as
content
and the bounding
polygon
coordinates. The
spans
information points to the text fragment within the top-level
content
property that contains the full text from the document.
```

"paragraphs": [
    {
        "spans": [],
        "boundingRegions": [],
        "content": "While healthcare is still in the early stages of its Al journey, we are seeing pharmaceutical and other life sciences organizations making major investments in Al and related technologies.\" TOM LAWRY | National Director for Al, Health and Life Sciences | Microsoft"
    }
]

```
Paragraph roles
The new page object detection based on machine learning extracts logical roles like titles, section headings, page headers, page footers, and more. The Document Intelligence layout model assigns certain text blocks in the
paragraphs
collection with their specialized role or type predicted by the model.
It's best to use paragraph roles with unstructured documents to help understand the layout of the extracted content for a richer semantic analysis. The following paragraph roles are supported.
Predicted role
Description
Supported file types
title
The main headings on the page
PDF, Image, DOCX, PPTX, XLSX, HTML
sectionHeading
One or more subheadings on the page
PDF, Image, DOCX, XLSX, HTML
footnote
Text near the bottom of the page
PDF, Image
pageHeader
Text near the top edge of the page
PDF, Image, DOCX
pageFooter
Text near the bottom edge of the page
PDF, Image, DOCX, PPTX, HTML
pageNumber
Page number
PDF, Image
```
{
    "paragraphs": [
                {
                    "spans": [],
                    "boundingRegions": [],
                    "role": "title",
                    "content": "NEWS TODAY"
                },
                {
                    "spans": [],
                    "boundingRegions": [],
                    "role": "sectionHeading",
                    "content": "Mirjam Nilsson"
                }
    ]
}


```
Text, lines, and words
The document layout model in Document Intelligence extracts print and handwritten-style text as
lines
and
words
. The
styles
collection includes any handwritten style for lines, if detected, along with the spans that point to the associated text. This feature applies to
supported handwritten languages
.
For Microsoft Word, Excel, PowerPoint, and HTML, the Document Intelligence v4.0 2024-11-30 (GA) layout model extracts all embedded text as is. Texts are extracted as words and paragraphs. Embedded images aren't supported.
Sample code
Output
```
# Analyze lines.
if page.lines:
    for line_idx, line in enumerate(page.lines):
    words = get_words(page, line)
    print(
        f"...Line # {line_idx} has word count {len(words)} and text '{line.content}' "
        f"within bounding polygon '{line.polygon}'"
    )

    # Analyze words.
    for word in words:
        print(f"......Word '{word.content}' has a confidence of {word.confidence}")


```
View samples on GitHub.
```
"words": [
    {
        "content": "While",
        "polygon": [],
        "confidence": 0.997,
        "span": {}
    },
],
"lines": [
    {
        "content": "While healthcare is still in the early stages of its Al journey, we",
        "polygon": [],
        "spans": [],
    }
]

```
Handwritten style for text lines
The response includes whether each text line is in a handwritten style or not, along with a confidence score. For more information, see
Handwritten language support
. The following example shows an example JSON snippet.
```
"styles": [
{
    "confidence": 0.95,
    "spans": [
    {
        "offset": 509,
        "length": 24
    }
    "isHandwritten": true
    ]
}

```
If you enable the
font/style add-on capability
, you also get the font/style result as part of the
styles
object.
Selection marks
The layout model also extracts selection marks from documents. Extracted selection marks appear within the
pages
collection for each page. They include the bounding
polygon
,
confidence
, and selection
state
(
selected/unselected
). The text representation (that is,
:selected:
and
:unselected
) is also included as the starting index (
offset
) and
length
that references the top-level
content
property that contains the full text from the document.
Sample code
Output
```
# Analyze selection marks.
if page.selection_marks:
    for selection_mark in page.selection_marks:
        print(
            f"Selection mark is '{selection_mark.state}' within bounding polygon "
            f"'{selection_mark.polygon}' and has a confidence of {selection_mark.confidence}"
        )


```
View samples on GitHub.
```
{
    "selectionMarks": [
        {
            "state": "unselected",
            "polygon": [],
            "confidence": 0.995,
            "span": {
                "offset": 1421,
                "length": 12
            }
        }
    ]
}

```
Tables
Extracting tables is a key requirement for processing documents that contain large volumes of data typically formatted as tables. The layout model extracts tables in the
pageResults
section of the JSON output. Extracted table information includes the number of columns and rows, row span, and column span.
Each cell with its bounding polygon is output along with information whether the area is recognized as
columnHeader
or not. The model supports extracting tables that are rotated. Each table cell contains the row and column index and bounding polygon coordinates. For the cell text, the model outputs the
span
information that contains the starting index (
offset
). The model also outputs the
length
within the top-level content that contains the full text from the document.
Here are a few factors to consider when you use the Document Intelligence bale extraction capability:
Is the data that you want to extract presented as a table, and is the table structure meaningful?
Can the data fit in a two-dimensional grid if the data isn't in a table format?
Do your tables span multiple pages? If so, to avoid having to label all the pages, split the PDF into pages before you send it to Document Intelligence. After the analysis, post-process the pages to a single table.
See
Tabular fields
if you create custom models. Dynamic tables have a variable number of rows for each column. Fixed tables have a constant number of rows for each column.
Note
Table analysis isn't supported if the input file is XLSX. For 2024-11-30 (GA), the bounding regions for figures and tables cover only the core content and exclude the associated caption and footnotes.
Sample code
Output
```
if result.tables:
    for table_idx, table in enumerate(result.tables):
        print(f"Table # {table_idx} has {table.row_count} rows and " f"{table.column_count} columns")
        if table.bounding_regions:
            for region in table.bounding_regions:
                print(f"Table # {table_idx} location on page: {region.page_number} is {region.polygon}")
        # Analyze cells.
        for cell in table.cells:
            print(f"...Cell[{cell.row_index}][{cell.column_index}] has text '{cell.content}'")
            if cell.bounding_regions:
                for region in cell.bounding_regions:
                print(f"...content on page {region.page_number} is within bounding polygon '{region.polygon}'")


```
View samples on GitHub.
```
{
    "tables": [
        {
            "rowCount": 9,
            "columnCount": 4,
            "cells": [
                {
                    "kind": "columnHeader",
                    "rowIndex": 0,
                    "columnIndex": 0,
                    "columnSpan": 4,
                    "content": "(In millions, except earnings per share)",
                    "boundingRegions": [],
                    "spans": []
                    },
            ]
        }
    ]
}


```
Output response to Markdown format
The layout API can output the extracted text in Markdown format. Use the
outputContentFormat=markdown
to specify the output format in Markdown. The Markdown content is output as part of the
content
section.
Note
For v4.0 2024-11-30 (GA), the representation of tables is changed to HTML tables to enable rendering of items like merged cells and multirow headers. Another related change is to use the Unicode checkbox characters ☒ and ☐ for selection marks instead of
:selected:
and
:unselected:
. This update means that the content of selection-mark fields contains
:selected:
even though their spans refer to Unicode characters in the top-level span. For a full definition of Markdown elements, see
Markdown output format
.
Sample code
Output
```
document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
poller = document_intelligence_client.begin_analyze_document(
    "prebuilt-layout",
    AnalyzeDocumentRequest(url_source=url),
    output_content_format=ContentFormat.MARKDOWN,
)


```
View samples on GitHub.
```
PageHeader="This is the header of the document."

This is title
===
# 1\. Text
Latin refers to an ancient Italic language originating in the region of Latium in ancient Rome.
# 2\. Page Objects
## 2.1 Table
Here's a sample table below, designed to be simple for easy understand and quick reference.
| Name | Corp | Remark |
| - | - | - |
| Foo | | |
| Bar | Microsoft | Dummy |
Table 1: This is a dummy table
## 2.2. Figure
<figure>
<figcaption>

Figure 1: Here is a figure with text
</figcaption>

![](figures/0)
FigureContent="500 450 400 400 350 250 200 200 200- Feb"
</figure>

# 3\. Others
Al Document Intelligence is an Al service that applies advanced machine learning to extract text, key-value pairs, tables, and structures from documents automatically and accurately:
    :selected:
clear
    :selected:
precise
    :unselected:
vague
    :selected:
coherent
    :unselected:
Incomprehensible
Turn documents into usable data and shift your focus to acting on information rather than compiling it. Start with prebuilt models or create custom models tailored to your documents both on premises and in the cloud with the Al Document Intelligence studio or SDK.
Learn how to accelerate your business processes by automating text extraction with Al Document Intelligence. This webinar features hands-on demos for key use cases such as document processing, knowledge mining, and industry-specific Al model customization.
PageFooter="This is the footer of the document."
PageFooter="1 | Page"

```
Figures
Figures (charts and images) in documents play a crucial role in complementing and enhancing the textual content. They provide visual representations that aid in the understanding of complex information. The
figures
object detected by the layout model has key properties like:
boundingRegions
: The spatial locations of the figure on the document pages, including the page number and the polygon coordinates that outline the figure's boundary.
spans
: The text spans related to the figure that specify their offsets and lengths within the document's text. This connection helps in associating the figure with its relevant textual context.
elements
: The identifiers for text elements or paragraphs within the document that are related to or describe the figure.
caption
: The description if there is one.
When
output=figures
is specified during the initial analyze operation, the service generates cropped images for all detected figures that can be accessed via
/analyeResults/{resultId}/figures/{figureId}
. The
FigureId
value is the ID included in each figure object, following an undocumented convention of
{pageNumber}.{figureIndex}
where
figureIndex
resets to one per page.
For v4.0 2024-11-30 (GA), the bounding regions for figures and tables cover only the core content and exclude the associated caption and footnotes.
Sample code
Output
```
# Analyze figures.
if result.figures:
    for figures_idx,figures in enumerate(result.figures):
        print(f"Figure # {figures_idx} has the following spans:{figures.spans}")
        for region in figures.bounding_regions:
            print(f"Figure # {figures_idx} location on page:{region.page_number} is within bounding polygon '{region.polygon}'")

```
View samples on GitHub.
```
{
    "figures": [
        {
        "id": "{figureId}",
        "boundingRegions": [],
        "spans": [],
        "elements": [
            "/paragraphs/15",
            ...
        ],
        "caption": {
            "content": "Here is a figure with some text",
            "boundingRegions": [],
            "spans": [],
            "elements": [
            "/paragraphs/15"
            ]
        }
        }
    ]
}

```
Sections
Hierarchical document structure analysis is pivotal in organizing, comprehending, and processing extensive documents. This approach is vital for semantically segmenting long documents to boost comprehension, facilitate navigation, and improve information retrieval. The advent of
retrieval-augmented generation (RAG)
in document-generative AI underscores the significance of hierarchical document structure analysis.
The layout model supports sections and subsections in the output, which identifies the relationship of sections and objects within each section. The hierarchical structure is maintained in
elements
for each section. You can use the
output response to Markdown format
to easily get the sections and subsections in Markdown.
Sample code
Output
```
document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
poller = document_intelligence_client.begin_analyze_document(
    "prebuilt-layout",
    AnalyzeDocumentRequest(url_source=url),
    output_content_format=ContentFormat.MARKDOWN,
)


```
View samples on GitHub.
```
{
    "sections": [
        {
        "spans": [],
        "elements": [
            "/paragraphs/0",
            "/sections/1",
            "/sections/2",
            "/sections/5"
        ]
        },
...
}

```
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
Important
Azure Document Intelligence v3.0 API (
2022-08-31
) reaches end of support on
March 30, 2029
. To avoid production disruption, use
Azure Document Intelligence 2024-11-30 v4.0
for all new development, and migrate existing workloads to
Azure Document Intelligence 2024-11-30 v4.0
before this date. For migration guidance, see the
Document Intelligence migration guide
.
This content applies to:
v2.1
|
Latest version:
v4.0 (GA)
The Document Intelligence layout model is an advanced document-analysis API. The model is based on machine learning and is available in the Document Intelligence cloud. You can use it to take documents in various formats and return structured data representations of the documents. It combines an enhanced version of the powerful
OCR
capabilities with deep learning models. You can use it to extract text, tables, selection marks, and document structure.
Document layout analysis
Document structure layout analysis is the process of analyzing a document to extract regions of interest and their interrelationships. The goal is to extract text and structural elements from the page to build better semantic understanding models. There are two types of roles in a document layout:
Geometric roles
: Text, tables, figures, and selection marks are examples of geometric roles.
Logical roles
: Titles, headings, and footers are examples of logical roles of texts.
The following illustration shows the typical components in an image of a sample page.
Supported languages and locales
For a complete list of supported languages, see
Language support: Document analysis models
.
Document Intelligence v2.1 supports the following tools, applications, and libraries.
Feature
Resources
Layout model
•
Document Intelligence labeling tool
•
REST API
•
Client-library SDK
•
Document Intelligence Docker container
Input guidance
Supported file formats:
Model
PDF
Image:
JPEG/JPG, PNG, BMP, TIFF, HEIF
Office:
Word (DOCX), Excel (XLSX), PowerPoint (PPTX), HTML
Read
✔
✔
✔
Layout
✔
✔
General document
✔
✔
Prebuilt
✔
✔
Custom extraction
✔
✔
Custom classification
✔
✔
✔
Photos and scans
: For best results, provide one clear photo or high-quality scan per document.
PDFs and TIFFs
: For PDFs and TIFFs, up to 2,000 pages can be processed with a free-tier subscription. Only the first two pages are processed.
File size
: The file size for analyzing documents is 500 MB for the paid (S0) tier and 4 MB for the free (F0) tier.
Image dimensions
: The image dimensions must be between 50 pixels x 50 pixels and 10,000 pixels x 10,000 pixels.
Password locks
: If your PDFs are password-locked, you must remove the lock before submission.
Text height
: The minimum height of the text to be extracted is 12 pixels for a 1024 x 768 pixel image. This dimension corresponds to about 8-point text at 150 dots per inch.
Custom model training
: The maximum number of pages for training data is 500 for the custom template model and 50,000 for the custom neural model.
Custom extraction model training
: The total size of training data is 50 MB for the template model and 1 GB for the neural model.
Custom classification model training
: The total size of training data is 1 GB with a maximum of 10,000 pages. For 2024-11-30 (GA), the total size of training data is 2 GB with a maximum of 10,000 pages.
Office file types (DOCX, XLSX, PPTX)
: The maximum string length limit is 8 million characters.
Input guide
Supported file formats
: JPEG, PNG, PDF, and TIFF.
Supported number of pages
: For PDF and TIFF, up to 2,000 pages are processed. For free tier subscribers, only the first two pages are processed.
Supported file size
: The file size must be less than 50 MB, and the dimensions must be at least 50 x 50 pixels and at most 10,000 x 10,000 pixels.
Get started
You can use Document Intelligence to extract data such as text, tables, table headers, selection marks, and structure information from documents. You need the following resources:
An Azure subscription. You can
create one for free
.
A
Document Intelligence instance
in the Azure portal. You can use the free pricing tier (F0) to try the service. After your resource deploys, select
Go to resource
to get your key and endpoint.
After you retrieve your key and endpoint, you can use the following development options to build and deploy your Document Intelligence applications.
Note
Document Intelligence Studio is available with v3.0 APIs and later versions.
REST API
Client libraries
Document Intelligence Studio
2023-07-31` GA (v3.1)
2022-08-31` GA (v3.0)
C# SDK
Java SDK
JavaScript
Python SDK
Document Intelligence Studio
Get started: Document Intelligence Studio
REST API
Document Intelligence v2.1 (Form Recognizer)
Document Intelligence Sample Labeling tool
Go to the
Document Intelligence Sample Labeling tool
.
On the sample tool home page, select
Use Layout to get text, tables and selection marks
.
In the
Document Intelligence service endpoint
field, paste the endpoint that you obtained with your Document Intelligence subscription.
In the
key
field, paste the key that you obtained from your Document Intelligence resource.
In the
Source
field, select
URL
from the dropdown menu. You can use the sample document:
Sample document
.
Select
Fetch
.
Select
Run Layout
. The Document Intelligence Sample Labeling tool calls the Analyze Layout API to analyze the document.
View the results. See the highlighted extracted text, detected selection marks, and detected tables.
Document Intelligence v2.1 supports the following tools, applications, and libraries.
Feature
Resources
Layout API
•
Document Intelligence labeling tool
•
REST API
•
Client-library SDK
•
Document Intelligence Docker container
Extract data
The layout model extracts structural elements from your documents. The structural elements are described here, and the following guidance shows you how to extract them from your document input.
Page
Paragraph
Text, line, and word
Selection mark
Table
Annotations
Extract data
The layout model extracts structural elements from your documents. The structural elements are described here, and the following guidance shows you how to extract them from your document input.
Page
Paragraph
Text, line, and word
Selection mark
Table
Natural reading order
Select page number or range
Page
The
pages
collection is a list of pages within the document. Each page is represented sequentially within the document and includes the orientation angle that indicates if the page is rotated and the width and height (dimensions in pixels). The page units in the model output are computed as shown in the following table.
File format
Computed page unit
Total pages
Images (JPEG/JPG, PNG, BMP, HEIF)
Each image = 1 page unit.
Total images
PDF
Each page in the PDF = 1 page unit.
Total pages in the PDF
TIFF
Each image in the TIFF = 1 page unit.
Total images in the TIFF
Word (DOCX)
Up to 3,000 characters = 1 page unit. Embedded or linked images aren't supported.
Total pages of up to 3,000 characters each
Excel (XLSX)
Each worksheet = 1 page unit. Embedded or linked images aren't supported.
Total worksheets
PowerPoint (PPTX)
Each slide = 1 page unit. Embedded or linked images aren't supported.
Total slides
HTML
Up to 3,000 characters = 1 page unit. Embedded or linked images aren't supported.
Total pages of up to 3,000 characters each
```
"pages": [
    {
        "pageNumber": 1,
        "angle": 0,
        "width": 915,
        "height": 1190,
        "unit": "pixel",
        "words": [],
        "lines": [],
        "spans": []
    }
]

```
Sample code
Output
```
# Analyze pages.
for page in result.pages:
    print(f"----Analyzing layout from page #{page.page_number}----")
    print(
        f"Page has width: {page.width} and height: {page.height}, measured with unit: {page.unit}"
    )


```
View samples on GitHub.
```
"pages": [
    {
        "pageNumber": 1,
        "angle": 0,
        "width": 915,
        "height": 1190,
        "unit": "pixel",
        "words": [],
        "lines": [],
        "spans": []
    }
]

```
Extract selected pages from documents
For large multipage documents, use the
pages
query parameter to indicate specific page numbers or page ranges for text extraction.
Paragraph
The layout model extracts all identified blocks of text in the
paragraphs
collection as a top-level object under
analyzeResults
. Each entry in this collection represents a text block and includes the extracted text as
content
and the bounding
polygon
coordinates. The
span
information points to the text fragment within the top-level
content
property that contains the full text from the document.
```

"paragraphs": [
    {
        "spans": [],
        "boundingRegions": [],
        "content": "While healthcare is still in the early stages of its Al journey, we are seeing pharmaceutical and other life sciences organizations making major investments in Al and related technologies.\" TOM LAWRY | National Director for Al, Health and Life Sciences | Microsoft"
    }
]

```
Paragraph role
The new page object detection based on machine learning extracts logical roles like titles, section headings, page headers, page footers, and more. The Document Intelligence layout model assigns certain text blocks in the
paragraphs
collection with their specialized role or type predicted by the model. It's best to use paragraph roles with unstructured documents to help understand the layout of the extracted content for a richer semantic analysis. The following paragraph roles are supported.
Predicted role
Description
Supported file types
title
The main headings in the page
PDF, Image, DOCX, PPTX, XLSX, HTML
sectionHeading
One or more subheadings on the page
PDF, Image, DOCX, XLSX, HTML
footnote
Text near the bottom of the page
PDF, Image
pageHeader
Text near the top edge of the page
PDF, Image, DOCX
pageFooter
Text near the bottom edge of the page
PDF, Image, DOCX, PPTX, HTML
pageNumber
Page number
PDF, Image
```
{
    "paragraphs": [
                {
                    "spans": [],
                    "boundingRegions": [],
                    "role": "title",
                    "content": "NEWS TODAY"
                },
                {
                    "spans": [],
                    "boundingRegions": [],
                    "role": "sectionHeading",
                    "content": "Mirjam Nilsson"
                }
    ]
}


```
Text, line, and word
The document layout model in Document Intelligence extracts print and handwritten-style text as lines and words. The
styles
collection includes any handwritten style for lines if detected along with the spans that point to the associated text. This feature applies to
supported handwritten languages
.
For Word, Excel, PowerPoint, and HTML, the Document Intelligence v4.0 2024-11-30 (GA) layout model extracts all embedded text as is. Texts are extracted as words and paragraphs. Embedded images aren't supported.
```
"words": [
    {
        "content": "While",
        "polygon": [],
        "confidence": 0.997,
        "span": {}
    },
],
"lines": [
    {
        "content": "While healthcare is still in the early stages of its Al journey, we",
        "polygon": [],
        "spans": [],
    }
]

```
Sample code
Output
```
# Analyze lines.
for line_idx, line in enumerate(page.lines):
    words = line.get_words()
    print(
        f"...Line # {line_idx} has word count {len(words)} and text '{line.content}' "
        f"within bounding polygon '{format_polygon(line.polygon)}'"
    )

    # Analyze words.
    for word in words:
        print(
            f"......Word '{word.content}' has a confidence of {word.confidence}"
        )


```
View samples on GitHub.
```
"words": [
    {
        "content": "While",
        "polygon": [],
        "confidence": 0.997,
        "span": {}
    },
],
"lines": [
    {
        "content": "While healthcare is still in the early stages of its Al journey, we",
        "polygon": [],
        "spans": [],
    }
]

```
Handwritten style
The response includes classifying whether each text line is of handwriting style or not, along with a confidence score. For more information, see
Handwritten language support
. The following example shows an example JSON snippet.
```
"styles": [
{
    "confidence": 0.95,
    "spans": [
    {
        "offset": 509,
        "length": 24
    }
    "isHandwritten": true
    ]
}

```
If you enable the
font/style add-on capability
, you also get the font/style result as part of the
styles
object.
Selection mark
The layout model also extracts selection marks from documents. Extracted selection marks appear within the
pages
collection for each page. They include the bounding
polygon
,
confidence
, and selection
state
(
selected/unselected
). The text representation (that is,
:selected:
and
:unselected
) is also included as the starting index (
offset
) and
length
that references the top-level
content
property that contains the full text from the document.
```
{
    "selectionMarks": [
        {
            "state": "unselected",
            "polygon": [],
            "confidence": 0.995,
            "span": {
                "offset": 1421,
                "length": 12
            }
        }
    ]
}

```
Sample code
Output
```
# Analyze selection marks.
for selection_mark in page.selection_marks:
    print(
        f"Selection mark is '{selection_mark.state}' within bounding polygon "
        f"'{format_polygon(selection_mark.polygon)}' and has a confidence of {selection_mark.confidence}"
    )


```
View samples on GitHub.
```
{
    "selectionMarks": [
        {
            "state": "unselected",
            "polygon": [],
            "confidence": 0.995,
            "span": {
                "offset": 1421,
                "length": 12
            }
        }
    ]
}

```
Table
Extracting tables is a key requirement for processing documents that contain large volumes of data typically formatted as tables. The layout model extracts tables in the
pageResults
section of the JSON output. Extracted table information includes the number of columns and rows, row span, and column span. Each cell with its bounding polygon is output along with information whether the area is recognized as
columnHeader
or not.
The model supports extracting tables that are rotated. Each table cell contains the row and column index and bounding polygon coordinates. For the cell text, the model outputs the
span
information that contains the starting index (
offset
). The model also outputs the
length
within the top-level content that contains the full text from the document.
Here are a few factors to consider when you use the Document Intelligence bale extraction capability:
Is the data that you want to extract presented as a table, and is the table structure meaningful?
Can the data fit in a two-dimensional grid if the data isn't in a table format?
Do your tables span multiple pages? If so, to avoid having to label all the pages, split the PDF into pages before you send it to Document Intelligence. After the analysis, post-process the pages to a single table.
See
Tabular fields
if you create custom models. Dynamic tables have a variable number of rows for each column. Fixed tables have a constant number of rows for each column.
Note
Table analysis isn't supported if the input file is XLSX. Document Intelligence v4.0 2024-11-30 (GA) supports bounding regions for figures and tables that cover only the core content and excludes the associated caption and footnotes.
```
{
    "tables": [
        {
            "rowCount": 9,
            "columnCount": 4,
            "cells": [
                {
                    "kind": "columnHeader",
                    "rowIndex": 0,
                    "columnIndex": 0,
                    "columnSpan": 4,
                    "content": "(In millions, except earnings per share)",
                    "boundingRegions": [],
                    "spans": []
                    },
            ]
        }
    ]
}


```
Sample code
Output
```
# Analyze tables.
for table_idx, table in enumerate(result.tables):
    print(
        f"Table # {table_idx} has {table.row_count} rows and "
        f"{table.column_count} columns"
    )
    for region in table.bounding_regions:
        print(
            f"Table # {table_idx} location on page: {region.page_number} is {format_polygon(region.polygon)}"
        )
    for cell in table.cells:
        print(
            f"...Cell[{cell.row_index}][{cell.column_index}] has text '{cell.content}'"
        )
        for region in cell.bounding_regions:
            print(
                f"...content on page {region.page_number} is within bounding polygon '{format_polygon(region.polygon)}'"
            )


```
View samples on GitHub.
```
{
    "tables": [
        {
            "rowCount": 9,
            "columnCount": 4,
            "cells": [
                {
                    "kind": "columnHeader",
                    "rowIndex": 0,
                    "columnIndex": 0,
                    "columnSpan": 4,
                    "content": "(In millions, except earnings per share)",
                    "boundingRegions": [],
                    "spans": []
                    },
            ]
        }
    ]
}


```
Annotations
The layout model extracts annotations in documents, such as checks and crosses. The response includes the kind of annotation, along with a confidence score and bounding polygon.
```
    {
    "pages": [
    {
        "annotations": [
        {
            "kind": "cross",
            "polygon": [...],
            "confidence": 1
        }
        ]
    }
    ]
}

```
Natural reading order output (Latin only)
You can specify the order in which the text lines are output with the
readingOrder
query parameter. Use
natural
for a more human-friendly reading order output, as shown in the following example. This feature is supported only for Latin languages.
Select page number or range for text extraction
For large multipage documents, use the
pages
query parameter to indicate specific page numbers or page ranges for text extraction. The following example shows a document with 10 pages, with text extracted for both cases, all pages (1-10), and selected pages (3-6).
The Get Analyze Layout Result operation
The second step is to call the
Get Analyze Layout Result
operation. This operation takes as input the Result ID that the
Analyze Layout
operation created. It returns a JSON response that contains a
status
field with the following possible values.
Field
Type
Possible values
status
string
notStarted
: The analysis operation isn't started.
running
: The analysis operation is in progress.
failed
: The analysis operation failed.
succeeded
: The analysis operation succeeded.
Call this operation iteratively until it returns the
succeeded
value. To avoid exceeding the requests-per-second rate, use an interval of three to five seconds.
When the
status
field has the
succeeded
value, the JSON response includes the extracted layout, text, tables, and selection marks. The extracted data includes extracted text lines and words, bounding boxes, text appearance with handwritten indication, tables, and selection marks with selected/unselected indicated.
Handwritten classification for text lines (Latin only)
The response includes classifying whether each text line is of a handwritten style or not, along with a confidence score. This feature is supported only for Latin languages. The following example shows the handwritten classification for the text in the image.
Sample JSON output
The response to the
Get Analyze Layout Result
operation is a structured representation of the document with all the information extracted.
See a
sample document file
and its structured output
sample layout output
.
The JSON output has two parts:
The
readResults
node contains all the recognized text and selection mark. The text presentation hierarchy is page, then line, and then individual words.
The
pageResults
node contains the tables and cells extracted with their bounding boxes, confidence, and a reference to the lines and words in the
readResults
field.
Example output
Text
The layout API extracts text from documents and images with multiple text angles and colors. It accepts photos of documents, faxes, printed and/or handwritten (English-only) text, and mixed modes. Text is extracted with information provided on lines, words, bounding boxes, confidence scores, and style (handwritten or other). All the text information is included in the
readResults
section of the JSON output.
Tables with headers
The Layout API extracts tables in the
pageResults
section of the JSON output. You can scan, photograph, or digitize documents. Tables can be complex with merged cells or columns, with or without borders, and with odd angles.
Extracted table information includes the number of columns and rows, row span, and column span. Each cell with its bounding box is output along with whether the area is recognized as part of a header or not. The model-predicted header cells can span multiple rows and aren't necessarily the first rows in a table. They also work with rotated tables. Each table cell also includes the full text with references to the individual words in the
readResults
section.
Selection marks (documents)
The layout API also extracts selection marks from documents. Extracted selection marks include the bounding box, confidence, and state (selected/unselected). Selection mark information is extracted in the
readResults
section of the JSON output.
Migration guide
To learn how to use the v3.1 version in your applications and workflows, follow the steps in the
Document Intelligence v3.1 migration guide
.
If you're using v3.0, migrate to v4.0 before
March 30, 2029
. Use the
Document Intelligence migration guide
and the
v4.0 quickstart
.
Related content
Learn how to
process your own forms and documents
with the
Document Intelligence Studio
.
Finish a
Document Intelligence quickstart
, and create a document processing app in the development language of your choice.
Find more samples on GitHub.
Find more samples on GitHub.
Learn how to
process your own forms and documents
with the
Document Intelligence Sample Labeling tool
.
Finish a
Document Intelligence quickstart
, and create a document processing app in the development language of your choice.
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