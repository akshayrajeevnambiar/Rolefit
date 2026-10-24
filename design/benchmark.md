# Benchmark

RoleFit answers one question: across the descriptions you are actually considering, which skills come up, and which of those are missing from your résumé? The quote under each gap is the line that asked for the skill.

Teal and Huntr are the products a job seeker would open for this job. Linear is not a job tool. It is the craft reference for a dense screen that is mostly type. RoleFit is an open-source portfolio project, so their pricing, plans, and signup funnels are out of scope on purpose.

Public docs checked for this note: Teal’s Job Matcher help article (July 2026) and résumé-match page, Huntr’s keyword-extraction article and job-tracker page. Linear is judged from the public app at linear.app, not from a private audit.

## Teal

Teal is a commercial job-search suite: a tracker, a résumé builder, and a Job Matcher. The matcher compares one résumé with one job. You pick a saved job, a job from their board, or a description you paste. Keywords already on the résumé are marked included. Missing keywords are marked missing. Their help article colors those two states green and red. A free account sees a limited keyword list. Teal+ sees the full list. Their match tool also produces a score from 0 to 100, and the product will draft a résumé bullet from a missing keyword.

What works for this use case: the description and the résumé are compared in one place, and the result says whether a word is already on the résumé.

What works against it: the comparison is one job at a time, so you never learn that PostgreSQL is in five of the six roles you care about. A score invites people to add words until the number moves, including words they cannot defend in an interview. The full answer sits behind a paid plan. A missing keyword is a tag. It does not quote the sentence, so a passing mention and a requirement look the same.

Borrow: keep the description and the résumé status together, and say in words whether you list the skill.

Leave: the score, the “write me a bullet” action, green/red chips as the whole interface, and every plan and upgrade.

## Huntr

Huntr is a job-application tracker built as a kanban board. The default stages are Wishlist, Applied, Interview, Offer, and Rejected. A card holds the description, contacts, and documents. That is a clear model if the question is where each application stands. Keyword extraction exists. Their help center groups terms into hard skills, soft skills, knowledge, education, and industry, then offers a keyword match score. The same article suggests about 70% coverage as a target for a résumé.

What works for this use case: the source description stays attached to the job, and the extracted terms are grouped instead of dumped in one list.

What works against it: a board answers “what stage is this application in?” RoleFit’s question is “what does this set of roles keep asking for?” Keywords still belong to one card. There is no count across the set. A coverage target has the same stuffing problem as Teal’s score. A row of columns is a wide desktop layout and a poor way to read on a phone.

Borrow: the pasted text stays on screen next to what was extracted. Categories stay a short closed list (Language, Library, Data, Tool, Practice), which is the useful part of their grouping.

Leave: stages, contacts, the map, documents, the match percentage, and plan gates.

## Linear

Linear is an issue tracker for software teams. Nothing in it is about résumés. It is here because the screen has to be dense without looking like a template.

What is worth taking, from the public app: the chrome is type, alignment, and hairline rules. Color is rare. Lists scan. Metadata is quiet. Empty states are a sentence and one next action. Focus is obvious. Navigation is words.

What would be a mistake to copy: the object in Linear is an issue moving through a workflow. Copying that would turn RoleFit into another application tracker, which is Huntr’s job. Linear’s marketing site uses strong color and gradients. That is a homepage. RoleFit does not have one in this design. Linear’s accent is a violet. Proof does not use it.

Borrow: hairlines instead of shadows, rectangular controls, an empty state with a single next action, numbers that line up, and a table when the data is a ranking.

Leave: the issue workflow, the command palette as an identity, the violet, and a dark-mode-first chrome. Long pasted text is easier to read on a light ground. One theme is the whole MVP.

## What RoleFit takes from this

The screen is a proof of a set of descriptions. You paste the source, the skills are marked in that source, Market ranks them by how often they were named, and Gaps quotes the line. There is no match score, because a score answers a different and worse question. There is no pricing, because this is a local open-source tool, not a suite to sell.
