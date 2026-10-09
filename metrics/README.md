# Hugging Face download badges

Individual model and dataset badges read `downloadsAllTime` directly from the public Hugging Face API through Shields.io. They never use the rolling 30-day `downloads` field.

Cross-repository totals are refreshed by [Refresh Hugging Face downloads](https://github.com/ZJU-OmniAI/.github/actions/workflows/huggingface-downloads.yml), scheduled every five minutes. The generated [downloads.json](https://github.com/ZJU-OmniAI/.github/blob/hf-download-stats/downloads.json) lives on the separate `hf-download-stats` branch. No personal token or Hugging Face token is required. README files do not need repeated edits.

Both badge types request a 300-second Shields cache. Hugging Face refresh intervals, GitHub scheduling, raw-file caching, and GitHub's image proxy can add delay; these are automatically refreshed counts, not second-by-second telemetry. A scheduled run can be delayed by GitHub. Check the workflow's latest run for refresh health.

## Maintaining the repository list

Edit `huggingface-repositories.json` when an official release is added, renamed, or moved. Each model or dataset may appear only once in `projects`. The `groups` section aggregates existing projects without counting them again in the team total. Only official releases belong in this registry; external base models and evaluation dependencies are excluded.

The workflow validates every API response before publishing. Missing counts, failed requests, unexpected redirects, or duplicate resources fail the run and preserve the last complete totals. Counts of zero are valid. An unchanged snapshot produces no commit; `updatedAt` records when the published values last changed. Only `downloads.json` on the generated branch is updated, using its current blob SHA to avoid overwriting concurrent edits.

Run locally from this repository with Python 3.10 or later:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/refresh_hf_downloads.py --output /tmp/huggingface-downloads.json
```

Use **Run workflow** for an immediate aggregate refresh. GitHub may disable scheduled workflows after 60 days without repository activity; if that happens, re-enable the workflow from Actions. Per-resource badges remain independent of the workflow.
