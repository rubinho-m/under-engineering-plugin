# Under Engineering Plugin

Two skills and bundled hook that prevent unnecessary complexity while planning and find it in
completed code. They focus on redundant service and database calls, work added
without agreement, and safeguards for hypothetical problems.

## What the plugin does

`lean-grilling` builds on [grilling](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md)
by [Matt Pocock](https://github.com/mattpocock), adding checks for unnecessary complexity during planning.

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

## Install

### OpenCode and other agents

Requires Node.js, npm, and Git. Install both skills globally for OpenCode:

```sh
npx skills add rubinho-m/under-engineering-plugin --agent opencode --global --yes
```

For another agent, omit `--agent opencode` to choose from the installer's supported
agents. Omit `--global` to install into the current project. To inspect the package
before installation:

```sh
npx skills add rubinho-m/under-engineering-plugin --list
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
codex plugin marketplace add rubinho-m/under-engineering-plugin && codex plugin add under-engineering-plugin@rubinho-m
```

Start a new session. Review and trust the plugin's `SessionStart` hook through
`/hooks`; Codex does not run a new hook before approval. Installation does not
change hook trust settings. The plugin is also available in the desktop app when
it shares the same local configuration.

```text
$under-engineering-plugin:lean-grilling Help me design ...
$under-engineering-plugin:overengineering-review <MR/PR URLs> Agreed plan: <source>.
```

### Claude Code

Requires a recent Claude Code with plugin support and Git:

```sh
claude plugin install under-engineering-plugin --marketplace https://github.com/rubinho-m/under-engineering-plugin.git
```

Start a new session or run `/reload-plugins`. Both skills and the shared
`SessionStart` hook load from the same package. Check installation with
`claude plugin list`.

```text
/under-engineering-plugin:lean-grilling Help me design ...
/under-engineering-plugin:overengineering-review <MR/PR URLs> Agreed plan: <source>.
```

The Codex/Claude plugin requires no additional Python, Node.js, MCP servers,
API keys, or services. Its hook runs only the shell's built-in `echo` command.

## Update and uninstall

If you installed version 0.1.3, remove its previous ID before installing the
renamed plugin with the commands above:

```sh
# Codex
codex plugin remove underengineering-agent-skills@rubinho-m
# Claude Code
claude plugin uninstall underengineering-agent-skills@rubinho-m
```

For versions before 0.1.3, use `lean-agent-skills@rubinho-m` as the old ID in
those removal commands.

The standalone skill names (`lean-grilling` and `overengineering-review`) have
not changed; installations through the `skills` CLI need no migration.

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
codex plugin marketplace upgrade rubinho-m && codex plugin add under-engineering-plugin@rubinho-m
codex plugin remove under-engineering-plugin@rubinho-m
```

Start a new session after updating. If Codex requests another review of a changed
hook, approve it through `/hooks`.

Claude Code:

```sh
claude plugin marketplace update rubinho-m && claude plugin update under-engineering-plugin@rubinho-m
claude plugin uninstall under-engineering-plugin@rubinho-m
```

Uninstalling the plugin leaves other plugins in the `rubinho-m` marketplace
intact. The package does not overwrite manually installed personal skills or
hooks. If you already have those copies, check for duplicates before use.
