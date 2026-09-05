#!/usr/bin/env python3
"""
Bedrock Corpus Generator for BM25-at-Scale experiment.

Source: OECD "The Agentic AI Landscape and Its Conceptual Foundations" (Feb 2026)

Design: Gold documents + adversarial traps sit in tier 0 (the bedrock).
Each subsequent tier adds ONLY background noise documents.
Same questions, same gold answers — only noise grows.
"""
import json
import os
import random
import hashlib
from pathlib import Path

random.seed(42)

CORPUS_DIR = Path(__file__).parent / "corpus"

# ─── GOLD DOCUMENTS — extracted from OECD Agentic AI paper ──────────────────

GOLD_DOCUMENTS = [
    {
        "id": "GOLD-001",
        "title": "OECD Definition of an AI System",
        "content": """The OECD Council Recommendation on Artificial Intelligence defines an AI system as
"a machine-based system that, for explicit or implicit objectives, infers, from the input it
receives, how to generate outputs such as predictions, content, recommendations, or decisions
that can influence physical or virtual environments. Different AI systems vary in their levels
of autonomy and adaptiveness after deployment."

The Explanatory Memorandum on the Updated OECD Definition and the OECD Framework for the
Classification of AI Systems identify the following key elements:
- Objectives (explicit/human-defined, implicit in rules, implicit in training data, not fully known)
- Input and data (used during development and after deployment)
- Inference (generating intermediate or final outputs from inputs)
- Outputs (predictions, content, recommendations, decisions, actions)
- Influence on physical or virtual environments
- Autonomy (degree to which a system can learn or act without human involvement)
- Adaptiveness (ability to continue learning and evolving after deployment)

Autonomy levels include:
a) No-action autonomy (human support) — system recommends, human decides
b) Low-action autonomy (human-in-the-loop) — system suggests, human approves
c) Medium-action autonomy (human-on-the-loop) — system acts unless human intervenes
d) High-action autonomy (human-out-of-the-loop) — system acts entirely on its own""",
        "questions": [
            {"q": "How does the OECD define an AI system?",
             "a": "A machine-based system that, for explicit or implicit objectives, infers from input how to generate outputs such as predictions, content, recommendations, or decisions that can influence physical or virtual environments",
             "type": "definition"},
            {"q": "What are the four levels of autonomy in the OECD AI framework?",
             "a": "No-action autonomy (human support), low-action autonomy (human-in-the-loop), medium-action autonomy (human-on-the-loop), high-action autonomy (human-out-of-the-loop)",
             "type": "factual"},
            {"q": "What are the seven key elements of the OECD AI system definition?",
             "a": "Objectives, input and data, inference, outputs, influence on environments, autonomy, and adaptiveness",
             "type": "enumeration"},
        ]
    },
    {
        "id": "GOLD-002",
        "title": "AI Agents — Conceptual Foundations and Definition",
        "content": """AI agents are systems that can perceive and act upon their environment with a degree
of autonomy, using tools as needed to achieve specific goals and adapt to changing inputs and
contexts.

The concept of an "agent" predates AI. Derived from the Latin "agere" (to act), it has deep
roots in philosophy where an agent is a being with the capacity to act. In economics, an agent
refers to a decision maker whose behaviour is modelled as the solution to an optimisation problem.

Contemporary AI research defines an intelligent agent as an entity that perceives its environment
through sensors and acts upon it through actuators (Russell and Norvig, 1995).

Two broad types of agents:
1. Reactive agents (reflex agents) — respond to stimuli without planning or goal-setting
2. Cognitive agents — perceive environment, reason about it, make decisions based on objectives.
   A rational agent is a cognitive agent that acts to achieve the best expected outcome.

Capability-driven categorisation (Russell and Norvig, 2022):
- Simple reflex agents
- Model-based agents (internal representation)
- Goal-based agents (acting to achieve specific objectives)
- Utility-based agents (calculating most desirable outcome)
- Learning agents (improve own performance over time)

Three elements are PREVALENT in AI agent definitions:
1. Objectives — goals guiding behaviour
2. Outputs — often in the form of actions
3. Autonomy — degree of independent operation

FREQUENT elements: influence on environment, adaptiveness, inference.
OCCASIONAL elements: data and input.""",
        "questions": [
            {"q": "What are the three prevalent elements in AI agent definitions according to the OECD analysis?",
             "a": "Objectives, outputs (often in the form of actions), and autonomy",
             "type": "factual"},
            {"q": "What is the difference between reactive and cognitive agents?",
             "a": "Reactive agents simply respond to stimuli without planning, while cognitive agents perceive their environment, reason about it, and make decisions based on objectives",
             "type": "comparative"},
            {"q": "What Latin word is 'agent' derived from and what does it mean?",
             "a": "Agere, meaning to act",
             "type": "factual"},
        ]
    },
    {
        "id": "GOLD-003",
        "title": "Agentic AI — Definition and Distinct Characteristics",
        "content": """Agentic AI generally refers to systems composed of multiple co-ordinated AI agents
that can break down tasks, collaborate, and pursue complex objectives autonomously over extended
periods. Agentic AI systems are designed to operate in more open-ended, less predictable physical
or virtual environments and to function with minimal human supervision.

Key distinctions from AI agents:
- Objectives: More complex goals with task decomposition, delegation, and longer timeframes
  (AI agents have simpler, narrower goals with shorter timeframes)
- Outputs: Execution of more complex tasks within a larger action space
- Autonomy: Greater autonomy, flexibility and agency; may include capacity for autonomous tool discovery
- Influence on environment: More open-ended, complex, and unpredictable environments
- Adaptiveness: Higher-order adaptiveness, including reflexive and self-improvement capabilities
- Inference: Multi-agent co-ordination, distributed reasoning, deliberative reasoning

Task decomposition and delegation: Agentic AI systems can break down complex objectives into
smaller, manageable tasks and delegate them to individual agents.

Extended timeframes: Agentic AI systems can pursue goals over longer periods, introducing a
temporal dimension absent in most AI agent definitions.

System-level architecture: Agentic AI is often described as a system of co-ordinated AI agents,
typically organised within LLM-enabled architectures.

Distributed problem-solving: Agents in an agentic system work together to solve problems
collectively through inference, planning, and co-ordination.

The AAAI (2025) defines: "The concept of Agentic AI refers to the integration of generative AI
and LLMs into autonomous agent frameworks aiming to leverage the generative capabilities of such
models to enhance interaction, creativity, and real-time decision-making in dynamic environments."

Not all AI agents are part of an agentic AI system. Individual agents operating in isolation —
without broader system-level orchestration — are generally not considered agentic AI.""",
        "questions": [
            {"q": "What is the OECD's common understanding of agentic AI?",
             "a": "Systems composed of multiple co-ordinated AI agents that can break down tasks, collaborate, and pursue complex objectives autonomously over extended periods, designed to operate in open-ended, less predictable environments with minimal human supervision",
             "type": "definition"},
            {"q": "How does AAAI (2025) define agentic AI?",
             "a": "The integration of generative AI and LLMs into autonomous agent frameworks aiming to leverage generative capabilities to enhance interaction, creativity, and real-time decision-making in dynamic environments",
             "type": "definition"},
            {"q": "Are all AI agents part of an agentic AI system?",
             "a": "No, individual agents operating in isolation without broader system-level orchestration are generally not considered agentic AI",
             "type": "factual"},
        ]
    },
    {
        "id": "GOLD-004",
        "title": "Agentic AI as a Socio-Technical Paradigm",
        "content": """Agentic AI systems are more than technical tools; they are increasingly regarded as
systems embedded in social contexts and interactions, operating in a socio-technical paradigm.

The value of agentic AI systems comes from their ability to act autonomously and interact with
other agents — human, artificial, or institutional — through co-ordination and negotiation.

In this socio-technical view, agentic AI systems can possess:
- Autonomy: The ability to act independently within a defined scope
- Social Ability: Capacity to interact with other agents through protocols
- Reactivity: Awareness and responsive engagement with the environment
- Pro-activeness: Anticipation of needs and taking initiative toward goals

Effective interaction depends on robust technical infrastructures and shared protocols that
enable agents to communicate, co-ordinate, and be orchestrated. Key standards include:
- Model Context Protocol (MCP) by Anthropic — open standard for connecting AI applications to
  external data sources and tools
- Agent-to-Agent (A2A) protocol by Google — protocol for agent interoperability
- Agent Communication Language (ACL) — formal language for structured inter-agent communication

According to Dignum and Dignum (2025), such systems should be capable of handling potentially
conflicting goals, adjusting to real-world situations, and knowing when a "good enough" outcome
is more appropriate than constant optimisation.

Lessons from multi-agent system research can provide a valuable foundation for designing more
reliable, context-aware LLM-enabled multi-agent interactions (AAAI, 2025).""",
        "questions": [
            {"q": "What are the four capabilities agentic AI systems possess in the socio-technical paradigm?",
             "a": "Autonomy, social ability, reactivity, and pro-activeness",
             "type": "factual"},
            {"q": "What is the Model Context Protocol (MCP) and who created it?",
             "a": "An open standard by Anthropic for connecting AI applications to external data sources and tools",
             "type": "factual"},
            {"q": "What three interoperability standards are mentioned for agent communication?",
             "a": "Model Context Protocol (MCP) by Anthropic, Agent-to-Agent (A2A) protocol by Google, and Agent Communication Language (ACL)",
             "type": "enumeration"},
        ]
    },
    {
        "id": "GOLD-005",
        "title": "Stack Overflow Developer Survey — AI Agent Adoption Trends",
        "content": """The Stack Overflow Developer Survey received more than 49,000 responses from 177
countries and covered 62 questions. It defines AI agents as "autonomous software entities that
can operate with minimal to no direct human intervention using artificial intelligence techniques."

Key findings on AI agent adoption:
- About half of respondents are already using, or plan to use, AI agents in their work
- 38% have no plans to adopt AI agents
- The vast majority of developers highlight opportunities to further strengthen security,
  privacy, and accuracy of AI agents

Most common use: Software engineering purposes
- However, 64% of respondents identifying as data scientist, engineer, or analyst use agents
  primarily for data and analytics

Most popular tools by use case:
- AI agent memory/data management: Redis, GitHub MCP Server, Supabase, ChromaDB
- AI agent orchestration/frameworks: Ollama, LangChain, LangGraph, Vertex AI, Amazon Bedrock Agents
- AI agent observability/monitoring/security: Grafana + Prometheus, Sentry, Snyk, New Relic, LangSmith
- Out-of-the-box agents/copilots/assistants: ChatGPT, GitHub Copilot, Google Gemini, Claude, Microsoft Copilot""",
        "questions": [
            {"q": "How many responses did the Stack Overflow Developer Survey receive?",
             "a": "More than 49,000 responses from 177 countries",
             "type": "factual"},
            {"q": "What percentage of developers have no plans to adopt AI agents?",
             "a": "38%",
             "type": "factual"},
            {"q": "What is the most common use case for AI agents among developers?",
             "a": "Software engineering purposes",
             "type": "factual"},
        ]
    },
    {
        "id": "GOLD-006",
        "title": "GitHub Activity — Agentic AI Framework Adoption",
        "content": """According to recent data, GitHub activity has seen a 920% increase in repositories
using agentic AI frameworks such as AutoGPT, BabyAGI, OpenDevin, and CrewAI from early 2023
to mid-2025 (SuperAGI, 2025).

In parallel, emerging trends in GitHub repositories, including increasing adoption of the MCP
and multi-agent orchestration strategies, highlight a significant shift toward agent-centric
development paradigms (Ruiz, 2025).

Global searches for "agentic AI" on Google increased sharply in 2025, indicating it is becoming
a rapidly established concept in the AI landscape. Google Trends data shows search interest
scaled from near zero to peak interest (100) during 2025.

The agentic AI paradigm differs from traditional AI agents in both architecture and function.
Whereas single AI agents are typically designed to complete well-defined, tool-assisted tasks
in isolation, agentic AI systems consist of multiple, specialised agents that communicate and
co-ordinate to achieve shared objectives within open, evolving environments (Yousefi, Billi
and Rotolo, 2025).

Five levels of AI agent sophistication have been proposed (Chawla, 2025):
Level 1: Simple reflex — rule-based, no memory
Level 2: Model-based — internal world model
Level 3: Goal-based — pursue specific objectives
Level 4: Utility-based — optimise for best outcome
Level 5: Learning — self-improving through experience""",
        "questions": [
            {"q": "By what percentage did GitHub agentic AI framework repositories increase from 2023 to mid-2025?",
             "a": "920%",
             "type": "factual"},
            {"q": "Which four agentic AI frameworks are mentioned in the GitHub activity data?",
             "a": "AutoGPT, BabyAGI, OpenDevin, and CrewAI",
             "type": "enumeration"},
            {"q": "What are the five levels of AI agent sophistication proposed by Chawla (2025)?",
             "a": "Simple reflex, model-based, goal-based, utility-based, and learning",
             "type": "enumeration"},
        ]
    },
    {
        "id": "GOLD-007",
        "title": "AI Agent Definitions — Russell and Norvig to Modern Sources",
        "content": """Key definitions of AI agents from multiple authoritative sources:

Russell and Norvig (1995): "An agent is something that perceives and acts in an environment.
An ideal intelligent agent takes the best possible action in a situation. Computer agents are
expected to: operate autonomously, perceive their environment, persist over a prolonged time
period, adapt to change, and create and pursue goals."

Wooldridge (2002): "An agent is a computer system that is capable of independent action on
behalf of its user or owner."

Ferber (1999): An agent is a physical or virtual entity capable of acting in an environment,
communicating with other agents, driven by tendencies/objectives, possessing resources,
perceiving its environment (to a limited extent), offering services.

IBM (2025): "An AI agent is a software entity that employs AI techniques and has agency to act
in its environment based on set goals."

NIST (2025): "AI agent systems have the capability for autonomous decision-making and taking
action to operate with limited human supervision to achieve complex goals."

Bengio et al. (2025): "AI agent: A general-purpose AI which acts to achieve goals, possibly
using plans, adaptively performing tasks involving multiple steps and uncertain outcomes,
interacting with its environment with little to no human oversight."

Anthropic (2024): Agents are LLMs using tools based on environmental feedback in a loop. The
task often terminates upon completion, but it's also common to include stopping conditions
such as a maximum number of iterations.

Partnership on AI (2025): "Agents reason, plan, and perform sequences of actions to achieve
user goals. Unlike generative AI, these systems directly execute actions by using digital
tools to interact with complex environments."

Hugging Face (2025): "An agent is a system that leverages an AI model to interact with its
environment in order to achieve a user-defined objective." """,
        "questions": [
            {"q": "How does NIST (2025) define AI agent systems?",
             "a": "AI agent systems have the capability for autonomous decision-making and taking action to operate with limited human supervision to achieve complex goals",
             "type": "definition"},
            {"q": "How does Anthropic (2024) describe agents?",
             "a": "Agents are LLMs using tools based on environmental feedback in a loop",
             "type": "definition"},
            {"q": "According to Bengio et al. (2025), what is an AI agent?",
             "a": "A general-purpose AI which acts to achieve goals, possibly using plans, adaptively performing tasks involving multiple steps and uncertain outcomes, interacting with its environment with little to no human oversight",
             "type": "definition"},
        ]
    },
    {
        "id": "GOLD-008",
        "title": "Key Differences Between AI Agents and Agentic AI Systems",
        "content": """Comparative framework based on the key elements of the OECD AI System Definition:

OBJECTIVES:
- AI Agents: Simpler, narrower goals with shorter timeframes
- Agentic AI: More complex goals with task decomposition, delegation and longer timeframes

OUTPUTS:
- AI Agents: Execution of more basic tasks and decision making within a more limited action space
- Agentic AI: Execution of more complex tasks within a larger action space

AUTONOMY:
- AI Agents: Higher reliance on step-by-step instructions and closer supervision
- Agentic AI: Greater autonomy, flexibility and agency; may include autonomous tool discovery

INFLUENCE ON ENVIRONMENT:
- AI Agents: Less complex environments typically within digital ecosystems
- Agentic AI: More open-ended, complex, and unpredictable environments

ADAPTIVENESS:
- AI Agents: Basic adaptiveness to changing inputs and contexts
- Agentic AI: Higher-order adaptiveness, including reflexive and self-improvement capabilities

INFERENCE:
- AI Agents: Individual reasoning and planning
- Agentic AI: Multi-agent co-ordination, distributed reasoning, deliberative reasoning

Agency exists on a spectrum: from reactive agents that simply respond to stimuli, through
agent-assisted workflows such as "copilot" systems that support discrete tasks, to agentic AI
systems that co-ordinate multiple agents and manage entire workflows with minimal human oversight.

While agentic AI systems are composed of AI agents, not all AI agents are part of an agentic
AI system. Individual agents operating in isolation are generally not considered agentic AI.""",
        "questions": [
            {"q": "How does the autonomy of AI agents differ from agentic AI systems?",
             "a": "AI agents have higher reliance on step-by-step instructions and closer supervision, while agentic AI has greater autonomy, flexibility and agency including capacity for autonomous tool discovery",
             "type": "comparative"},
            {"q": "What does the spectrum of agency range from according to the OECD report?",
             "a": "From reactive agents that respond to stimuli, through agent-assisted workflows (copilot systems), to agentic AI systems that co-ordinate multiple agents with minimal human oversight",
             "type": "factual"},
        ]
    },
    {
        "id": "GOLD-009",
        "title": "Agentic AI Architectures and Technical Stack",
        "content": """Architecture-driven categorisation of AI agents includes:
- BDI (Belief-Desire-Intention) — formalises mental states into beliefs, desires, and intentions
- Reactive architectures — direct stimulus-response mappings without internal models
- Layered/hybrid architectures — combine reactive and deliberative components in stacked layers

LLM-based agent architectures are built around a central LLM augmented with:
1. Planning modules — task decomposition and strategy formulation
2. Memory systems — short-term and long-term storage for context and past interactions
3. Tool use — ability to call external APIs, code execution, web search
4. Action modules — executing decisions in the environment

Inference in agentic AI is evolving from immediate generation to "deliberative reasoning" or
"test-time compute." Rather than producing instantaneous outputs, agentic systems engage in
internal chains of thought as well as recursive multi-agent critique and self-reflection
during inference (Kim et al., 2025; Zhao et al., 2025).

Agentic AI denotes systems that couple large-scale foundation models with capabilities to reason,
act (e.g., via tools or environments), and interact with users and other systems in a sustained,
goal-directed manner (Dignum and Dignum, 2025).

Challapally et al. (2025) describe agentic AI as "the class of systems that embeds persistent
memory and iterative learning by design. Unlike current systems that require full context each
time, agentic systems maintain persistent memory, learn from interactions, and can autonomously
orchestrate complex workflows."

For multi-agent interoperability, Gosmar et al. (2024) proposed an "AI multi-agent
interoperability extension for managing multiparty conversations." Hammond et al. (2025) studied
multi-agent risks from advanced AI systems.""",
        "questions": [
            {"q": "What are the three architecture types for categorising intelligent agents?",
             "a": "BDI (Belief-Desire-Intention), reactive architectures, and layered/hybrid architectures",
             "type": "enumeration"},
            {"q": "What four components augment the central LLM in LLM-based agent architectures?",
             "a": "Planning modules, memory systems, tool use, and action modules",
             "type": "enumeration"},
            {"q": "How is inference evolving in agentic AI according to the paper?",
             "a": "From immediate generation to deliberative reasoning or test-time compute, involving internal chains of thought and recursive multi-agent critique and self-reflection",
             "type": "factual"},
        ]
    },
    {
        "id": "GOLD-010",
        "title": "Policy Implications and Future Directions for Agentic AI",
        "content": """The OECD report identifies several areas meriting further exploration for policymaking:

1. Greater clarity on architectures underpinning agentic AI and its technical stack.
   Mapping these architectures can help identify where safeguards, standards, or oversight
   mechanisms may be most effective.

2. Development of relevant typologies of agentic AI to support policy development.
   Such typologies might distinguish systems by domain of application, level of autonomy,
   adaptiveness, tool access levels, or capacity to influence environments.

3. Empirical evidence on adoption and use across different contexts.
   Limited data on AI agent adoption and use constrain the evidence base.

4. The need for responsible deployment frameworks.
   As agentic AI systems become more capable and widely deployed, effective policymaking
   requires understanding system-level orchestration and minimal human oversight scenarios.

The report is part of the OECD Horizontal Project on Thriving with AI: Empowering Economies
and Societies.

The paper was prepared by Luis Aranda and Kasumi Sugimoto from the OECD AI and Emerging
Digital Technologies (AIEDT) Division, under strategic direction of Audrey Plonk.

It was presented at the fourth Plenary meeting of the Global Partnership on Artificial
Intelligence (GPAI) in November 2025 and at an ad hoc Agentic AI expert workshop attended
by over 190 experts.

The OECD.AI Expert Group on Agentic AI is co-chaired by Vincent Corruble (Sorbonne University)
and Francesca Rossi (IBM).

Chan et al. (2023) identified 4 key characteristics of increasing agency: underspecification,
directness of impact, goal-directedness, and long-term planning.""",
        "questions": [
            {"q": "Who co-chairs the OECD.AI Expert Group on Agentic AI?",
             "a": "Vincent Corruble (Sorbonne University) and Francesca Rossi (IBM)",
             "type": "factual"},
            {"q": "How many experts attended the ad hoc Agentic AI expert workshop?",
             "a": "Over 190 experts",
             "type": "factual"},
            {"q": "What four characteristics of increasing agency did Chan et al. (2023) identify?",
             "a": "Underspecification, directness of impact, goal-directedness, and long-term planning",
             "type": "enumeration"},
        ]
    },
]

