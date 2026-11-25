# ZJU-OmniAI organization profile

This repository maintains the public GitHub organization homepage at <https://github.com/ZJU-OmniAI>.

- `profile/README.md`: the organization profile.
- `profile/assets/`: banner, research map, divider, and link buttons, each in a light and a dark version, plus project cover images in `covers/`.
- `tools/`: the generator for those SVG graphics.
- `metrics/` and `scripts/`: the automatically refreshed Hugging Face download totals.
- `people/`: the people page (`people/README.md`), laid out like zjureal.com/people.html and generated from `people/people.json` by `INTER_DIR=... NOTO_SC_DIR=... python3 tools/build_people.py` (same fonts as the profile graphics). Groups, in order: Faculty · 教员, Postdocs · 博士后, Research Engineers · 工程师, PhD Students · 博士生, Master's Students · 硕士生; empty groups are hidden. Only list people the team confirms. Put photos in `people/photos/` and set each person's `photo` to the file name; without one the card shows initials. `group_photos` (also in `people/photos/`) rotate in the hero. Person fields: name, name_zh, title, year, works, homepage, scholar (full URL), github, email. Its links on the homepage (navigation row and footer) are commented out for now; uncomment them in `profile/README.md` to show the page again. The page itself stays reachable by URL.

GitHub renders `profile/README.md` from the default branch of the public `ZJU-OmniAI/.github` repository. Relative image paths resolve against `profile/`. See [GitHub's organization-profile documentation](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile).

## Page layout

1. Banner, badges (organization stars, followers, and team model/dataset/total Hugging Face downloads), and a one-line introduction.
2. **News**: media coverage only (no paper releases or acceptance notices). One line per article, newest first: month, the outlet as a code tag, the original article title linked, the project repository, and its project page.
3. **Featured Projects**: six cards, each with a 16:9 cover, venue, model/dataset download badges where the project has official releases, a star badge, a one-sentence description, and links.
4. **Research Map**: the generated overview figure, then one table per research direction. Every row keeps its model downloads, dataset downloads, and GitHub stars badges under the links; projects inside Embodied-Omni show the repository-wide `Embodied-Omni stars`. Reading lists and tools keep their star badges.
5. **Tools for Research & Work**: research tools, kept separate from papers.
6. Footer with link buttons.

## Maintaining the profile

1. Date paper releases by the public paper date and acceptance announcements by the confirmed announcement month.
2. Put each work in one primary research direction. Keep Reasoner, Navigator, and Memory-Bench within the Embodied-Omni series and link directly to their subdirectories.
3. Add only publicly available paper, code, model, dataset, and project-page links. Resource collections belong below the relevant research table.
4. Verify conference acceptance in the project's official repository or publication record. Use `arXiv YEAR` when no venue is confirmed.
5. When a project is added or removed from a research direction, update `DIRECTIONS` in `tools/build_profile_assets.py` and rebuild the research map so the figure and the tables agree.
6. Covers are 16:9. Prefer an 8-second looping animated WebP (640×360, 12 fps, about 2 MB or less) cut from the group's own real-robot or real-deployment footage that shows the technical difficulty (for example real-environment navigation, dual-arm parcel handling, multi-task real-robot montages). Avoid toy-like tabletop clips or AI-generated footage when real footage exists. Never use footage filmed by partner companies or third parties. Projects without suitable video keep a 1200×675 JPEG figure. Every video cover carries the ZJU-OmniAI Lab watermark: cut the clip to 640×360 PNG frames at 12 fps with ffmpeg, then run `python3 tools/watermark_covers.py FRAME_DIR profile/assets/covers/NAME.webp` (a slanted grid of small translucent marks sliding diagonally over the whole frame, two larger marks drifting on separate paths, and a fixed corner badge; every motion loops with the clip).

## Rebuilding the graphics

Text in the SVGs is converted to outlines so it renders the same for every viewer. The generator uses Inter and Noto Sans SC (both SIL OFL 1.1) from the Fontsource packages `@fontsource-variable/inter` and `@fontsource-variable/noto-sans-sc`:

```sh
pip install fonttools brotli
INTER_DIR=.../@fontsource-variable/inter/files \
NOTO_SC_DIR=.../@fontsource-variable/noto-sans-sc/files \
python3 tools/build_profile_assets.py
```

## Suggested public repository pins

In order: **Embodied-Omni**, **vla-corrector**, **Spatial-Interactor**, **ProVisE**, **GFT**, **Data-Copilot**.

This selection places the two embodied directions first, followed by spatial cognition, evaluation, learning methods, and a representative agent system. Organization owners can customize six public pins from the organization Overview page.

## Research scope

OmniAI's positioning is **from the digital world to the physical world**, with the loop **perceive → reason → act → remember** (keep this order in every graphic and sentence). The six directions are an editorial organization of the group's public work. In the research map they are grouped as the digital world (Trustworthy Multimodal Intelligence; Reasoning & Reinforcement Learning; Autonomous Agents & Tool Use) and the physical world (Spatial Intelligence & World Models; Embodied Brain; Embodied Cerebellum), each column read top to bottom as perceive, reason, act. The tables below the map keep the embodied directions first because the embodied cerebellum and embodied brain are the group's main line.

The current world-model entry is a reading resource. GFT studies LLM reasoning post-training; MGAP and OMNEX-VL study multimodal grounding/hallucination. They are placed in their respective learning and multimodal directions.

VLA-Δ (action learning) and VLA-Rolling (efficient action-chunk inference) sit with VLA-Corrector under Embodied Cerebellum. Scene-Designer (agentic 3D scene generation) sits under Spatial Intelligence. DTCA (RL for diffusion language models) sits under Reasoning & RL and links to arXiv 2610.35201.

Source verification date: 2026-11-21. Project repositories and paper links are provided in the profile next to the corresponding work.
