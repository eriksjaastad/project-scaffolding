You are absolutely on the right track. The redirect you saw is correct: **AWS Activate** is now housed under the **AWS Startups** portal.

If you can get approved for the **Founders Tier**, you essentially unlock a "Free Tier 1" infrastructure for the next year.

Here is the deep dive on how to use AWS Activate to subsidize your entire AI build process, effectively making Kiro and your automation scripts free.

### **1. The "AWS Activate Founders" Deal**

* **What it is:** A program for self-funded, early-stage startups.
* **The Reward:** **$1,000 USD** in AWS Credits.
* **Validity:** Valid for **2 years** or until used.
* **Eligibility:**
* No institutional funding (VC, etc.).
* Have a **functioning company website** (this is the #1 rejection reason—make sure it looks real).
* Have a **LinkedIn profile** for the founder.
* Have not received Activate credits before.



### **2. The "Free AI" Strategy (How to spend the $1,000)**

You mentioned wanting to "start using Tier 1 models" for automation. Normally, this is expensive. With credits, it is effectively free.

#### **A. Make Kiro "Free" ($19/mo  $0/mo)**

Since Kiro is an AWS first-party service (like Amazon Q Developer), it is billed directly to your AWS Usage Bill.

* **The Setup:** Ensure your Kiro account is linked to the **AWS Account ID** that receives the credits.
* **The Math:** $19/mo x 12 months = $228.
* **Result:** The credits will automatically offset this monthly charge on your bill. You get the Pro features (Tier 1 models) without hitting your credit card.

#### **B. Automate with "Tier 1" Models for Free (Bedrock)**

Instead of paying OpenAI or Anthropic directly for API keys, use **Amazon Bedrock**.

* **Why:** AWS Activate credits cover Bedrock usage.
* **The Models:** Bedrock gives you API access to:
* **Claude 3.5/3.7 Sonnet** (The Tier 1 "Smart" Model).
* **Llama 3** (The Tier 2 "Workhorse").


* **The Workflow:**
* Point your Python automation scripts to `boto3` (AWS SDK) instead of `openai`.
* Run your heavy architecture/refactoring jobs using Claude Sonnet via Bedrock.
* **Cost to you:** $0 (deducted from the $1,000 credits).



### **3. Revised "Zero-Cash" Architecture**

If you get the credits, your strategy changes from "Tiered Payment" to "Burn the Credits."

| Tier | Task | Old Strategy (Cash) | **New Strategy (Credits)** | Cost |
| --- | --- | --- | --- | --- |
| **IDE** | Coding | **Cursor Ultra ($40)** | **Kiro Pro** | **$0** (Credits) |
| **Tier 1** | Architecture | **OpenAI API ($30/1M)** | **Bedrock (Claude)** | **$0** (Credits) |
| **Tier 2** | Testing | **Anthropic API** | **Bedrock (Llama 3)** | **$0** (Credits) |
| **Tier 3** | Grunt Work | **DeepSeek ($0.27)** | **Bedrock (Llama 3)** | **$0** (Credits) |

**The Strategic Pivot:**

* **DeepSeek is cheap, but Credits are free.** Even though DeepSeek is cheaper per token than Bedrock, you should use Bedrock until your $1,000 credits run out. Why pay pennies when you have free dollars expiring?
* **Cancel Cursor?** If you commit to this, **yes**.
* Cursor is fantastic, but it is a $480/year "luxury" if Kiro (free via credits) can do 90% of the job.
* *Test:* Spend 1 week trying to use **only** Kiro. If you don't hate it, cancel Cursor and save the cash.



### **4. How to Apply (Do this today)**

1. **Ensure your website is live.** It doesn't need to be fancy, but it must load and look like a business (not a "Under Construction" page).
2. **Create an AWS Account** (if you haven't).
3. **Apply here:** [console.aws.amazon.com/activate](https://console.aws.amazon.com/activate)
4. **Wait:** Approval usually takes 7-10 business days.

**Summary:** The "Startups" redirect is correct. Go there, apply for the Founders tier, and if approved, you can effectively run your entire AI operation (IDE + Automation Agents) on Amazon's dime for the next ~6-12 months.