# ─── ADVERSARIAL TRAP DOCUMENTS ────────────────────────────────────────────

TRAP_DOCUMENTS = [
    {
        "id": "TRAP-001",
        "title": "Blog Post: Agentic AI Means Fully Autonomous AI (MISLEADING)",
        "content": """Popular Tech Blog — "Agentic AI = AGI?"
Many commentators conflate agentic AI with artificial general intelligence (AGI).
CLARIFICATION: The OECD report makes NO claim that agentic AI equals AGI. Agentic AI
refers to systems of co-ordinated agents with task decomposition and delegation, NOT
to systems with human-level general intelligence. This conflation is misleading."""
    },
    {
        "id": "TRAP-002",
        "title": "Draft Note: AI Agents Don't Need Autonomy (INCORRECT)",
        "content": """Internal Discussion Note (pre-review):
A reviewer suggested that autonomy is not a defining characteristic of AI agents.
CORRECTION: This is INCORRECT. The OECD analysis shows autonomy is one of the THREE
most prevalent elements in AI agent definitions, along with objectives and outputs.
This note was rejected during peer review."""
    },
    {
        "id": "TRAP-003",
        "title": "Outdated Article: AI Agent Adoption at 90% (INCORRECT STAT)",
        "content": """Tech Magazine Article (2024, OUTDATED):
"Survey shows 90% of developers have adopted AI agents in their work."
CORRECTION: The Stack Overflow 2025 survey (49,000+ respondents) shows that about HALF
of developers are using or plan to use AI agents, and 38% have NO plans to adopt them.
The 90% figure is fabricated and should not be cited."""
    },
    {
        "id": "TRAP-004",
        "title": "Misattributed Quote: NIST Defines Agentic AI (WRONG SOURCE)",
        "content": """Presentation Slide (contains error):
"NIST (2025) defines agentic AI as systems composed of multiple co-ordinated agents."
CORRECTION: NIST (2025) defines AI AGENT SYSTEMS, not agentic AI. The definition of
agentic AI as "multiple co-ordinated agents" comes from the OECD's own analysis
synthesising multiple sources. Do not attribute this to NIST."""
    },
    {
        "id": "TRAP-005",
        "title": "Conference Abstract: MCP Created by Google (WRONG ATTRIBUTION)",
        "content": """Conference Abstract (factual error):
"Google's Model Context Protocol (MCP) enables AI agent interoperability."
CORRECTION: MCP was created by ANTHROPIC, not Google. Google created the Agent-to-Agent
(A2A) protocol. These are DIFFERENT standards by DIFFERENT companies."""
    },
    {
        "id": "TRAP-006",
        "title": "Student Essay: GitHub Activity 200% Increase (WRONG NUMBER)",
        "content": """Student Term Paper (incorrect data):
"GitHub repositories using agentic AI frameworks saw a 200% increase."
CORRECTION: The actual figure is a 920% increase in GitHub repositories using agentic
AI frameworks (AutoGPT, BabyAGI, OpenDevin, CrewAI) from early 2023 to mid-2025.
The 200% figure is made up."""
    },
    {
        "id": "TRAP-007",
        "title": "Draft Report: Reactive Agents Are Agentic AI (MISCLASSIFICATION)",
        "content": """Internal Draft (rejected):
"Simple reactive agents qualify as agentic AI because they respond to their environment."
CORRECTION: The OECD report explicitly states that individual agents operating in isolation
without broader system-level orchestration are generally NOT considered agentic AI.
Reactive agents lack the coordination, task decomposition, and extended timeframes
that characterise agentic AI."""
    },
    {
        "id": "TRAP-008",
        "title": "Social Media Post: Only 2 Autonomy Levels (INCOMPLETE)",
        "content": """LinkedIn Post (oversimplified):
"The OECD defines two levels of AI autonomy: with human oversight and without."
CORRECTION: The OECD framework defines FOUR levels of autonomy:
1) No-action (human support), 2) Low-action (human-in-the-loop),
3) Medium-action (human-on-the-loop), 4) High-action (human-out-of-the-loop).
Reducing this to two levels loses critical nuance."""
    },
]

