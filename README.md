# Codex Game Studios

Codex Game Studios is a Codex plugin that turns a workspace into a structured
game development studio. It packages 73 workflow skills, 49 role context cards,
studio process docs, templates, rules, and safety hooks for guiding a game from
concept through release.

This repository was migrated from the original Claude Code Game Studios
template. The Codex plugin entry points are now the standard root-level plugin
paths, while legacy directories are kept only as migration references.

## What's Included

| Category | Count | Location | Purpose |
| --- | ---: | --- | --- |
| Skills | 73 | `skills/` | Guided workflows such as `start`, `brainstorm`, `setup-engine`, `dev-story`, `code-review`, and `release-checklist` |
| Role cards | 49 | `agents/` | TOML context cards for directors, leads, specialists, and engine experts |
| Hooks | 12 scripts | `hooks/`, `hooks.json` | Session context, commit/push checks, asset checks, skill-change reminders, and compaction support |
| Studio docs | 40+ | `docs/studio/` | Workflow catalog, coordination rules, templates, coding standards, and review gates |
| Rules | 11 | `docs/rules/` | Path-scoped standards for gameplay, engine, UI, networking, tests, data, and docs |

## Plugin Structure

```text
.codex-plugin/
  plugin.json              # Codex plugin manifest
skills/                    # Codex skills, one folder per workflow
agents/                    # Role context cards in TOML
hooks.json                 # Hook configuration
hooks/                     # Hook scripts
docs/studio/               # Studio workflow docs and templates
docs/rules/                # Path-scoped rule documents
docs/engine-reference/     # Godot, Unity, and Unreal reference notes
design/                    # Game design artifacts created by workflows
production/                # Sprint, milestone, QA, and release artifacts
src/                       # Game source code
```

## How To Use

Install or load this repository as a Codex plugin. The manifest at
`.codex-plugin/plugin.json` points Codex at `./skills/` and `./hooks.json`.

Start with the `start` skill for a new project. It detects whether an engine,
game concept, source code, prototypes, design docs, or production artifacts
already exist, then routes you to the right workflow.

Common workflow skills:

- `start` - guided onboarding
- `brainstorm` - develop a game concept
- `setup-engine` - choose and configure Godot, Unity, or Unreal
- `map-systems` and `design-system` - build the design specification
- `create-architecture` and `architecture-decision` - define architecture and ADRs
- `create-epics`, `create-stories`, and `sprint-plan` - prepare production work
- `dev-story`, `story-readiness`, and `story-done` - implement and close stories
- `code-review`, `qa-plan`, `smoke-check`, and `regression-suite` - review and test
- `release-checklist`, `launch-checklist`, `changelog`, and `patch-notes` - ship

## Role Context Cards

The `agents/*.toml` files are role context cards, not a promise that Codex will
register 49 named runtime agents automatically. Skills can read these files when
they need a specialist perspective. For example, implementation workflows can
load `agents/lead-programmer.toml`, while design workflows can load
`agents/game-designer.toml` or `agents/creative-director.toml`.

When a skill says to use a named specialist, the Codex-compatible behavior is:
read the matching TOML role card, apply that role's review criteria in the
current session, and use Codex subagents only when the active environment exposes
that capability.

## Hooks

`hooks.json` uses portable plugin-root paths and calls scripts under `hooks/`.
The migrated hook set keeps the safer lifecycle and validation checks:

- session context and gap detection
- commit and push validation
- asset validation
- skill-change reminders
- pre/post compaction state handling
- session stop logging

Claude-specific subagent audit hooks are retained as script files for reference
but are not wired in `hooks.json`.

## Migration Notes

The legacy `.claude/`, `.agents/`, `.codex/`, and `CLAUDE.md` migration sources
have been removed after verification. The standard Codex plugin paths are the
root-level `.codex-plugin/`, `skills/`, `agents/`, `hooks/`, and `hooks.json`.

## License

MIT License. See `LICENSE` for details.
