## What LM Studio gives you

LM Studio can run a local model *and* expose it as an **OpenAI-compatible API server** on your Mac, typically:

* `http://localhost:1234/v1` ([LM Studio][1])

That means any tool that can talk to “OpenAI-style” endpoints can talk to LM Studio just by changing the **base URL**.

---

## LM Studio setup (Mac, no-terminal version)

1. **Open LM Studio**
2. **Load a model** in the LM Studio UI (whatever you already have installed there)
3. Go to the **Local Server** / **Developer** area and hit **Start Server** (LM Studio docs show this as the local OpenAI-compatible server) ([LM Studio][2])

Optional sanity check (only if you want to verify it’s alive): LM Studio docs show a minimal `curl` call to `…/v1/chat/completions`. ([LM Studio][2])

---

## VS Code: plug LM Studio into Continue (best “local in IDE” experience)

Continue supports **OpenAI-compatible providers** via `apiBase`. ([Continue][3])

In your Continue config, you set:

* `apiBase: http://localhost:1234/v1`
* `apiKey`: can be anything if LM Studio isn’t enforcing one (some setups use a dummy like `lm-studio`)
* `model`: **use the exact model id LM Studio shows you** in its server UI/Documents/examples ([LM Studio][1])

That’s it — now VS Code chats/edits route to LM Studio locally.

---

## Cursor: what works, what doesn’t (with LM Studio)

**Important limitation:** Cursor does a lot of processing on **Cursor’s servers**, so Cursor’s servers **cannot reach your Mac’s `localhost`**, which means “LM Studio at `http://localhost:1234`” won’t work directly. ([Cursor - Community Forum][4])

**The workaround** (if you really want LM Studio inside Cursor):

* Make LM Studio’s OpenAI-compatible server **publicly reachable** (tunnel/reverse proxy), secured with a key, then point Cursor’s **Override OpenAI Base URL** at that public URL. Cursor staff/community have described this approach. ([Cursor - Community Forum][4])

**Reality check:** Cursor’s “override base URL” path has had rough edges/limitations in recent months, and some users report breakage when overriding. ([Cursor - Community Forum][5])

### Practical recommendation for your “spread the load” plan

* **VS Code + Continue = local-first (cheap)**
* **Cursor = bundled / cloud-first (fast + reliable)**
* Only do the Cursor+LM Studio tunnel if you’re okay with “works, but can be fiddly.”

---

If you paste (1) the model name LM Studio shows when the server is running, and (2) whether you’re using Continue already, I can write the exact Continue `config.yaml` block for your setup (still LM Studio only).

[1]: https://lmstudio.ai/Documents/developer/openai-compat?utm_source=chatgpt.com "OpenAI Compatibility Endpoints | LM Studio Docs"
[2]: https://lmstudio.ai/Documents/developer?utm_source=chatgpt.com "LM Studio Developer Docs"
[3]: https://docs.continue.dev/customize/model-providers/top-level/openai?utm_source=chatgpt.com "How to Configure OpenAI Models with Continue"
[4]: https://forum.cursor.com/t/using-local-llms-with-cursor-is-it-possible/15494?page=2&utm_source=chatgpt.com "Using Local LLMs with Cursor: Is it Possible? - Page 2"
[5]: https://forum.cursor.com/t/cannot-override-openai-base-url/144198?utm_source=chatgpt.com "Cannot override OpenAI Base URL - Bug Reports"
