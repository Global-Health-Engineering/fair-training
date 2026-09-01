# Differentiation from ETH Library RDM offerings

Lars's direction, recorded 2026-09-01, to work into the proposal before submission. This answers the board question the Open Science office flagged when consulted: does the DSN or the RDM Summer School already cover this? The answer must be explicit in sections 2.1, 2.2, 2.4 (risk), and 2.5.

## The core claim

The ETH Library RDM Summer School and the RDM workshop series and our programme serve different people and do different work. They do not overlap; ours starts where theirs ends.

## The five differentiators

1.  Theory versus practice. The RDM Summer School and the RDM workshop series teach theory and background. Our programme is hands-on and practical: each participant works on their own real dataset and takes it to a published, citable FAIR data package.

2.  Novices versus people with RDM responsibility. The Library offerings address novices in RDM. We recruit people who already hold RDM responsibility in their group or role. This is the professionalisation angle from the ETH Domain Measure 5 work on career paths for open research data professionals: we upskill people who already carry the responsibility, rather than introducing beginners to the basics. [Links to wiki/research/rdm-rse-careers-eth-domain in the vault.]

3.  Basics versus larger questions. We address larger questions the introductory offerings do not reach, in particular discipline-specific and community-specific FAIR requirements. Different communities and different data types need different data-sharing and data-security practice. This is the community-specific FAIR practice the FCF call prioritises, drawn from the openwashdata experience.

4.  AI-use declaration as a running thread. Throughout the programme we critically assess the contribution to thinking and standards around declaring AI use in scientific research. No ETH Library RDM offering does this. It is a current, open question in research integrity, and running a year-long programme with fifteen researchers who use AI-assisted workflows on their own data is a place to develop and test standards for declaring that use.

5.  The cohort is a test group and generates research results. The fifteen participants are not only trainees. They are a test group: the programme is a study of how FAIR data sharing, data security, and AI-use declaration differ across disciplines and communities. The cohort produces research results at the same time as it produces fifteen published data packages. This reframes the programme as scientific work with an output, not only a training service, which strengthens sections 2.2 (innovative aspect) and 2.5 (added value and new knowledge).

## Where each point goes in the proposal

- 2.1 (relevance and target community): points 2 and 3. State that the target community is ETH researchers who already hold RDM responsibility, and that the mixed cohort exists to surface discipline- and community-specific FAIR requirements.
- 2.2 (specific effort, innovation): points 1, 4, and 5. The hands-on practical delivery, the AI-use-declaration thread, and the cohort as a test group that generates research results are the innovative aspects.
- 2.4 (risk, overlap mitigation): the whole file. When the board asks about DSN or Summer School overlap, answer with the five differentiators: different audience (responsibility-holders, not novices), different mode (hands-on, not theory), larger questions (community-specific, AI declaration), and a research output. We complement the Library offerings and feed lessons back to the DSN; we do not duplicate them.
- 2.5 (added value): points 4 and 5. The programme contributes new thinking on AI-use declaration standards and produces research results on community-specific FAIR practice, both of which the Library offerings do not produce. This is added value to ETH, not a second copy of an existing course.

## Framing note

Do not attack the Library offerings. The programme is positioned as the practical, professionalising layer above the Library's introductory theory, feeding lessons back to the DSN. That keeps the DSN relationship (which the call requires us to support) constructive while making the non-duplication case.

## Prior work and stakeholder engagement (recorded 2026-09-01)

This programme is not starting from scratch. Early-stage versions of the proposal and the training approach have already been shared with, and supported by, the ETH stakeholders whose buy-in the FAIR Board looks for. State this in section 1.2 (ongoing ETH activities, named engagement) and section 2.4 (feasibility, tested material).

- Shared with the ETH Library and with SwissRN. Early-stage proposals were shared with the ETH Library and within the Swiss Reproducibility Network (SwissRN). Lars is himself the SwissRN Local Node Leader for ETH Zurich (since 2025), so the SwissRN link is an internal role, not an external contact. Daniel Stekhoven leads the reproducibility-levels framework work within SwissRN (the Reprolevel paper), which connects into the GFRN AI-disclosure work; he is a collaborator, not the ETHZ node lead. [Corrected 2026-09-01: earlier draft wrongly named Stekhoven as the node lead.]

- The DSN and SwissRN have supported previous workshops. The Data Stewardship Network and SwissRN supported earlier gitforsci and agentsforsci workshops, which built training material that this FAIR training programme reuses. That material has already been tested once and is being further refined for this programme. This gives the feasibility case concrete evidence: the workshops exist, were run with ETH support, and the material is proven and improving. [TODO name which gitforsci and agentsforsci workshops, roughly when they ran, and how the DSN and SwissRN supported them.]

- GHE has already run rbtl, a full course of the same kind, three times. rbtl is "Research Beyond the Lab: Open Science and Research Methods for a Global Engineer", designed and taught by Lars Schöbitz and Elizabeth (Liz) Tilley at Global Health Engineering (D-MAVT). It was offered for the first time in spring 2022 and taught again in spring 2024 and spring 2025, so three runs. Over a semester, students develop their own research project, learn the quantitative methods to collect data from people, work with data using tidyverse R packages, use Git and GitHub for version control and collaboration, and write and communicate with Quarto, applying open science principles throughout. All course materials are published as Open Educational Resources under permissive licences on GitHub (organisations rbtl-fs22, rbtl-fs24, rbtl-fs25; the FS22 site is at <https://rbtl-fs22.github.io/website/>, FS25 at <https://rbtl-fs25.github.io/website/>). This is direct evidence that the "design a project, collect your own data, take it to FAIR with hands-on data science tooling" model already works at ETH, taught three times, with real students and real data, inside D-MAVT. [TODO confirm the exact student numbers per run if you want a cohort figure in the proposal; the three runs and the OER output are already verified from the GHE website.]

Why this matters for the proposal:

- Section 1.2: it shows active, named engagement with ETH services and initiatives (Library, DSN, SwissRN) and concrete beneficiaries (rbtl students, gitforsci and agentsforsci participants), which criterion 1.2 rewards directly.
- Section 2.4: it de-risks feasibility. The material is already built and tested once; this call refines and extends it, rather than inventing it. Pair this with the existing openwashdata and ds4owd track record.
- It also answers the overlap question from a second angle: the approach has been developed and supported by the DSN and SwissRN themselves, so it complements rather than duplicates what those bodies do.

## Teaching artifact for the agentic-workflow workshop and the AI-declaration thread (2026-09-01)

A concrete method to teach in the eight-hour agentic-workflow workshop, and a live example of the AI-declaration thread: Hadley Wickham's three-file workflow (a cleaning script, a YAML data dictionary, and a Parquet file, kept in sync through an AI agent, with a Git commit after each change so every AI edit is visible in the diff and reversible). It makes AI-assisted data cleaning auditable, and it teaches data dictionaries as the reusability artifact that makes data both FAIR and AI-ready. Wickham's framing that you write down what you know about the data so the agent can help, the same documentation that always helped human colleagues, is a good teaching hook for section 2.2. Recorded in the vault at wiki/tech/ai-feedback-loops-for-data-science (transcript stored under ingested/transcripts/, out of git).