# ─── NOISE DOCUMENT TEMPLATES ──────────────────────────────────────────────

NOISE_TOPICS = [
    ("AI Ethics", [
        "bias detection in machine learning models", "fairness metrics for classification",
        "algorithmic accountability frameworks", "ethical AI deployment guidelines",
        "transparency in automated decision-making", "AI impact assessments",
        "responsible AI governance structures", "human rights and AI systems",
        "AI safety research methodologies", "value alignment in AI systems"
    ]),
    ("Machine Learning", [
        "gradient descent optimization techniques", "neural network architecture design",
        "transfer learning for domain adaptation", "reinforcement learning reward shaping",
        "generative adversarial network training", "attention mechanism implementations",
        "model compression and quantization", "federated learning privacy guarantees",
        "hyperparameter tuning strategies", "ensemble methods for robust prediction"
    ]),
    ("Natural Language Processing", [
        "tokenization strategies for multilingual models", "sentiment analysis benchmarks",
        "named entity recognition approaches", "machine translation quality metrics",
        "question answering system architectures", "text summarization techniques",
        "language model pre-training objectives", "dialogue system design patterns",
        "information extraction pipelines", "semantic similarity computation"
    ]),
    ("Cloud Computing", [
        "containerization and orchestration platforms", "serverless architecture patterns",
        "cloud cost optimization strategies", "multi-cloud deployment frameworks",
        "edge computing for IoT applications", "cloud security best practices",
        "infrastructure as code tooling", "service mesh implementations",
        "cloud-native application development", "data lake architecture design"
    ]),
    ("Data Science", [
        "exploratory data analysis methodologies", "feature engineering best practices",
        "time series forecasting models", "anomaly detection in streaming data",
        "A/B testing statistical frameworks", "causal inference methods",
        "data pipeline orchestration tools", "data quality monitoring systems",
        "dimensionality reduction techniques", "graph analytics algorithms"
    ]),
    ("Software Engineering", [
        "microservices architecture patterns", "continuous integration best practices",
        "code review automation tools", "technical debt management strategies",
        "API design and versioning standards", "database migration approaches",
        "performance testing frameworks", "observability and monitoring stack",
        "security vulnerability scanning", "developer productivity metrics"
    ]),
    ("Robotics", [
        "simultaneous localization and mapping", "robot motion planning algorithms",
        "computer vision for object detection", "human-robot interaction design",
        "swarm robotics coordination protocols", "manipulation and grasping strategies",
        "sensor fusion techniques", "autonomous navigation systems",
        "robotic process automation workflows", "safety standards for collaborative robots"
    ]),
    ("Digital Policy", [
        "data privacy regulation compliance", "intellectual property in AI outputs",
        "competition policy for AI markets", "cross-border data flow frameworks",
        "digital identity verification standards", "platform governance models",
        "cybersecurity regulation landscape", "digital skills workforce development",
        "broadband infrastructure investment", "open data initiative management"
    ]),
]

