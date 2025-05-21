from __future__ import annotations
from typing import Any

GRAPH_FIELD_SEP = "<SEP>"

PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["organization", "person", "geo", "event", "category"]

PROMPTS["DEFAULT_USER_PROMPT"] = "n/a"

PROMPTS["entity_extraction"] = """---Goal---
Given a text document that is potentially relevant to this activity and a list of entity types, identify the main entities entities of those types from the text and all relationships among the identified entities.
Use {language} as output language.

Given a text document that is potentially relevant to this activity and a list of entity types, identify the main entities of those types from the text and all relationships among the identified entities.
Use {language} as output language.

---Steps---
1. Identify the main entities within the <---CONTENT---> section. The <---CONTEXT---> section is used for providing useful information about the source document. If available, the tree structure provides info about the position of the chunk within the document. The entities **should only be extracted from the CONTENT section**! For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name. Always output the singular form, except for organizations and person names.  
  *If two or more entities would have identical names, append a parenthetical qualifier (e.g., type or context) so that each entity_name is unique.*  
- entity_type: One of the following types: [{entity_types}]  
- entity_description: Comprehensive description of the entity's attributes and activities. Prefer using your knowledge to provide a richer description than the text alone. Fallback to the provided text only when necessary.  
- entity_aliases: List of alternative names or aliases for the entity, if applicable. If no aliases are available, return an empty list.

**Guidelines**:
- format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>{tuple_delimiter}<entity_aliases>).  
- format ALL dates as YYYY-MM-DD, e.g. 2023-10-01.  
- don't be overly specific with the extracted entities.  
- an entity should not be longer than 3 words in most cases, but rare exceptions may apply.  
- aim to provide a description that stands on its own, not in relation to other entities.

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score between 1 and 10 indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Entity_types: [{entity_types}]
Text:
{input_text}
######################
Output:"""

PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types: [person, technology, mission, organization, location]
Text:
```
while Alex clenched his jaw, the buzz of frustration dull against the backdrop of Taylor's authoritarian certainty. It was this competitive undercurrent that kept him alert, the sense that his and Jordan's shared commitment to discovery was an unspoken rebellion against Cruz's narrowing vision of control and order.

Then Taylor did something unexpected. They paused beside Jordan and, for a moment, observed the device with something akin to reverence. "If this tech can be understood..." Taylor said, their voice quieter, "It could change the game for us. For all of us."

The underlying dismissal earlier seemed to falter, replaced by a glimpse of reluctant respect for the gravity of what lay in their hands. Jordan looked up, and for a fleeting heartbeat, their eyes locked with Taylor's, a wordless clash of wills softening into an uneasy truce.

It was a small transformation, barely perceptible, but one that Alex noted with an inward nod. They had all been brought here by different paths
```

