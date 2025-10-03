6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

Sign In | Subscribe


Technology’s generational moment with
generative AI: A CIO and CTO guide

July 11, 2023 | Article

CIOs and CTOs can take nine actions to reimagine business and
technology with generative AI.

DOWNLOADS

 Article (12 pages)

H

ardly a day goes by without some new business-busting development related to

generative AI surfacing in the media. The excitement is well deserved— McKinsey

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

1/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

research  estimates that generative AI could add the equivalent of $2.6 trillion to $4.4 trillion

of value annually.

[ 1 ]

CIOs and chief technology officers (CTOs) have a critical role in capturing that value, but it’s

worth remembering we’ve seen this movie before. New technologies emerged—the

internet, mobile, social media—that set off a melee of experiments and pilots, though

significant business value often proved harder to come by. Many of the lessons learned from

those developments still apply, especially when it comes to getting past the pilot stage to

reach scale. For the CIO and CTO, the generative AI boom presents a unique opportunity to

apply those lessons to guide the C-suite in turning the promise of generative AI into

sustainable value for the business.

Through conversations with dozens of tech leaders and an analysis of generative AI

initiatives at more than 50 companies (including our own), we have identified nine actions all

technology leaders can take to create value, orchestrate technology and data, scale

solutions, and manage risk for generative AI (see sidebar, “A quick primer on key terms”):

1. Move quickly to determine the company’s posture for the adoption of generative

AI, and develop practical communications to, and appropriate access for, employees.

2. Reimagine the business and identify use cases that build value through improved

productivity, growth, and new business models. Develop a “financial AI” (FinAI)

capability that can estimate the true costs and returns of generative AI.

3. Reimagine the technology function, and focus on quickly building generative AI

capabilities in software development, accelerating technical debt reduction, and

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

2/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

dramatically reducing manual effort in IT operations.

4. Take advantage of existing services or adapt open-source generative AI models

to develop proprietary capabilities (building and operating your own generative AI

models can cost tens to hundreds of millions of dollars, at least in the near term).

5. Upgrade your enterprise technology architecture to integrate and manage

generative AI models and orchestrate how they operate with each other and

existing AI and machine learning (ML) models, applications, and data sources.

6. Develop a data architecture to enable access to quality data by processing both

structured and unstructured data sources.

7. Create a centralized, cross-functional generative AI platform team to provide

approved models to product and application teams on demand.

8. Invest in upskilling key roles—software developers, data engineers, MLOps

engineers, and security experts—as well as the broader nontech workforce. But you

need to tailor the training programs by roles and proficiency levels due to the

varying impact of generative AI.

9. Evaluate the new risk landscape and establish ongoing mitigation practices to

address models, data, and policies.

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

3/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

1. Determine the company’s posture for the
adoption of generative AI

As use of generative AI becomes increasingly widespread, we have seen CIOs and CTOs

respond by blocking employee access to publicly available applications to limit risk. In doing

so, these companies risk missing out on opportunities for innovation, with some employees

even perceiving these moves as limiting their ability to build important new skills.

Instead, CIOs and CTOs should work with risk leaders to balance the real need for risk

mitigation with the importance of building generative AI skills in the business. This requires

establishing the company’s posture regarding generative AI by building consensus around

the levels of risk with which the business is comfortable and how generative AI fits into the

business’s overall strategy. This step allows the business to quickly determine company-

wide policies and guidelines.

Once policies are clearly defined, leaders should communicate them to the business, with

the CIO and CTO providing the organization with appropriate access and user-friendly

guidelines. Some companies have rolled out firmwide communications about generative AI,

provided broad access to generative AI for specific user groups, created pop-ups that warn

users any time they input internal data into a model, and built a guidelines page that

appears each time users access a publicly available generative AI service.

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

4/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

2. Identify use cases that build value through
improved productivity, growth, and new
business models

CIOs and CTOs should be the antidote to the “death by use case” frenzy that we already see

in many companies. They can be most helpful by working with the CEO, CFO, and other

business leaders to think through how generative AI challenges existing business models,

opens doors to new ones, and creates new sources of value. With a deep understanding of

the technical possibilities, the CIO and CTO should identify the most valuable opportunities

and issues across the company that can benefit from generative AI—and those that can’t. In

some cases, generative AI is not the best option.

McKinsey research , for example, shows generative AI can lift productivity for certain