def _generate_noise_doc(idx: int) -> dict:
    topic_name, subtopics = random.choice(NOISE_TOPICS)
    subtopic = random.choice(subtopics)
    doc_num = 1000 + idx

    paragraphs = []
    for _ in range(random.randint(6, 12)):
        words = []
        for _ in range(random.randint(40, 80)):
            pool = [
                "the", "analysis", "of", "artificial", "intelligence", "systems",
                "framework", "implementation", "requires", "careful", "consideration",
                "of", "multiple", "factors", "including", "performance", "safety",
                "reliability", "and", "scalability", "across", "different", "deployment",
                "environments", "research", "indicates", "that", "modern", "approaches",
                "to", "machine", "learning", "leverage", "large", "scale", "data",
                "processing", "techniques", "combined", "with", "advanced", "model",
                "architectures", "enable", "more", "effective", "solutions", "for",
                "complex", "tasks", "requiring", "multi-step", "reasoning", "planning",
                "tool", "use", "integration", "evaluation", "methods", "should",
                "account", "domain-specific", "constraints", "governance", "policies",
                "standards", "compliance", "protocols", "best", "practices", "industry",
                "benchmarks", "stakeholder", "requirements", "user", "experience",
                "design", "principles", "development", "lifecycle", "management",
                topic_name.lower(), subtopic.split()[0], subtopic.split()[-1]
            ]
            words.append(random.choice(pool))
        paragraphs.append(" ".join(words) + ".")

    content = f"Document: DOC-{doc_num}\nTopic: {topic_name} — {subtopic}\n\n"
    content += "\n\n".join(paragraphs)

    return {
        "id": f"NOISE-{idx:05d}",
        "title": f"{topic_name}: {subtopic.title()} (DOC-{doc_num})",
        "content": content,
    }


