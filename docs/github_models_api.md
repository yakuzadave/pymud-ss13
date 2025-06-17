# GitHub Models API

The documentation generation workflow relies on an AI model. To verify which models are available you can query the GitHub Models API. Replace `<YOUR-TOKEN>` with a personal access token that has the `models:read` permission.

```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://models.github.ai/catalog/models
```

A successful response looks like this:

```json
[
  {
    "id": "openai/gpt-4.1",
    "name": "OpenAI GPT-4.1",
    "publisher": "OpenAI",
    "summary": "gpt-4.1 outperforms gpt-4o across the board, with major gains in coding, instruction following, and long-context understanding",
    "rate_limit_tier": "high",
    "supported_input_modalities": ["text", "image", "audio"],
    "supported_output_modalities": ["text"],
    "tags": ["multipurpose", "multilingual", "multimodal"]
  }
]
```

Each object in the array contains information about a model, including its identifier, publisher, and supported modalities. Use the `id` field when specifying a model in a workflow. For example, the documentation job uses `openai/gpt-4`.
