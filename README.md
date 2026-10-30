# Under (anti-over) engineering Agent Skills

Two skills that prevent unnecessary complexity while planning and find it in
completed code. They focus on redundant service and database calls, work added
without agreement, and safeguards for hypothetical problems.

The skills use the [Agent Skills format](https://agentskills.io/specification).
Codex and Claude Code can install the full plugin, including a session hook.
OpenCode and other compatible agents can install the skills with the
[`skills` CLI](https://github.com/vercel-labs/skills).

## Install

### OpenCode and other agents

Requires Node.js, npm, and Git. Install both skills globally for OpenCode:

```sh
npx skills add rubinho-m/lean-agent-skills --agent opencode --global --yes
```

For another agent, omit `--agent opencode` to choose from the installer's supported
agents. Omit `--global` to install into the current project. To inspect the package
before installation:

```sh
npx skills add rubinho-m/lean-agent-skills --list
```

Start a new session and ask the agent to load the skill by name:

```text
Use lean-grilling to help me design ...
Use overengineering-review on <MR/PR URLs>. Agreed plan: <source>.
```

This installation includes skills only. OpenCode does not run the Codex/Claude
`hooks/hooks.json` file. To pair an existing `grilling` skill automatically,
add this rule to your project's `AGENTS.md` (or the agent's equivalent persistent
instructions file):

```text
Whenever grilling is used, directly or through another workflow, load and apply
lean-grilling before preparing question rounds and confirming the final plan.
```

OpenCode reads `AGENTS.md` as project instructions. Other clients need support for
Agent Skills and persistent instructions; this package cannot add those features
to an arbitrary CLI. See [OpenCode skills](https://docs.opencode.ai/docs/skills/)
and [rules](https://docs.opencode.ai/docs/rules/).

### Codex

Requires a recent Codex CLI with `codex plugin` commands and Git:

```sh
codex plugin marketplace add rubinho-m/lean-agent-skills && codex plugin add lean-agent-skills@rubinho-m
```

Start a new session. Review and trust the plugin's `SessionStart` hook through
`/hooks`; Codex does not run a new hook before approval. Installation does not
change hook trust settings. The plugin is also available in the desktop app when
it shares the same local configuration.

```text
$lean-agent-skills:lean-grilling Help me design ...
$lean-agent-skills:overengineering-review <MR/PR URLs> Agreed plan: <source>.
```

### Claude Code

Requires a recent Claude Code with plugin support and Git:

```sh
claude plugin install lean-agent-skills --marketplace https://github.com/rubinho-m/lean-agent-skills.git
```

Start a new session or run `/reload-plugins`. Both skills and the shared
`SessionStart` hook load from the same package. Check installation with
`claude plugin list`.

```text
/lean-agent-skills:lean-grilling Help me design ...
/lean-agent-skills:overengineering-review <MR/PR URLs> Agreed plan: <source>.
```

The Codex/Claude plugin requires no additional Python, Node.js, MCP servers,
API keys, or services. Its hook runs only the shell's built-in `echo` command.

## Compatibility checks

OpenCode 1.19.5 discovered both skills installed by `skills` CLI 1.7.4 in an
isolated project. Claude Code 2.1.312 passed strict plugin validation. These
checks cover installation and discovery, not model behavior in a conversation.

## What the skills do

`lean-grilling` works on its own and alongside an existing `grilling` skill. It
filters questions before each round, checks the simplest sufficient solution,
shows the material cost of decisions, and requests one independent review before
final plan approval. If subagents are unavailable, it discloses that limitation
and checks the plan itself without calling that review independent.

The Codex/Claude session hook instructs the agent to load the companion whenever
`grilling` is used. Other agents can receive the same instruction through the
project rule above. The model applies the checks; neither a hook nor a rule
proves that a plan contains no overengineering.

`overengineering-review` examines the full diff against the target branch, traces
calls across multiple MRs, and compares behavior with the user's agreed decisions.
It produces a report without changing code or creating tasks. Necessary security,
authorization, and data integrity checks remain part of the solution.

Skill instructions are currently written in Russian. You can request answers in
your preferred language; the README and installation instructions are in English.

## Update and uninstall

For skills installed through the `skills` CLI:

```sh
npx skills update --global
npx skills remove lean-grilling overengineering-review --agent opencode --global --yes
```

The update command updates all globally installed skills. Omit `--global` for a
project installation. Removing skills does not remove a rule you added to
`AGENTS.md`; remove that rule if you no longer use the companion.

Codex:

```sh
codex plugin marketplace upgrade rubinho-m && codex plugin add lean-agent-skills@rubinho-m
codex plugin remove lean-agent-skills@rubinho-m
```

Start a new session after updating. If Codex requests another review of a changed
hook, approve it through `/hooks`.

Claude Code:

```sh
claude plugin marketplace update rubinho-m && claude plugin update lean-agent-skills@rubinho-m
claude plugin uninstall lean-agent-skills@rubinho-m
```

Uninstalling the plugin leaves other plugins in the `rubinho-m` marketplace
intact. The package does not overwrite manually installed personal skills or
hooks. If you already have those copies, check for duplicates before use.

## Credits

The planning discussion is based on
[`grilling`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md)
by [Matt Pocock](https://github.com/mattpocock), licensed under MIT. Attribution
also appears in the `lean-grilling` skill's `metadata.credits` field.
Complexity filtering, decision cost tracking, and change review are additions
in this package. Package license: [MIT](LICENSE).

## Development

Python 3 is required to run the package checks:

```sh
python3 -m unittest discover -s tests -v
```

Before a release, update `version` in both `plugin.json` and
`.claude-plugin/plugin.json`, then run the checks. Both manifests share `skills/`
and `hooks/hooks.json`; do not declare the hook again in either manifest.
Validate the Claude Code package with `claude plugin validate . --strict`.

Installation and format references:
[Codex plugins](https://developers.openai.com/plugins/build/plugins),
[Codex CLI](https://learn.chatgpt.com/docs/cli/reference),
[Codex hook trust](https://learn.chatgpt.com/docs/hooks),
[Claude Code plugins](https://code.claude.com/docs/en/plugins-reference),
[Claude Code plugin commands](https://code.claude.com/docs/en/plugins/cli-reference).

This repository is a Git marketplace for plugin installation. It is not a
submission to OpenAI's official plugin directory.
