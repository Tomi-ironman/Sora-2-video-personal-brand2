# Styles Presets

This folder contains JSON style presets used by `scripts/video_creation/style_engine.py`.

Each style file has:
- name
- clip_pattern (optional)
- pacing: hook_duration, story_duration, text_duration, personal_duration
- text: mode, fontsize, position
- transitions (reserved)
- grade: filter (ffmpeg -vf filter string)

Use via `create_video_master.py` by passing `style_name` (filename without .json).