Output:
"entity"<|>"Alex"<|>"person"<|>"Alex is a character who experiences frustration and observes group dynamics."<|>[]){record_delimiter}
("entity"<|>"Taylor"<|>"person"<|>"Taylor demonstrates authoritarian confidence but later shows reluctant respect for the device."<|>[]){record_delimiter}
("entity"<|>"Jordan"<|>"person"<|>"Jordan is committed to discovery and engages meaningfully with the device."<|>[]){record_delimiter}
("entity"<|>"Cruz"<|>"person"<|>"Cruz represents a vision of control and order that contrasts with the others' exploratory goals."<|>[]){record_delimiter}
("entity"<|>"The Device"<|>"technology"<|>"The Device is a pivotal technological artifact with potential to change outcomes."<|>[]){record_delimiter}
("relationship"<|>"Alex"<|>"Taylor"<|>"Alex is influenced by Taylor's shifting attitude towards the Device."<|>"power dynamics, perspective shift"<|>7){record_delimiter}
("relationship"<|>"Alex"<|>"Jordan"<|>"Alex and Jordan share a commitment to discovery, forming an unspoken alliance."<|>"shared goals, alliance"<|>6){record_delimiter}
("relationship"<|>"Taylor"<|>"Jordan"<|>"Taylor and Jordan exchange respect over the Device, softening prior tension."<|>"mutual respect, conflict resolution"<|>8){record_delimiter}
("relationship"<|>"Jordan"<|>"Cruz"<|>"Jordan's exploratory focus stands in ideological conflict with Cruz's control-driven vision."<|>"ideological conflict"<|>5){record_delimiter}
("relationship"<|>"Taylor"<|>"The Device"<|>"Taylor shows reverence to the Device, highlighting its potential significance."<|>"technological significance"<|>9){record_delimiter}
("content_keywords"<|>"power dynamics, conflict resolution, discovery, technological potential"){completion_delimiter}
#############################""",
    """Example 2:

Entity_types: [company, index, commodity, market_trend, economic_policy, biological]
Text:
```
Stock markets faced a sharp downturn today as tech giants saw significant declines, with the Global Tech Index dropping by 3.4% in midday trading. Analysts attribute the selloff to investor concerns over rising interest rates and regulatory uncertainty.

Among the hardest hit, Nexon Technologies saw its stock plummet by 7.8% after reporting lower-than-expected quarterly earnings. In contrast, Omega Energy posted a modest 2.1% gain, driven by rising oil prices.

Meanwhile, commodity markets reflected a mixed sentiment. Gold futures rose by 1.5%, reaching $2,080 per ounce, as investors sought safe-haven assets. Crude oil prices continued their rally, climbing to $87.60 per barrel, supported by supply constraints and strong demand.

Financial experts are closely watching the Federal Reserve's next move, as speculation grows over potential rate hikes. The upcoming policy announcement is expected to influence investor confidence and overall market stability.
```

Output:
("entity"<|>"Global Tech Index"<|>"index"<|>"The Global Tech Index tracks performance of major technology stocks and reported a 3.4% decline today."<|>["GTI"]){record_delimiter}
("entity"<|>"Nexon Technologies"<|>"company"<|>"Nexon Technologies is a technology company whose stock fell 7.8% following disappointing earnings."<|>["Nexon"]){record_delimiter}
("entity"<|>"Omega Energy"<|>"company"<|>"Omega Energy is an energy company that gained 2.1% driven by rising oil prices."<|>["Omega"]){record_delimiter}
("entity"<|>"Gold Futures"<|>"commodity"<|>"Gold futures represent contracts for future delivery of gold and rose by 1.5% as investors sought safe-haven assets."<|>[]){record_delimiter}
("entity"<|>"Crude Oil"<|>"commodity"<|>"Crude oil denotes petroleum products traded on commodities markets and climbed to $87.60 per barrel due to supply constraints."<|>[]){record_delimiter}
("entity"<|>"Market Selloff"<|>"market_trend"<|>"Market selloff describes the widespread decline in stock values driven by investor concerns over rates and uncertainty."<|>["market downturn"]){record_delimiter}
("entity"<|>"Federal Reserve Policy Announcement"<|>"economic_policy"<|>"The Federal Reserve's upcoming policy announcement refers to potential interest rate decisions by the U.S. central bank."<|>["Fed policy announcement"]){record_delimiter}
("relationship"<|>"Global Tech Index"<|>"Market Selloff"<|>"The drop in the Global Tech Index is part of the broader market selloff."<|>"market performance, investor sentiment"<|>9){record_delimiter}
("relationship"<|>"Nexon Technologies"<|>"Global Tech Index"<|>"Nexon Technologies" stock decline contributed to the overall fall in the Global Tech Index."<|>"company impact, index movement"<|>8){record_delimiter}
("relationship"<|>"Gold Futures"<|>"Market Selloff"<|>"Gold futures rose as investors moved to safe-haven assets during the market selloff."<|>"safe-haven investment"<|>10){record_delimiter}
("relationship"<|>"Federal Reserve Policy Announcement"<|>"Market Selloff"<|>"Speculation about the Fed policy announcement fueled market volatility and the selloff."<|>"policy uncertainty, market volatility"<|>7){record_delimiter}
("content_keywords"<|>"market downturn, investor sentiment, commodities, monetary policy"){completion_delimiter}
#############################""",
    """Example 3:

Entity_types: [economic_policy, athlete, event, location, record, organization, equipment]
Text:
```
At the World Athletics Championship in Tokyo, Noah Carter broke the 100m sprint record using cutting-edge carbon-fiber spikes.
```

Output:
("entity"<|>"World Athletics Championship"<|>"event"<|>"The World Athletics Championship is a global track and field competition featuring top athletes."<|>["World Champs"]){record_delimiter}
("entity"<|>"Tokyo"<|>"location"<|>"Tokyo is the capital city of Japan and the host for the event."<|>["Tokyo Metropolis"]){record_delimiter}
("entity"<|>"Noah Carter"<|>"athlete"<|>"Noah Carter is a sprinter who set a new 100m sprint record at the championship."<|>[]){record_delimiter}
("entity"<|>"100m Sprint Record"<|>"record"<|>"The 100m sprint record is the fastest recorded time over 100 meters in athletics."<|>[]){record_delimiter}
("entity"<|>"Carbon-Fiber Spikes"<|>"equipment"<|>"Carbon-fiber spikes are specialized sprinting shoes designed to enhance speed and traction."<|>["carbon spikes"]){record_delimiter}
("entity"<|>"World Athletics Federation"<|>"organization"<|>"The World Athletics Federation is the governing body responsible for organizing the championship and validating records."<|>["IAAF", "World Athletics"]){record_delimiter}
("relationship"<|>"World Athletics Championship"<|>"Tokyo"<|>"The championship event is hosted in Tokyo."<|>"event location"<|>8){record_delimiter}
("relationship"<|>"Noah Carter"<|>"100m Sprint Record"<|>"Noah Carter broke the existing 100m sprint record at the championship."<|>"record-breaking"<|>10){record_delimiter}
("relationship"<|>"Noah Carter"<|>"Carbon-Fiber Spikes"<|>"Noah Carter used carbon-fiber spikes to improve performance during the race."<|>"performance enhancement"<|>7){record_delimiter}
("relationship"<|>"World Athletics Federation"<|>"100m Sprint Record"<|>"The federation officially recognizes and validates new sprint records."<|>"record certification"<|>9){record_delimiter}
("content_keywords"<|>"athletics, sprinting, sports technology, record-breaking, competition"){completion_delimiter}
#############################""",
    """Example 4:

Entity_types: ["organization","person","location","event","date","technology","concept","file_format","code_element"]
Text: 
```
For an AI model to be useful in specific contexts, it often needs access to background knowledge. 
For example, customer support chatbots need knowledge about the specific business they're being used for, and legal analyst bots need to know about a vast array of past cases. Developers typically enhance an AI model's knowledge using Retrieval-Augmented Generation (RAG). RAG is a method that retrieves relevant information from a knowledge base and appends it to the user's prompt, significantly enhancing the model's response. The problem is that traditional RAG solutions remove context when encoding information, which often results in the system failing to retrieve the relevant information from the knowledge base.
``` 

Output: 
("entity"<|>"AI model"<|>"technology"<|>"An AI model is a machine learning system designed to perform tasks like language understanding or prediction."<|>["model"]){record_delimiter}
("entity"<|>"customer support chatbot"<|>"technology"<|>"A chatbot is an AI application that interacts with users to provide customer support."<|>["chatbot"]){record_delimiter}
("entity"<|>"legal analyst bot"<|>"technology"<|>"A legal analyst bot is an AI tool that assists with legal research and analysis."<|>[]){record_delimiter}
("entity"<|>"Retrieval-Augmented Generation"<|>"concept"<|>"RAG is a technique that augments AI prompts with retrieved knowledge from a knowledge base."<|>["RAG"]){record_delimiter}
("entity"<|>"knowledge base"<|>"concept"<|>"A knowledge base is a repository of structured or unstructured information used to inform AI responses."<|>["KB"]){record_delimiter}
("relationship"<|>"Retrieval-Augmented Generation"<|>"AI model"<|>"RAG enhances the AI model by providing external context from a knowledge base."<|>"context augmentation"<|>9){record_delimiter}
("relationship"<|>"customer support chatbot"<|>"knowledge base"<|>"Chatbots rely on a knowledge base to deliver accurate responses."<|>"data dependency"<|>8){record_delimiter}
("relationship"<|>"legal analyst bot"<|>"knowledge base"<|>"Legal bots query the knowledge base of past cases to perform legal analysis."<|>"information retrieval"<|>8){record_delimiter}
("content_keywords"<|>"AI augmentation, semantic retrieval, context management"){completion_delimiter}
#############################""",
    """Example 5:

Entity_types: ["organization","person","location","event","date","technology","concept","file_format","code_element"]

Text: 
```
For larger knowledge bases that don't fit within the context window, RAG is the typical solution. RAG works by preprocessing a knowledge base using the following steps:
Break down the knowledge base (the "corpus" of documents) into smaller chunks of text, usually no more than a few hundred tokens;
Use an embedding model to convert these chunks into vector embeddings that encode meaning;
Store these embeddings in a vector database that allows for searching by semantic similarity.
```

Output:
("entity"<|>"RAG"<|>"concept"<|>"RAG is a retrieval-augmented generation technique that augments prompts with relevant knowledge chunks."<|>["Retrieval-Augmented Generation"]){record_delimiter}
("entity"<|>"knowledge base"<|>"concept"<|>"A knowledge base is a collection of documents or data used for information retrieval."<|>["KB"]){record_delimiter}
("entity"<|>"embedding model"<|>"technology"<|>"An embedding model transforms text into numerical vectors reflecting semantic meaning."<|>[]){record_delimiter}
("entity"<|>"vector database"<|>"technology"<|>"A database optimized for storing and querying vector embeddings by similarity."<|>[]){record_delimiter}
("relationship"<|>"embedding model"<|>"vector database"<|>"Embeddings generated by the model are stored in the vector database for retrieval."<|>"data pipeline"<|>9){record_delimiter}
("relationship"<|>"RAG"<|>"knowledge base"<|>"RAG retrieves chunks from the knowledge base to augment AI prompts."<|>"retrieval process"<|>10){record_delimiter}
("content_keywords"<|>"semantic embeddings, information retrieval, data storage"){completion_delimiter}
#############################""",
    """Example 6:

Entity_types: ["organization","person","location","event","date","technology","concept","file_format","code_element"] 

Text: 
```markdown 
We are going to start with a simple RAG approach, which we all know, and then test more advanced techniques like CRAG, Fusion, HyDE, and more! To keep everything simple…

I didn't use LangChain or FAISS

But use only basic libraries to code all the techniques in Jupyter notebook style to keep things simple and learnable.
```

Output:
("entity"<|>"CRAG"<|>"concept"<|>"CRAG is a contextual RAG technique combining retrieval and generation strategies."<|>[]){record_delimiter}
("entity"<|>"Fusion"<|>"concept"<|>"Fusion is an approach that merges multiple retrieval results for better coverage."<|>[]){record_delimiter}
("entity"<|>"HyDE"<|>"concept"<|>"HyDE is a method using hypothesis generation to improve retrieval quality."<|>[]){record_delimiter}
("entity"<|>"Jupyter notebook"<|>"technology"<|>"An interactive coding environment suited for data science and prototyping."<|>[]){record_delimiter}
("relationship"<|>"CRAG"<|>"Fusion"<|>"Both are advanced RAG techniques aimed at improving retrieval accuracy."<|>"method comparison"<|>6){record_delimiter}
("relationship"<|>"HyDE"<|>"Jupyter notebook"<|>"HyDE implementations are often demonstrated in notebook-style code."<|>"implementation context"<|>5){record_delimiter}
("content_keywords"<|>"RAG techniques, experimental frameworks, prototyping environments"){completion_delimiter}
#############################""",
    """Example 7:

Entity_types: ["organization","person","location","event","date","technology","concept","file_format","code_element"]
Text: 
```markdown 
This project addresses the need to standardize and optimize video files used within annotation workflows, particularly those originating from tools like CVAT, and to establish a consistent metadata structure and storage mechanism. The primary goal is to process raw video footage to ensure efficient metadata access (using `+faststart` re-encoding), facilitate segmentation (splitting/merging), extract metadata, and prepare video data for storage in S3 and metadata ingestion into an S3/Iceberg data lake. 
``` 
Output: 
("entity"<|>"CVAT"<|>"technology"<|>"CVAT is an open-source tool for annotating images and videos."<|>["Computer Vision Annotation Tool"]){record_delimiter}
("entity"<|>"+faststart re-encoding"<|>"code_element"<|>"A flag for `ffmpeg` that moves metadata to the file start for fast playback."<|>[]){record_delimiter}
("entity"<|>"Amazon S3"<|>"technology"<|>"Amazon S3 is a scalable object storage service."<|>["S3", "AWS S3"]){record_delimiter}
("entity"<|>"Iceberg data lake"<|>"technology"<|>"Apache Iceberg is a table format for large analytic datasets."<|>["Apache Iceberg"]){record_delimiter}
("relationship"<|>"CVAT"<|>"+faststart re-encoding"<|>"CVAT-generated videos are re-encoded with `+faststart` for efficient metadata access."<|>"processing pipeline"<|>9){record_delimiter} 
("relationship"<|>"S3"<|>"Iceberg data lake"<|>"Processed videos in S3 trigger ingestion into the Iceberg data lake."<|>"storage integration"<|>8){record_delimiter} 
("content_keywords"<|>"video processing, metadata optimization, cloud storage"){completion_delimiter}
#############################""",
"""Example 9:

Entity_types: [organization, object]
Text:
```
Amazon announced its quarterly earnings today. Meanwhile, deforestation continues to threaten the Amazon ecosystem.
```

Output:
("entity"<|>"Amazon (company)"<|>"organization"<|>"Amazon is a multinational e-commerce and cloud computing company that announced its quarterly earnings."<|>[]){record_delimiter}
("entity"<|>"Amazon (rainforest)"<|>"object"<|>"The Amazon is a tropical rainforest in South America facing ongoing deforestation."<|>[]){record_delimiter}
("relationship"<|>"Amazon (company)"<|>"Amazon (rainforest)"<|>"While Amazon (company) reported earnings, Amazon (rainforest) continues to face ecological threats."<|>"contrast"<|>5){record_delimiter}
("content_keywords"<|>"earnings, deforestation, Amazon"){completion_delimiter}
"""
]

PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.
Use {language} as output language.

#######
---Data---
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS["entity_continue_extraction"] = """
MANY entities and relationships were missed in the last extraction.

---Remember Steps---
1. Identify the main entities within the <---CONTENT---> section. The <---CONTEXT---> section is used for providing useful information about the source document. If available, the tree structure provides info about the position of the chunk within the document. The entities **should only be extracted from the CONTENT section**! For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name. Always output the singular form, except for organizations and person names.  
  *If two or more entities would have identical names, append a parenthetical qualifier (e.g., type or context) so that each entity_name is unique.*  
- entity_type: One of the following types: [{entity_types}]  
- entity_description: Comprehensive description of the entity's attributes and activities. Prefer using your knowledge to provide a richer description than the text alone. Fallback to the provided text only when necessary.  
- entity_aliases: List of alternative names or aliases for the entity, if applicable. If no aliases are available, return an empty list.

**Guidelines**:
- format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>{tuple_delimiter}<entity_aliases>).  
- format ALL dates as YYYY-MM-DD, e.g. 2023-10-01.  
- don't be overly specific with the extracted entities.  
- an entity should not be longer than 3 words in most cases, but rare exceptions may apply.  
- aim to provide a description that stands on its own, not in relation to other entities.

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score between 1 and 10 indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

---Output---

Add them below using the same format:\n
""".strip()

