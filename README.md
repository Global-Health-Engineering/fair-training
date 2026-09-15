# fair-training

Application materials for **FAIR by doing**, a proposal to the ETH FAIR Competence Funding (2nd call).

## The call

The ETH FAIR Competence Funding supports projects that build FAIR (Findable, Accessible, Interoperable, Reusable) competence at ETH Zurich and strengthen the ETH Data Stewardship Network (DSN). This is the 2nd call.

- **Applicants:** Lars Schöbitz (corresponding) and Adriana Clavijo Daza, Global Health Engineering, D-MAVT.
- **Due:** 15 September 2026, 17:00 CET, submitted as a PDF to openscience@sl.ethz.ch using the official template.
- **Submitted:** 15 September 2026. See the submission record below.
- **Funding cap:** CHF 50,000. This proposal requests CHF 49,880, all direct cost.
- **Duration:** 12 months from 1 February 2027.

## The proposal in brief

A 12-month programme that trains 15 ETH researchers to make their own research data FAIR and to declare their use of AI tools, by doing it. Each participant takes a dataset of their own from a raw file to a published, citable data package. The cohort is mixed by department, career stage, and discipline, so the programme can treat FAIR practice as something that differs by community and data type rather than as one generic skill set. Five taught workshops (24 hours) cover Git and GitHub/GitLab collaboration, FAIR data sharing, task and project management, agentic AI workflows, and FAIR data management, alongside a full-day workshop on organisational change for open science hosted with Greg Wilson. Participants use agentic AI tools on their own data, and the programme works out how to declare AI use in a way that goes beyond ticking a box and shows what researchers still produced themselves.

For a fuller, scannable overview, see [comms/proposal-summary.md](comms/proposal-summary.md).

## Submission record

- The completed template is [`references/FAIR-Seed-Funding-2ndcall-Template-lschoebitz.docx`](references/FAIR-Seed-Funding-2ndcall-Template-lschoebitz.docx). It is the source of the submitted PDF, and `proposal/proposal.qmd` mirrors it section by section.
- The submitted PDF is [`references/FAIR-Seed-Funding-2ndcall-Template-lschoebitz.pdf`](references/FAIR-Seed-Funding-2ndcall-Template-lschoebitz.pdf), rendered from the completed template.
- The state of the repository at submission is tagged as release `v1.0.0` on `main`.
- The work plan tables (work packages, activities with milestones and research questions, budget, budget justification) live in a public Google Sheet that anyone can view and comment on: https://docs.google.com/spreadsheets/d/14DwpPjRWP73SPWMIgO_EpxFua7xIOAcl6iq3-ivrgK0. Table 2 is attached to the proposal as an annex.
- How AI was used in writing the proposal is declared in section 4.2 of the proposal and in full in [`proposal/ai-use-statement.md`](proposal/ai-use-statement.md). The record behind that statement is the commit history and the `prompts/` folder.

## Documents in this repository

### `proposal/`

- [`proposal.qmd`](proposal/proposal.qmd) - the proposal itself, in Quarto, mapped one to one onto the official template sections. For the submitted version the completed template is the source and the qmd was synced to match it. `quarto render` gives a plain DOCX for reading.
- [`ai-use-statement.md`](proposal/ai-use-statement.md) - the full declaration of how AI was used in preparing the application, written from the repository's own record: what the applicants did, what Claude Code drafted, the commit and prompt trail, and the personal data that went through the tools. Section 4.2 of the proposal carries the short version and links here.
- [`differentiation-notes.md`](proposal/differentiation-notes.md) - working notes on how the programme differs from, and complements, the DSN and the RDM Summer School.

### `comms/`

- [`proposal-summary.md`](comms/proposal-summary.md) - one-page stakeholder summary of the proposal.
- [`commitment-sheet.md`](comms/commitment-sheet.md) - participant commitment sheet.
- [`recruitment-plan.md`](comms/recruitment-plan.md) - plan for recruiting the 15 participants.
- [`interest-form.md`](comms/interest-form.md) - field specification for the expression-of-interest form, with the selection criteria the answers feed.

### `data/` and `tools/`

- [`data/read_sheets_data.R`](data/read_sheets_data.R) - reads the four work plan and budget Google Sheets into `data/tables/` as CSV. The sheets are the source of truth for the tables.
- [`tools/fill_template.py`](tools/fill_template.py) - fills the official DOCX template from `proposal.qmd` and `data/tables/`.
- [`tools/build_review.py`](tools/build_review.py) - builds the side-by-side cut review page used to shorten the draft; `tools/cuts.json` records the shortened drafts and their rationale.

### `prompts/`

One file per prompt behind an AI-assisted change, verbatim, with the timestamp, the model, and the files it touched. The matching commit carries a `Prompts:` trailer with the file ids and an `Assisted-by:` trailer naming the model; commits by the applicants alone carry `Human-authored: true`. This is the record the AI use statement points to.

### `references/`

- [`FAIR-Competence-Funding-2ndcall-guidelines-final.pdf`](references/FAIR-Competence-Funding-2ndcall-guidelines-final.pdf) - the call guidelines, including the evaluation criteria.
- [`FAIR-Seed-Funding-2ndcall-Template.docx`](references/FAIR-Seed-Funding-2ndcall-Template.docx) - the official submission template, blank.
- [`FAIR-Seed-Funding-2ndcall-Template-lschoebitz.docx`](references/FAIR-Seed-Funding-2ndcall-Template-lschoebitz.docx) - the completed template as submitted.
- [`FAIR-Seed-Funding-2ndcall-Template-lschoebitz.pdf`](references/FAIR-Seed-Funding-2ndcall-Template-lschoebitz.pdf) - the PDF as submitted on 15 September 2026.
- [`annex-activities.md`](references/annex-activities.md) - list of events where the underlying workflow has been presented.
- [`initial-draft.md`](references/initial-draft.md) - the first outline of the programme idea.
- [`initial-email.md`](references/initial-email.md) - the early note to the FAIR Coalition contact that opened the conversation.
