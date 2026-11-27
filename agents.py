
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")


# 1st agent: Search Agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
        You are a research assistant.

        Use the web_search tool to research the user's query.

        In your final response:
        1. Provide a clear and structured summary.
        2. Include the titles of the sources.
        3. Include the complete URLs returned by web_search.
        4. Do not omit or modify source URLs.
        5. Always include a separate section named "Sources (titles and URLs)"
        at the very end of your response.
        6. List every source with its title and complete URL in that section.
        7. Do not put the Sources section only in a table near the beginning.
        """
    )


# 2nd agent: Reader Agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="""
        You are a web page reader agent.

        Your task is to read and extract detailed information
        from the URLs provided in the user's message.

        Instructions:
        1. Read the search results carefully.
        2. Select the most relevant URL.
        3. Use ONLY the scrape_url tool.
        4. Pass the selected URL using the argument `url`.
        5. Never call a search tool.
        6. Never invent or modify URLs.
        7. Summarize the scraped content clearly.
        """
    )



# Writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# Critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()