marketing use cases (for example, by analyzing unstructured and abstract data for customer

preference) by roughly 10 percent and customer support (for example, through intelligent

bots) by up to 40 percent.

[ 2 ]

 The CIO and CTO can be particularly helpful in developing a

perspective on how best to cluster use cases either by domain (such as customer journey or

business process) or use case type (such as creative content creation or virtual agents) so

that generative AI will have the most value. Identifying opportunities won’t be the most

strategic task—there are many generative AI use cases out there—but, given initial

limitations of talent and capabilities, the CIO and CTO will need to provide feasibility and

resource estimates to help the business sequence generative AI priorities.

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

5/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

Providing this level of counsel requires tech leaders to work with the business to develop a

FinAI capability to estimate the true costs and returns on generative AI initiatives. Cost

calculations can be particularly complex because the unit economics must account for

multiple model and vendor costs, model interactions (where a query might require input

from multiple models, each with its own fee), ongoing usage fees, and human oversight

costs.

3. Reimagine the technology function

Generative AI has the potential to completely remake how the tech function works. CIOs

and CTOs need to make a comprehensive review of the potential impact of generative AI on

all areas of tech, but it’s important to take action quickly to build experience and expertise.

There are three areas where they can focus their initial energies:

Software development:  McKinsey research  shows generative AI coding support

can help software engineers develop code 35 to 45 percent faster, refactor code 20

to 30 percent faster, and perform code documentation 45 to 50 percent faster.

[ 3 ]

Generative AI can also automate the testing process and simulate edge cases,

allowing teams to develop more-resilient software prior to release, and accelerate

the onboarding of new developers (for example, by asking generative AI questions

about a code base). Capturing these benefits will require extensive training (see more

in action 8) and automation of integration and deployment pipelines through

DevSecOps  practices to manage the surge in code volume.

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

6/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

Technical debt:  Technical debt  can account for  20 to 40 percent of technology

budgets  and significantly slow the pace of development.

[ 4 ]

 CIOs and CTOs should

review their tech-debt balance sheets to determine how generative AI capabilities

such as code refactoring, code translation, and automated test-case generation can

accelerate the reduction of technical debt.

IT operations (ITOps): CIOs and CTOs will need to review their ITOps productivity

efforts to determine how generative AI can accelerate processes. Generative AI’s

capabilities are particularly helpful in automating such tasks as password resets,

status requests, or basic diagnostics through self-serve agents; accelerating triage

and resolution through improved routing; surfacing useful context, such as topic or

priority, and generating suggested responses; improving observability through

analysis of vast streams of logs to identify events that truly require attention; and

developing documentation, such as standard operating procedures, incident

postmortems, or performance reports.

4. Take advantage of existing services or adapt
open-source generative AI models

A variation of the classic “rent, buy, or build” decision exists when it comes to strategies for

developing generative AI capabilities. The basic rule holds true: a company should invest in

a generative AI capability where it can create a proprietary advantage for the business and

access existing services for those that are more like commodities.

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

7/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

The CIO and CTO can think through the implications of these options as three archetypes:

Taker—uses publicly available models through a chat interface or an API, with little or

no customization. Good examples include off-the-shelf solutions to generate code

(such as GitHub Copilot) or to assist designers with image generation and editing

(such as Adobe Firefly). This is the simplest archetype in terms of both engineering

and infrastructure needs and is generally the fastest to get up and running. These

models are essentially commodities that rely on feeding data in the form of prompts

to the public model.

Shaper—integrates models with internal data and systems to generate more

customized results. One example is a model that supports sales deals by connecting

generative AI tools to customer relationship management (CRM) and financial

systems to incorporate customers’ prior sales and engagement history. Another is

fine-tuning the model with internal company documents and chat history to act as an

assistant to a customer support agent. For companies that are looking to scale

generative AI capabilities, develop more proprietary capabilities, or meet higher

security or compliance needs, the Shaper archetype is appropriate.

There are two common approaches for integrating data with generative AI models in

this archetype. One is to “bring the model to the data,” where the model is hosted on

the organization’s infrastructure, either on-premises or in the cloud environment.

Cohere, for example, deploys foundation models on clients’ cloud infrastructure,

reducing the need for data transfers. The other approach is to “bring data to the

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

8/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

model,” where an organization can aggregate its data and deploy a copy of the large

model on cloud infrastructure. Both approaches achieve the goal of providing access

to the foundation models, and choosing between them will come down to the

