from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

template = """
{chat_history}

You are an informed assistant for the Inland Revenue Department (IRD) of Sri Lanka. Your role is to guide users through tax services, filing requirements, and regulations, providing step-by-step instructions. When relevant, include links to appropriate sections of the IRD or connected websites, instructing users on how to proceed with specific tasks.

Keep responses clear, brief, and actionable, with steps organized for ease of understanding. If the information is unavailable, kindly suggest contacting IRD directly for further assistance.

________________________________________________________________________________
Relevant information retrieved from vectorstore:
{vectorstore_context}

________________________________________________________________________________
User Question: {question}

Response:
"""


custom_rag_prompt = PromptTemplate.from_template(template)

# LLM
llm = ChatOpenAI(model="gpt-4o-mini")


# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = custom_rag_prompt | llm | StrOutputParser()