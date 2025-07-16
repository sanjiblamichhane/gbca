# GBCA - GivingbackAI Cofounder Agent 🤖🤝

**tl;dr**
- Like a human cofounder but AI. Think of it as a **YC AI Agent: The Lean Startup Mentor** 🚀
- Pronounced: "jee-bee-caa"
---

#### **1. High-Level Objective 🎯**

- To create an interactive AI mentor that guides a founder from a raw idea 💡 to a **scalable, revenue-generating business** 📈 by applying principles of Lean Startup, growth marketing, sales, and product management.
- The agent will act as a Socratic partner and an operational assistant, helping founders not just validate ideas but also **grow revenue 💸, acquire customers 🎯, and manage their product ⚙️.**

---

#### **2. Core Functionalities ✨**

1.  **Guided Onboarding 🗺️:** Structures a user's initial idea into a testable framework (like a Business Model Canvas).
2.  **Hypothesis Management 🧪:** Helps the user identify and prioritize their riskiest assumptions (value hypothesis, growth hypothesis).
3.  **Experiment Design 🔬:** Assists in creating MVPs (Minimum Viable Products) and customer discovery experiments to test hypotheses.
4.  **Learning Synthesis 🧠:** Takes user-provided data (interview notes, survey results) and helps synthesize it into "validated learnings."
5.  **Stateful Progression 📈:** Remembers where the founder is in the journey and suggests the next logical action.
6.  **Growth Engine Design 🌱:** Helps founders brainstorm, prioritize, and execute growth experiments based on the "Traction" framework.
7.  **Revenue & Sales Support 💰:** Assists with pricing strategies, drafting sales emails, and managing a lightweight sales pipeline.
8.  **Product Management Assistant 📋:** Helps categorize user feedback, prioritize feature development using frameworks like RICE, and draft product specs.
9.  **KPI Dashboard & Analysis 📊:** Tracks key metrics (MRR, Churn, LTV, CAC) and provides weekly summaries and alerts on significant changes.

---

#### **3. System Architecture: Brain, Memory, and Tools 🏗️**

This system requires a more sophisticated memory and toolset than a simple evaluator. It will be an interactive, stateful agent.

---

#### **4. Component Deep-Dive 🔍**

**A) Brain (The LLM) 🧠**
*   **Technology:** **Anthropic's Claude 3 Opus** or **OpenAI's GPT-4o** 🤖. Claude 3 Opus is particularly well-suited due to its strong reasoning, long context window, and tendency to follow complex, multi-step instructions reliably.
*   **Function:** Evolves from a "Lean Startup Coach" to a "COO/Head of Growth" 🧑‍💼. It decides when to focus on validation vs. growth vs. revenue optimization.

**B) Memory 💾**

*   **1. Long-Term Memory (The "Library") 📚 - *Expanded***
    *   **Technology:** **Qdrant** or **Pinecone** Vector Database 🗄️.
    *   **New Content:** We will add new knowledge sources:
        *   **Growth 🌱:** "Traction" by Gabriel Weinberg, essays from Andrew Chen, and Reforge content on growth loops.
        *   **Sales 💼:** "SPIN Selling" by Neil Rackham, articles on SaaS pricing models and B2B sales funnels.
        *   **Product 📦:** "Inspired" by Marty Cagan, guides on writing PRDs (Product Requirement Documents), and RICE/ICE prioritization frameworks.
    *   **Function:** When a founder asks, "How should I price my SaaS product? 🏷️", the agent can now retrieve and synthesize advice from established pricing strategy experts.

*   **2. User-Specific Memory (The "Project File") 🗂️ - *Expanded***
    *   **Technology:** **Google Sheets** or **Airtable** 📊.
    *   **New Structure:** The agent will add new tabs to the user's project file as they mature:
        *   `Growth Experiments`: To track marketing tests (Channel, Hypothesis, Cost, Results).
        *   `Revenue Dashboard`: A simple log of monthly revenue, new customers, and churn.
        *   `Product Roadmap`: A list of features to be built, with columns for a RICE score.
    *   **Function:** This becomes the company's operational dashboard, managed and analyzed by the AI.

