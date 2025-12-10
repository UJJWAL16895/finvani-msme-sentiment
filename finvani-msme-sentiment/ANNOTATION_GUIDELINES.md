# Annotation Guidelines: MSME Financial Sentiment Analysis

## 1. Overview
This document guides the annotation of financial news headlines for two classification tasks:
1.  **Sentiment**: Is the news Positive, Negative, or Neutral for the entity/sector?
2.  **MSME Relevance**: Is this news relevant to Micro, Small, and Medium Enterprises (MSMEs)?

## 2. Labels

### A. Sentiment
| Label | Description |
| :--- | :--- |
| **POS** (Positive) | News indicating growth, profits, beneficial policies, lower rates, or optimism. |
| **NEG** (Negative) | News indicating losses, restrictions, higher rates, penalties, or pessimism. |
| **NEU** (Neutral) | Factual reporting, market updates without clear bias, or mixed signals balancing each other out. |

### B. MSME Relevance
| Label | Description |
| :--- | :--- |
| **RELEVANT** | Content directly mentions MSMEs, SMEs, startups, collateral-free loans, Mudra scheme, RBI policies for small biz, or GST changes affecting small traders. |
| **NOT_RELEVANT** | General macroeconomic news (unless explicitly flagged for MSME impact), stock market updates of large caps, international relations, personal finance. |

---

## 3. Annotation Examples (25 Samples)

| ID | Headline | Sentiment | MSME Relevance | Reasoning |
| :--- | :--- | :--- | :--- | :--- |
| 1 | "RBI mandates banks to increase lending to MSME sector by 15%." | POS | RELEVANT | Direct benefit (more lending) to MSMEs. |
| 2 | "GST Council to waive off late fees for small taxpayers filing returns." | POS | RELEVANT | Relief for small taxpayers (often MSMEs). |
| 3 | "Inflation rises to 6.5%, raw material costs burden small manufacturers." | NEG | RELEVANT | Inflation hurting small manufacturers. |
| 4 | "Sensex crashes 1000 points amid global sell-off." | NEG | NOT_RELEVANT | General market news, not specific to MSME operations. |
| 5 | "Government launches PLI scheme for large automobile giants." | POS | NOT_RELEVANT | explicitly for "large" giants; trickle-down is too indirect. |
| 6 | "Startup Mahakumbh to showcase innovation from tier-2 cities." | POS | RELEVANT | Startups and tier-2 biz are core MSME constituents. |
| 7 | "SBI hikes home loan interest rates by 25 basis points." | NEG | NOT_RELEVANT | Personal finance (home loans), not business loans. |
| 8 | "Small tea growers demand better procurement prices from government." | NEG | RELEVANT | "Demand" implies dissatisfaction/struggle; small growers = MSME. |
| 9 | "Flipkart empowers 5 lakh sellers ahead of festive season." | POS | RELEVANT | Sellers on e-comm are typically MSMEs. |
| 10 | "Corporate tax collection surges 20% in Q3." | POS | NOT_RELEVANT | Macro fiscal news, no direct impact on small biz sentiment stated. |
| 11 | "Lendingkart raises funds to disburse loans to small businesses." | POS | RELEVANT | Fintech lending to small business. |
| 12 | "Cement prices likely to remain stable this quarter." | NEU | NOT_RELEVANT | Sector specific, neutral sentiment, low relevance unless construction MSME. |
| 13 | "RBI imposes penalty on cooperative bank for non-compliance." | NEG | RELEVANT | Coop banks often serve MSMEs; regulatory penalty is negative. |
| 14 | "Exports from MSME sector dip by 5% in November." | NEG | RELEVANT | Direct negative statistic for the sector. |
| 15 | "Government extends interest subvention scheme for exporters." | POS | RELEVANT | Policy benefit for exporters (many are MSME). |
| 16 | "Reliance industries announces AGM date." | NEU | NOT_RELEVANT | Large cap corporate announcement. |
| 17 | "Compliance burden high for small firms: Survey." | NEG | RELEVANT | "High burden" is negative; "small firms" = MSME. |
| 18 | "Rupee hits all-time low against US Dollar." | NEG | RELEVANT | (Edge Case) Generally relevant as it raises import costs for small manufacturing, though macro. Mark RELEVANT if implies input cost hike. |
| 19 | "SIDBI partners with fintechs to speed up loan processing." | POS | RELEVANT | SIDBI is the apex body for MSMEs. |
| 20 | "Mudra loan NPAs rise, raising concern for banks." | NEG | RELEVANT | High NPAs make future borrowing harder for MSMEs. |
| 21 | "New portal launched for Udhyam registration." | NEU | RELEVANT | Factual launch of infrastructure for MSMEs. |
| 22 | "Gold prices surge to new high." | POS | NOT_RELEVANT | Commodity news, mostly investment/personal. |
| 23 | "Lack of skilled labor hitting textile units in Surat." | NEG | RELEVANT | Operational challenge for textile units (MSME hub). |
| 24 | "Finance Minister to present budget on Feb 1." | NEU | NOT_RELEVANT | Factual event schedule, no sentiment yet. |
| 25 | "Cabinet approves 50,000 cr fund for self-reliant India." | POS | RELEVANT | Usually entails MSME support (Atmanirbhar Bharat). |

---

## 4. Edge Cases & Instruction

### A. Indirect Relevance
**Example**: "Steel prices hiked by 10%."
*   **Label**: RELEVANT (if context implies input cost) or NOT_RELEVANT (if generic).
*   **Rule**: If in doubt, label **NOT_RELEVANT** unless the headline mentions "Input costs", "Raw material", or "SMEs hit".

### B. Mixed Sentiment
**Example**: "Revenue grows, but margins shrink for small retailers."
*   **Label**: NEG (Profitability matters more than revenue for survival).
*   **Rule**: Prioritize **Profit/Survival** over Volume/Revenue.

### C. Policy Announcements vs. Implementation
**Example**: "Govt *plans* to launch support scheme."
*   **Label**: POS (Sentiment is driven by optimism).
*   **Rule**: Announcements of support are **POS**. Delays in implementation are **NEG**.

### D. "Mudra" and "GST"
Keywords like "Mudra", "GST compensation", "Udyam", "SIDBI", "Khadi" are strong indicators of **RELEVANT**.
