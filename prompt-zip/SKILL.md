---
name: prompt-zip
description: Collect authorized task deliverables into a verified ZIP archive and provide its actual download link. Use when the user requests a downloadable bundle, delivery as a ZIP, or packaging all completed work. Confirm the deliverable set, then create and verify the archive using available local tools.
license: MIT
metadata:
  author: "SYSETUP.COM CarlosHRG"
---

# prompt-zip

Create the archive and verify it before claiming delivery. Making it downloadable in the current session does not authorize uploading it to an external service.

## Collect the authorized deliverables

Confirm the final deliverables and their applicable check results from the supplied files or conversation. Package them directly with available local tools; no prior authoring workflow or other skill is required. Select the final outputs, editable sources, relevant assets or data, and instructions needed to use them. Include supporting inputs only when necessary and authorized. Save chat-only deliverables to files when file output is available. Identify unfinished or missing deliverables before claiming a complete bundle.

Exclude credentials, secrets, private reasoning, internal instructions, unrelated files, caches, installed dependencies, and scratch outputs. Use an explicit file set rather than archiving the environment.

Build an explicit mapping of source regular files to portable relative member names, sorted by member name. Reject symlinks, including symlinked path components, special files, unreadable files, and sources outside authorized roots. If dereferencing is explicitly required, verify the resolved target and its authorization before staging it as a regular file. Stage copies in a new private directory without moving or deleting originals; freeze this snapshot before packing. Add a brief usage note only when needed to explain entrypoints, prerequisites, limitations, or partial delivery.

## Create and verify the archive

Choose the requested filename or a descriptive name. Verify an authorized writable destination and the platform's actual download or attachment mechanism before choosing the delivery path; do not assume a particular sandbox directory exists.

Preserve an existing destination by choosing an unused versioned filename unless replacement was explicitly authorized. Keep the archive outside the staging folder and input set. Reject absolute or drive-qualified member names, backslashes, empty or dot components, parent traversal, and duplicate names, including collisions after Unicode normalization or case folding for portable extraction. Preserve distinct subdirectories rather than flattening files or silently keeping the last collision.

Create a candidate at a new path; publish it as the final archive only after verification. Reopen it, confirm it is nonempty, run an integrity check such as Python's `zipfile.ZipFile.testzip()`, and compare the full member list, count, sizes, and streamed member bytes against the frozen source mapping. Set equality alone misses duplicate members; streaming bounds memory without extracting files. Rebuild and repeat verification after final edits or a changed source. On a read, write, space, or verification failure, preserve originals and any prior verified archive, identify the failed candidate, and do not offer it as a verified download.

For example, `guide/usage.md` and `reference/usage.md` keep their directories; two different sources both mapped to `usage.md` require disambiguation before packing. A preexisting `delivery.zip` leads to a new unused version name. An escaping link or failed integrity check stops delivery; it does not become an implicit omission from a complete bundle.

## Deliver truthfully

Return the actual supported download or attachment link for the verified archive and briefly identify its contents. Never substitute a guessed URL or an example path. Individual file links may supplement the ZIP.

If deliverables are missing, label the archive and response as partial. If platform limits require multiple archives, name the parts and explain the split without silently omitting files.

When file creation or downloadable attachments are unavailable, state the specific limitation and provide the usable result the environment supports. Do not claim that an archive, attachment, or working link exists without evidence.

Use [the evaluation cases](evals/evals.json) when reviewing unsafe mappings, failed verification, and unavailable delivery tools.
