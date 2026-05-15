# Codex Game Studios -- Compatibility Notes

This repository is now a Codex plugin. `CLAUDE.md` is kept as a compatibility
entrypoint for tools or workflows that still look for it, but the canonical
configuration lives in the Codex plugin structure.

## Primary Codex Plugin Entry Points

- Plugin manifest: `.codex-plugin/plugin.json`
- Skills: `skills/*/SKILL.md`
- Role context cards: `agents/*.toml`
- Hooks: `hooks.json` and `hooks/*.sh`
- Studio workflow docs: `docs/studio/`
- Path-scoped rules: `docs/rules/`

## Project Structure

@docs/studio/directory-structure.md

## Engine Version Reference

@docs/engine-reference/godot/VERSION.md

## Technical Preferences

@docs/studio/technical-preferences.md

## Coordination Rules

@docs/studio/coordination-rules.md

## Collaboration Protocol

**User-driven collaboration, not autonomous execution.**
Every task follows: **Question -> Options -> Decision -> Draft -> Approval**.

- Skills should present concrete options before product or architecture decisions.
- File edits should be previewed or summarized before being written when the workflow requires approval.
- Multi-file changes should list the affected files before implementation.
- No commits without user instruction.

## Coding Standards

@docs/studio/coding-standards.md

## Context Management

@docs/studio/context-management.md