def build_corpus_tiers(max_tier: int = 7) -> dict:
    """Build nested corpus tiers. Returns {tier: [doc_list]}."""
    tiers = {}

    bedrock = []
    for g in GOLD_DOCUMENTS:
        bedrock.append({"id": g["id"], "title": g["title"], "content": g["content"], "type": "gold"})
    for t in TRAP_DOCUMENTS:
        bedrock.append({"id": t["id"], "title": t["title"], "content": t["content"], "type": "trap"})

    tiers[0] = bedrock

    noise_idx = 0
    cumulative = list(bedrock)
    noise_counts = [0, 75, 150, 300, 600, 1200, 2400, 4800]

    for tier in range(1, max_tier + 1):
        new_noise = []
        for _ in range(noise_counts[tier]):
            new_noise.append({**_generate_noise_doc(noise_idx), "type": "noise"})
            noise_idx += 1
        cumulative = cumulative + new_noise
        tiers[tier] = list(cumulative)

    return tiers


def save_corpus(tiers: dict):
    """Save corpus tiers to disk."""
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)

    questions = []
    for g in GOLD_DOCUMENTS:
        for qa in g["questions"]:
            questions.append({
                "question": qa["q"],
                "answer": qa["a"],
                "type": qa["type"],
                "source_doc": g["id"],
            })

    with open(CORPUS_DIR / "questions.json", "w") as f:
        json.dump(questions, f, indent=2)
    print(f"Saved {len(questions)} questions")

    for tier, docs in tiers.items():
        tier_dir = CORPUS_DIR / f"tier_{tier}"
        tier_dir.mkdir(exist_ok=True)
        for doc in docs:
            fname = f"{doc['id']}.txt"
            with open(tier_dir / fname, "w") as f:
                f.write(f"TITLE: {doc['title']}\n\n{doc['content']}")

        manifest = {
            "tier": tier,
            "total_docs": len(docs),
            "gold": sum(1 for d in docs if d["type"] == "gold"),
            "trap": sum(1 for d in docs if d["type"] == "trap"),
            "noise": sum(1 for d in docs if d["type"] == "noise"),
        }
        with open(tier_dir / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)

        print(f"Tier {tier}: {len(docs)} docs (gold={manifest['gold']}, "
              f"trap={manifest['trap']}, noise={manifest['noise']})")


if __name__ == "__main__":
    print("Building bedrock corpus tiers...")
    tiers = build_corpus_tiers(max_tier=7)
    save_corpus(tiers)
    print("\nDone. Corpus saved to", CORPUS_DIR)