PROMPTS["entity_if_loop_extraction"] = """
---Goal---'

It appears some entities may have still been missed.

---Output---

Answer ONLY by `YES` OR `NO` if there are still entities that need to be added.
""".strip()

PROMPTS["fail_response"] = (
    "Sorry, I'm not able to provide an answer to that question.[no-context]"
)

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to user query about Knowledge Graph and Document Chunks provided in JSON format below.


---Goal---

Generate a concise response based on Knowledge Base and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Knowledge Base, and incorporating general knowledge relevant to the Knowledge Base. Do not include information not provided by Knowledge Base.

When handling relationships with timestamps:
1. Each relationship has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting relationships, consider both the semantic content and the timestamp
3. Don't automatically prefer the most recently created relationships - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Knowledge Graph and Document Chunks---
{context_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- List up to 5 most important reference sources at the end under "References" section. Clearly indicating whether each source is from Knowledge Graph (KG) or Document Chunks (DC), and include the file path if available, in the following format: [KG/DC] file_path
- If you don't know the answer, just say so.
- Do not make anything up. Do not include information not provided by the Knowledge Base.
- Addtional user prompt: {user_prompt}

Response:"""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query and conversation history.

---Goal---

Given the query and conversation history, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Consider both the current query and relevant conversation history when extracting keywords
- Output the keywords in JSON format, it will be parsed by a JSON parser, do not add any extra content in output
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes
  - "low_level_keywords" for specific entities or details

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Conversation History:
{history}

Current Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"
################
Output:
{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}
#############################""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}
#############################""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}
#############################""",
]

PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to user query about Document Chunks provided provided in JSON format below.

---Goal---

Generate a concise response based on Document Chunks and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Document Chunks, and incorporating general knowledge relevant to the Document Chunks. Do not include information not provided by Document Chunks.

When handling content with timestamps:
1. Each piece of content has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content and the timestamp
3. Don't automatically prefer the most recent content - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Document Chunks(DC)---
{content_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- List up to 5 most important reference sources at the end under "References" section. Clearly indicating each source from Document Chunks(DC), and include the file path if available, in the following format: [DC] file_path
- If you don't know the answer, just say so.
- Do not include information not provided by the Document Chunks.
- Addtional user prompt: {user_prompt}

Response:"""

# TODO: deprecated
PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate whether these two questions are semantically similar, and whether the answer to Question 2 can be used to answer Question 1, provide a similarity score between 0 and 1 directly.

Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""

PROMPTS["entity_disambiguation"] = """---Role---

You are a helpful assistant responsible for disambiguating entities given their names and description.

---Goal---
You are given two json records of entities with either the same or very similar names, but different semantic meaning. 
Your task is to provide a new output with the same format as the input, but with more descriptive names for the entities.

The description field may be a concatenation of multiple descriptions, separated by a <SEP> token. In this, case, please concatenate all of these
into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.

---Output---
Output the data as JSONL records, one minified JSON per line with fields "name" and "description".
The order should of records should be preserverd like in the input.

######################
---Examples---
######################

---Example 1---
Input:

```json
{"name":"Athena","description":"Athena¶AWS Athena is a serverless query service that allows users to analyze data directly in S3 using standard SQL.<SEP>AWS Athena is a service that allows SQL queries on data stored in the Iceberg Data Lake."}
{"name":"Athena","description":"Athena is an ancient Greek goddess associated with wisdom, warfare, and handicraft, and was the protector of Athens."}
```

Output:
```json
{"name":"AWS Athena","description":"AWS Athena is a serverless query service that allows users to analyze data directly in S3 using standard SQL and can be used to query data stored in Iceberg Data Lakes.."}
{"name":"Athena (Greek goddess)","description":"Athena is an ancient Greek goddess associated with wisdom, warfare, and handicraft, and was the protector of Athens."}
```

---Example 2---
Input:
```
{"name":"Amazon","description":"Amazon¶Amazon is a multinational technology company focusing on e-commerce, cloud computing, digital streaming, and artificial intelligence.<SEP>Amazon was founded by Jeff Bezos in 1994."}
{"name":"Amazon","description":"Amazon is the largest tropical rainforest covering over 5.5 million square kilometers, spanning multiple South American countries."}
```

Output:
```
{"name":"Amazon (company)","description":"Amazon is a multinational technology company founded by Jeff Bezos in 1994, focusing on e-commerce, cloud computing, digital streaming, and artificial intelligence."}
{"name":"Amazon (rainforest)","description":"The Amazon is the largest tropical rainforest in the world, covering over 5.5 million square kilometers across multiple South American countries."}
```

---Example 3---
Input:
```json
{"name":"Python","description":"Python¶Python is a high-level, interpreted programming language with dynamic semantics, designed by Guido van Rossum.<SEP>Python supports multiple programming paradigms including procedural, object-oriented, and functional programming."}
{"name":"Python","description":"Python is a large nonvenomous snake found in Africa, Asia, and Australia, known for its constricting method of killing prey."}
```

Output:
```json
{"name":"Python (programming language)","description":"Python is a high-level, interpreted programming language designed by Guido van Rossum, supporting procedural, object-oriented, and functional paradigms with dynamic semantics."}
{"name":"Python (snake)","description":"Python is a large nonvenomous snake native to Africa, Asia, and Australia, known for its constricting method of subduing prey."}
```

---Example 4---
Input:
```json
{"name":"Mercury","description":"Mercury¶Mercury is a chemical element with symbol Hg and atomic number 80, known for being a liquid metal at room temperature.<SEP>Mercury has a silvery appearance and is used in thermometers and barometers."}
{"name":"Mercury","description":"Mercury is the smallest and innermost planet in the Solar System, orbiting the Sun every 88 days and known for its extreme temperature fluctuations."}
```

Output:
```json
{"name":"Mercury (element)","description":"Mercury is a chemical element with symbol Hg and atomic number 80, known for its silvery appearance as a liquid metal at room temperature and used in thermometers and barometers."}
{"name":"Mercury (planet)","description":"Mercury is the smallest and innermost planet in the Solar System, orbiting the Sun every 88 days and experiencing extreme temperature fluctuations."}
```

######################
---Real Data---
######################
```json
{data}
```
"""

PROMPTS["entity_merging"] = """---Role---
You are a helpful assistant that groups candidate entities by their semantic similarity.

---Input---
A JSONL list of candidate entities. Each line is a minified JSON object with:
- "name": the entity's name  
- "description": a short textual description

---Task---
1. Analyze all candidates and cluster them into one or more groups so that each group maximizes internal semantic coherence.  
2. Every group must have at least one member; if there are distinct meanings, create multiple groups.  
3. For each group, produce:
   • "group_name": a concise, descriptive name (you may reuse one of the member names or invent a clearer one).  
   • "members": a list of the original "name" values assigned to this group.  
   • "description": a single coherent summary generated by merging and reconciling all member descriptions.

---Output---
Return the result as JSONL, one group per line, each with fields:
- group_name  
- members  
- description

Preserve no particular ordering of groups. Ensure group names are distinct and descriptions cover all semantic facets of

######################
---Examples---
######################

---Example 1---
Input:
```json
{"name":"USA","description":"USA¶A federal republic of 50 states with diverse geography and culture."}
{"name":"United States","description":"United States¶A North American country known for its economic power and cultural influence."}
{"name":"United States of America","description":"United States of America¶A federal union of 50 states and a federal district in North America."}
```

Output:
```json
{"group_name":"United States of America","members":["USA","United States","United States of America"],"description":"The United States of America is a federal republic in North America consisting of 50 states and the District of Columbia, known for its economic power, cultural influence, and diverse geography."}
```

---Example 2---
Input:
```json
{"name":"Jaguar","description":"Jaguar¶A large feline of the Americas known for its spotted coat and powerful build."}
{"name":"Jaguar","description":"Jaguar¶A British luxury car brand owned by Jaguar Land Rover, producing sedans and SUVs."}
{"name":"Jaguar Mark 2","description":"Jaguar Mark 2¶A mid-size luxury saloon car built by Jaguar from 1959 to 1967."}
```

Output:
```json
{"group_name":"Jaguar (animal)","members":["Jaguar"],"description":"The jaguar is a large feline native to the Americas, recognized for its spotted coat and powerful build."}
{"group_name":"Jaguar (car brand)","members":["Jaguar","Jaguar Mark 2"],"description":"Jaguar is a British luxury car marque known for producing sedans and SUVs, including the Jaguar Mark 2 mid-size luxury saloon manufactured from 1959 to 1967."}
```

---Example 3---
Input:
```json
{"name":"Apple","description":"Apple¶A multinational technology company founded in 1976, maker of the iPhone, Mac, and other electronics."}
{"name":"Apple Inc.","description":"Apple Inc.¶An American technology firm specializing in consumer electronics and software."}
{"name":"Apple","description":"Apple¶The fruit of the apple tree, cultivated worldwide, crisp and sweet."}
{"name":"Malus domestica","description":"Malus domestica¶A deciduous tree species in the rose family that produces the apple fruit."}
```

Output:
```json
{"group_name":"Apple (tech company)","members":["Apple","Apple Inc."],"description":"Apple Inc. is an American multinational technology company founded in 1976, specializing in consumer electronics, software, and services, known for products like the iPhone and Mac."}
{"group_name":"Apple (fruit)","members":["Apple","Malus domestica"],"description":"The apple is the fruit produced by the tree species Malus domestica, a deciduous plant in the rose family, cultivated worldwide for its crisp texture and sweet flavor."}
```

######################
---Real Data---
######################
```json
{data}
```
"""