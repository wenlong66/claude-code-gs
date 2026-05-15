# Codex Game Studios -- Game Studio Agent Architecture

Codex Game Studios is a Codex plugin for structured indie game development.
It provides 73 skills and 49 role context cards across design, engineering,
art, audio, narrative, QA, production, and release.

## Plugin Entry Points

- Plugin manifest: `.codex-plugin/plugin.json`
- Skills: `skills/*/SKILL.md`
- Role context cards: `agents/*.toml`
- Hooks: `hooks.json` and `hooks/*.sh`
- Studio workflow docs: `docs/studio/`
- Path-scoped rules: `docs/rules/`

## Technology Stack

- **Engine**: [CHOOSE: Godot 4 / Unity / Unreal Engine 5]
- **Language**: [CHOOSE: GDScript / C# / C++ / Blueprint]
- **Version Control**: Git with trunk-based development
- **Build System**: [SPECIFY after choosing engine]
- **Asset Pipeline**: [SPECIFY after choosing engine]

Engine-specialist role cards exist for Godot, Unity, and Unreal. Use the set
matching the configured engine in `docs/studio/technical-preferences.md`.

## Project References

- Project structure: `docs/studio/directory-structure.md`
- Engine reference: `docs/engine-reference/godot/VERSION.md`
- Technical preferences: `docs/studio/technical-preferences.md`
- Coordination rules: `docs/studio/coordination-rules.md`
- Coding standards: `docs/studio/coding-standards.md`
- Context management: `docs/studio/context-management.md`

## Collaboration Protocol

This plugin is user-driven, not autonomous. Every substantive task follows:
Question -> Options -> Decision -> Draft -> Approval.

- Skills should present concrete choices before making product or architecture decisions.
- File edits should be previewed or summarized before being written when the skill workflow requires approval.
- Multi-file changes should list the affected files before implementation.
- Commits are never made without explicit user instruction.

If the project has no engine configured and no game concept, start with the
`start` skill to run guided onboarding.