organization’s workload footprint.

Maker—builds a foundation model to address a discrete business case. Building a

foundation model is expensive and complex, requiring huge volumes of data, deep

expertise, and massive compute power. This option requires a substantial one-off

investment—tens or even hundreds of millions of dollars—to build the model and train

it. The cost depends on various factors, such as training infrastructure, model

architecture choice, number of model parameters, data size, and expert resources.

Each archetype has its own costs that tech leaders will need to consider (Exhibit 1). While

new developments, such as efficient model training approaches and lower graphics

processing unit (GPU) compute costs over time, are driving costs down, the inherent

complexity of the Maker archetype means that few organizations will adopt it in the short

term. Instead, most will turn to some combination of Taker, to quickly access a commodity

service, and Shaper, to build a proprietary capability on top of foundation models.

Exhibit 1

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

9/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

5. Upgrade your enterprise technology
architecture to integrate and manage
generative AI models

Organizations will use many generative AI models of varying size, complexity, and capability.

To generate value, these models need to be able to work both together and with the

business’s existing systems or applications. For this reason, building a separate tech stack

for generative AI creates more complexities than it solves. As an example, we can look at a

consumer querying customer service at a travel company to resolve a booking issue (Exhibit

2). In interacting with the customer, the generative AI model needs to access multiple

applications and data sources.

Exhibit 2

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

10/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

11/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

For the Taker archetype, this level of coordination isn’t necessary. But for companies looking

to scale the advantages of generative AI as Shapers or Makers, CIOs and CTOs need to

upgrade their technology architecture. The prime goal is to integrate generative AI models

into internal systems and enterprise applications and to build pipelines to various data

sources. Ultimately, it’s the maturity of the business’s enterprise technology architecture

that allows it to integrate and scale its generative AI capabilities.

Recent advances in integration and orchestration frameworks, such as LangChain and

LlamaIndex, have significantly reduced the effort required to connect different generative AI

models with other applications and data sources. Several integration patterns are also

emerging, including those that enable models to call APIs when responding to a user query

—GPT-4, for example, can invoke functions—and provide contextual data from an external

data set as part of a user query, a technique known as retrieval augmented generation. Tech

leaders will need to define reference architectures and standard integration patterns for

their organization (such as standard API formats and parameters that identify the user and

the model invoking the API).

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

12/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

There are five key elements that need to be incorporated into the technology architecture to

integrate generative AI effectively (Exhibit 3):

Context management and caching to provide models with relevant information

from enterprise data sources. Access to relevant data at the right time is what allows

the model to understand the context and produce compelling outputs. Caching

stores results to frequently asked questions to enable faster and cheaper responses.

Policy management to ensure appropriate access to enterprise data assets. This

control ensures that HR’s generative AI models that include employee compensation

details, for example, cannot be accessed by the rest of the organization.

Model hub, which contains trained and approved models that can be provisioned on

demand and acts as a repository for model checkpoints, weights, and parameters.

Prompt library, which contains optimized instructions for the generative AI models,

including prompt versioning as models are updated.

MLOps platform, including upgraded MLOps capabilities, to account for the

complexity of generative AI models. MLOps pipelines, for example, will need to

include instrumentation to measure task-specific performance, such as measuring a

model’s ability to retrieve the right knowledge.

Exhibit 3

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

13/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

14/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

In evolving the architecture, CIOs and CTOs will need to navigate a rapidly growing

ecosystem of generative AI providers and tooling. Cloud providers provide extensive access

to at-scale hardware and foundation models, as well as a proliferating set of services.

MLOps and model hub providers, meanwhile, offer the tools, technologies, and practices to

adapt a foundation model and deploy it into production, while other companies provide

applications directly accessed by users built on top of foundation models to perform

specific tasks. CIOs and CTOs will need to assess how these various capabilities are

assembled and integrated to deploy and operate generative AI models.

6. Develop a data architecture to enable access
to quality data

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

15/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

The ability of a business to generate and scale value, including cost reductions and

improved data and knowledge protections, from generative AI models will depend on how

well it takes advantage of its own data. Creating that advantage relies on a data architecture

that connects generative AI models to internal data sources, which provide context or help

fine-tune the models to create more relevant outputs.

In this context, CIOs, CTOs, and chief data officers need to work closely together to do the

following:

Categorize and organize data so it can be used by generative AI models. Tech leaders

will need to develop a comprehensive  data architecture  that encompasses both

