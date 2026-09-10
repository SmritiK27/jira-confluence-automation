# Validate Instruction Files

Use this instruction to review every `*.agent.md` file in `instructions/` for
the Single Responsibility Principle (SRP).

## Procedure

1. List all `instructions/*.agent.md` files.
2. Read each file completely before assessing it.
3. Identify the file's primary responsibility.
4. List the distinct responsibilities described by the file.
5. Decide whether those responsibilities form one cohesive task.
6. Note unrelated responsibilities, duplicated guidance, or overlap with another
   instruction file.
7. Check whether the filename accurately describes the primary responsibility.
8. Recommend one action: **Keep**, **Split**, **Rename**, or **Consolidate**.

Do not modify the instruction files during this review. Report observations and
recommendations only.

## SRP Criteria

Mark a file as **Compliant** when its instructions serve one cohesive purpose,
even if that purpose contains several closely related steps.

Mark a file as **Needs review** when it combines unrelated workflows, has more
than one independent reason to change, or duplicates another file's primary
guidance.

Treat minor naming concerns as recommendations, not as SRP violations.

## Output

Write a Markdown report using this structure:

```markdown
# Instruction SRP Verification Report

## Summary

- Files reviewed: <count>
- SRP compliant: <count>
- Needs review: <count>

## <filename>

- **Primary responsibility:** <one sentence>
- **SRP status:** Compliant / Needs review
- **Responsibilities found:**
  - <responsibility>
- **Unrelated or overlapping responsibilities:** <none or details>
- **Recommendation:** Keep / Split / Rename / Consolidate
- **Suggested changes:** <specific action or none>

## Overall Recommendations

- <cross-file recommendation>
```

Include every discovered instruction file, including this file if it is present
when the review runs. Distinguish clear SRP violations from minor naming or
overlap concerns, and support findings with concise references to the file
content.