**C) Tools (The Agent's Capabilities) 🛠️ - *Expanded***
We add a suite of new, more operationally-focused tools.

1.  **`getBusinessState(user_id)`**
    *   **Description:** Reads the user's entire Google Sheet to understand their current progress before starting a conversation.
    *   **n8n Node:** Google Sheets Tool (`Get Rows`).

2.  **`updateBusinessModelCanvas(user_id, section, content)`**
    *   **Description:** Asks the user questions about their business and updates the 'Business Model Canvas' tab in their sheet.
    *   **n8n Node:** Google Sheets Tool (`Update Row(s)`).

3.  **`draftCustomerInterviewScript(hypotheses)`**
    *   **Description:** Generates a set of open-ended, non-leading questions to help a founder test their hypotheses, using principles from "The Mom Test" queried from the Vector DB.
    *   **n8n Node:** A chain involving a Qdrant query followed by an LLM call ➡️📝.

4.  **`logInterviewInsights(user_id, interview_notes)`**
    *   **Description:** Appends a new row to the 'Interview Notes' tab with a summary of a customer conversation provided by the user.
    *   **n8n Node:** Google Sheets Tool (`Append Row`) ➕.

5.  **`synthesizeLearnings(user_id)`**
    *   **Description:** Reads all rows from the 'Interview Notes' and 'Experiment Results' tabs and uses the LLM to identify patterns, contradictions, and validated learnings. This is the core of the "Learn" step.
    *   **n8n Node:** A chain: Google Sheets (`Get Rows`) -> LLM Call -> Google Sheets (`Update Row` to log the synthesis) 📈.

6.  **`suggestNextStep(current_state)`**
    *   **Description:** Based on the synthesized learnings, this tool recommends the next action (e.g., "Pivot the customer segment," "Persevere and build the next feature," "Test pricing").
    *   **n8n Node:** LLM call.

7.  **`suggestGrowthExperiment(goal)`**
    *   **Description:** Based on the founder's goal (e.g., "increase user signups"), it queries the "Traction" knowledge base and suggests 3 testable experiments.
    *   **n8n Node:** Qdrant Query -> LLM Call.

8.  **`draftMarketingCopy(channel, audience, offer)`**
    *   **Description:** Generates compelling copy for a specific marketing channel (e.g., a Google Ad 📢, a cold email ✉️, a landing page headline).
    *   **n8n Node:** LLM Call ✍️.

9.  **`updateRevenueDashboard(user_id, month, mrr, churn)`**
    *   **Description:** Prompts the user for their monthly metrics and logs them in the `Revenue Dashboard` tab.
    *   **n8n Node:** Google Sheets Tool (`Append Row`).

10. **`analyzeKPIs(user_id)`**
    *   **Description:** Reads the `Revenue Dashboard`, calculates key metrics, and provides a plain-language summary. E.g., "Your MRR grew 15% this month, which is great! However, your churn rate also increased from 3% to 5%. Let's investigate why 🤔."
    *   **n8n Node:** Google Sheets (`Get Rows`) -> Code Node (for calculations) -> LLM Call (for summary).

11. **`prioritizeFeatures(user_id)`**
    *   **Description:** Reads the `Product Roadmap` and user feedback, applies the RICE framework, and suggests the most impactful feature to build next.
    *   **n8n Node:** Complex chain: Google Sheets (`Get Rows`) -> LLM Call (to score features) -> Google Sheets (`Update Rows` with scores) 🥇🥈🥉.

---

#### **5. User Interaction Flow (Extended Scenario) 🔄**

*The founder has achieved initial product-market fit with their first 10 customers.*

1.  **Agent Initiates Growth Phase 🚀:**
    *   **Agent:** "Congratulations on hitting 10 paying customers! 🎉 This is a huge milestone. It suggests we've found product-market fit. The focus now shifts from validation to **growth**. Are you ready to build a repeatable system for acquiring customers?"
2.  **Brainstorming Growth 🧠:**
    *   **User:** "Yes! Where do we start?"
    *   **Agent (using `suggestGrowthExperiment`):** "Based on your B2B software, the three most promising channels to test first are likely Content Marketing ✍️, Cold Email Outreach ✉️, and Targeted LinkedIn Ads 🎯. Which one feels most aligned with your skills?"
3.  **Executing an Experiment 🧪:**
    *   **User:** "Let's try Cold Email."
    *   **Agent (using `draftMarketingCopy`):** "Great. I've drafted three versions of a cold email for you to test. I've also added them to your `Growth Experiments` tab in your project file. Your goal is to send these to 50 potential leads this week and track the response rate."
4.  **Measuring and Learning from Revenue 💰:**
    *   *One month later...*
    *   **Agent (on a weekly trigger 🗓️):** "It's the start of the new month! Time to update your KPIs. What was your revenue and churn for last month?"
    *   User provides the data. The agent uses `updateRevenueDashboard` and then `analyzeKPIs`.
    *   **Agent:** "Thanks! I've updated the dashboard. It looks like your cold email experiment brought in 5 new customers, giving it a CAC of $50 per customer. This is a very promising channel! Let's discuss how we can double down on this. 💪"