structured and unstructured data sources. This requires putting in place standards

and guidelines to optimize data for generative AI use—for example, by augmenting

training data with synthetic samples to improve diversity and size; converting media

types into standardized data formats; adding metadata to improve traceability and

data quality; and updating data.

Ensure existing infrastructure or cloud services can support the storage and handling

of the vast volumes of data needed for generative AI applications.

Prioritize the development of data pipelines to connect generative AI models to

relevant data sources that provide “contextual understanding.” Emerging approaches

include the use of vector databases to store and retrieve embeddings (specially

formatted knowledge) as input for generative AI models as well as in-context

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

16/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

learning approaches, such as “few shot prompting,” where models are provided with

examples of good answers.

7. Create a centralized, cross-functional
generative AI platform team

Most tech organizations are on a journey to a  product and platform operating model . CIOs

and CTOs need to integrate generative AI capabilities into this operating model to build on

the existing infrastructure and help to rapidly scale adoption of generative AI. The first step

is setting up a generative AI platform team whose core focus is developing and maintaining

a platform service where approved generative AI models can be provisioned on demand for

use by product and application teams. The platform team also defines protocols for how

generative AI models integrate with internal systems, enterprise applications, and tools, and

also develops and implements standardized approaches to manage risk, such as

responsible AI frameworks.

CIOs and CTOs need to ensure that the platform team is staffed with people who have the

right skills. This team requires a senior technical leader who acts as the general manager.

Key roles include software engineers to integrate generative AI models into existing

systems, applications, and tools; data engineers to build pipelines that connect models to

various systems of record and data sources; data scientists to select models and engineer

prompts; MLOps engineers to manage deployment and monitoring of multiple models and

model versions; ML engineers to fine-tune models with new data sources; and risk experts

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

17/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

to manage security issues such as data leakage, access controls, output accuracy, and bias.

The exact composition of the platform team will depend on the use cases being served

across the enterprise. In some instances, such as creating a customer-facing chatbot,

strong product management and user experience (UX) resources will be required.

Realistically, the platform team will need to work initially on a narrow set of priority use

cases, gradually expanding the scope of their work as they build reusable capabilities and

learn what works best. Technology leaders should work closely with business leads to

evaluate which business cases to fund and support.

8. Tailor upskilling programs by roles and
proﬁciency levels

Generative AI has the potential to massively lift employees’ productivity and augment their

capabilities. But the benefits are unevenly distributed depending on roles and skill levels,

requiring leaders to rethink how to build the actual skills people need.

Our  latest empirical research  using the generative AI tool GitHub Copilot, for example,

helped software engineers write code 35 to 45 percent faster.

[ 5 ]

 The benefits, however,

varied. Highly skilled developers saw gains of up to 50 to 80 percent, while junior

developers experienced a 7 to 10 percent decline in speed. That’s because the output of the

generative AI tools requires engineers to critique, validate, and improve the code, which

inexperienced software engineers struggle to do. Conversely, in less technical roles, such as

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

18/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

customer service, generative AI helps low-skill workers significantly, with productivity

increasing by 14 percent and staff turnover dropping as well, according to one study.

[ 6 ]

These disparities underscore the need for technology leaders, working with the chief human

resources officer (CHRO), to rethink their talent management strategy to build the

workforce of the future. Hiring a core set of top generative AI talent will be important, and,

given the increasing scarcity and strategic importance of that talent, tech leaders should

put in place retention mechanisms, such as competitive salaries and opportunities to be

involved in important strategic work for the business.

Tech leaders, however, cannot stop at hiring. Because nearly every existing role will be

affected by generative AI, a crucial focus should be on upskilling people based on a clear

view of what skills are needed by role, proficiency level, and business goals. Let’s look at

software developers as an example. Training for novices needs to emphasize accelerating

their path to become top code reviewers in addition to code generators. Similar to the

difference between writing and editing, code review requires a different skill set. Software

engineers will need to understand what good code looks like; review the code created by

generative AI for functionality, complexity, quality, and readability; and scan for

vulnerabilities while ensuring they do not themselves introduce quality or security issues in

the code. Furthermore, software developers will need to learn to think differently when it

comes to coding, by better understanding user intent so they can create prompts and

define contextual data that help generative AI tools provide better answers.

Beyond training up tech talent, the CIO and CTO can play an important role in building

generative AI skills among nontech talent as well. Besides understanding how to use

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

