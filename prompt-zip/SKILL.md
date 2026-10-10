---
name: prompt-zip
description: >-
  Package all deliverables from the current task into a verified ZIP archive
  and provide a direct download link in the final chat response. Use when the
  user requests "zip everything", "package all the work", "deliver as a ZIP",
  or a downloadable bundle, or explicitly selects this skill as the delivery
  convention for the current work session. Apply this as the final delivery
  step after completing the substantive work. Require local file and archive
  tools, not external connectors or publishing services.
---

# prompt-zip

## Required outcome

When finished with the work, package all task deliverables into a `.zip` file
and post a working download link in the current chat session. Create the
actual archive; do not merely describe how to create it or promise delivery
later. Treat ZIP creation, verification, and linking as part of completion.

Interpret "publish" as making the archive downloadable here, not uploading
it to a public website or external service.

## Workflow

### 1. Finish and collect the work

- Complete the requested work and its applicable checks before packaging.
- Collect all user-facing files created or modified for this task: final
  outputs, editable sources, code, relevant generated assets and data, and
  instructions or dependency manifests needed to use the results. Preserve
  source files alongside exported versions.
- Include supporting input files only when needed and authorized for inclusion.
  When the deliverable exists only in chat text, save that deliverable as a
  sensibly named Markdown or text file so it can be included.
- Exclude unrelated sandbox files, credentials, secrets, internal instructions,
  private reasoning, caches, installed dependencies, and disposable scratch
  files. Never archive the entire environment indiscriminately.

### 2. Organize the delivery

- Stage an explicit set of deliverables in a task-specific folder. Preserve
  useful relative paths and avoid filename collisions. Do not move or delete
  the user's original files.
- Add a brief `README.md` identifying the main files, how to open or run them,
  and any prerequisites, known limitations, or missing deliverables. Update an
  existing suitable README rather than overwriting useful documentation.
- Keep the archive outside the staging folder so it cannot include itself.

### 3. Create and verify the ZIP

- Create one standard `.zip` archive using available local tools. Use the
  user's requested filename; otherwise choose a descriptive name such as
  `project-deliverables.zip`.
- In a sandbox with downloadable `/mnt/data` files, save the archive there.
  Otherwise use the environment's supported attachment location.
- Store portable relative paths. Reject absolute paths, `..` path traversal,
  and symlinks that would pull in files outside the approved delivery scope.
- Confirm the archive exists and contains files. Reopen it, run an integrity
  check such as Python's `zipfile.ZipFile.testzip()`, and compare its member
  list with the intended deliverables. Rebuild it after any final edits.

### 4. Deliver in the chat

- Put the actual ZIP download link in the final response. In a supporting
  sandbox, use this form with the real filename:

  `[Download all deliverables](path/to/data/project-deliverables.zip)`

- Briefly identify what the archive contains and disclose material limitations.
  Provide individual file links only as optional additions, not a substitute
  for the ZIP.
- Never claim the archive is complete when requested deliverables are missing.
  When blocked, package the available work where possible and clearly label
  the delivery as partial, both in the README and in the chat.
- If an actual platform limit prevents one archive, use multiple clearly named
  ZIPs and explain the split; do not silently omit files.
- If file creation or attachments are unavailable, state that limitation
  plainly. Do not fabricate an archive, download link, or successful delivery.