19/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

generative AI tools for such basic tasks as email generation and task management, people

across the business will need to become comfortable using an array of capabilities to

improve performance and outputs. The CIO and CTO can help adapt academy models to

provide this training and corresponding certifications.

The decreasing value of inexperienced engineers should accelerate the move away from a

classic talent pyramid, where the greatest number of people are at a junior level, to a

structure more like a diamond, where the bulk of the technical workforce is made up of

experienced people. Practically speaking, that will mean building the skills of junior

employees as quickly as possible while reducing roles dedicated to low-complexity manual

tasks (such as writing unit tests).

9. Evaluate the new risk landscape and
establish ongoing mitigation practices

Generative AI presents a fresh set of ethical questions and risks, including “hallucinations,”

whereby the generative AI model presents an incorrect response based on the highest-

probability response; the accidental release of confidential personally identifiable

information; inherent bias in the large data sets the models use; and high degrees of

uncertainty related to intellectual property (IP). CIOs and CTOs will need to become fluent in

ethics, humanitarian, and compliance issues to adhere not just to the letter of the law (which

will vary by country) but also to the spirit of responsibly managing their business’s

reputation.

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

20/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

Addressing this new landscape requires a significant review of cyber practices and updating

the software development process to evaluate risk and identify mitigation actions before

model development begins, which will both reduce issues and ensure the process doesn’t

slow down. Proven risk-mitigation actions for hallucinations can include adjusting the level

of creativity (known as the “temperature”) of a model when it generates responses;

augmenting the model with relevant internal data to provide more context; using libraries

that impose guardrails on what can be generated; using “moderation” models to check

outputs; and adding clear disclaimers. Early generative AI use cases should focus on areas

where the cost of error is low, to allow the organization to work through inevitable setbacks

and incorporate learnings.

To protect data privacy, it will be critical to establish and enforce sensitive data tagging

protocols, set up data access controls in different domains (such as HR compensation data),

add extra protection when data is used externally, and include privacy safeguards. For

example, to mitigate access control risk, some organizations have set up a policy-

management layer that restricts access by role once a prompt is given to the model. To

mitigate risk to intellectual property, CIOs and CTOs should insist that providers of

foundation models maintain transparency regarding the IP (data sources, licensing, and

ownership rights) of the data sets used.

Generative AI is poised to be one of the fastest-growing technology categories we’ve ever

seen. Tech leaders cannot afford unnecessary delays in defining and shaping a generative

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

21/22

6/25/25, 6:04 PM

A CIO and CTO technology guide to generative AI | McKinsey

AI strategy. While the space will continue to evolve rapidly, these nine actions can help CIOs

and CTOs responsibly and effectively harness the power of generative AI at scale.

How relevant and useful is this article for you?

1. “The economic potential of generative AI: The next productivity frontier,” McKinsey, June 14, 2023.

2. “The economic potential of generative AI: The next productivity frontier,” McKinsey, June 14, 2023.
3. Begum Karaci Deniz, Martin Harrysson, Alharith Hussin, and Shivam Srivastava, “Unleashing developer productivity

with generative AI,” McKinsey, June 27, 2023.

4. Vishal Dalal, Krish Krishnakanthan, Björn Münstermann, and Rob Patenge, “Tech debt: Reclaiming tech equity,”

McKinsey, October 6, 2020.

5. “Unleashing developer productivity with generative AI,” June 27, 2023.
6. Erik Brynjolfsson, Danielle Li, and Lindsey R. Raymond, Generative AI at work, National Bureau of Economic

Research (NBER) working paper, number 31161, April 2023.

ABOUT THE AUTHOR(S)

Aamer Baig  is a senior partner in McKinsey’s Chicago office;  Sven Blumberg  is a senior

partner in the Düsseldorf office; Eva Li is a consultant in the Bay Area office, where Megha

Sinha is a partner; Douglas Merrill is a partner in the Southern California office; Adi Pradhan

and Stephen Xu are associate partners in the Toronto office; and  Alexander Sukharevsky  is a

senior partner in the London office.

The authors wish to thank Stephanie Brauckmann, Anusha Dhasarathy, Martin Harrysson,

Klemens Hjartar, Alharith Hussin, Naufal Khan, Sam Nie, Chandrasekhar Panda, Henning Soller,

https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/technologys-generational-moment-with-generative-ai-a-cio-and-cto-guide

22/22

