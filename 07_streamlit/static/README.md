# Streamlit static assets

Files in this folder are served by Streamlit at `/app/static/<filename>`
when `server.enableStaticServing = true` (set in `.streamlit/config.toml`).

## Hero video (optional)

Drop a short, muted, looping mp4 here named **`hero-video.mp4`** and it
will automatically render as the hero background in the dashboard. The
app falls back to a CSS-animated water ambience (droplets + flowing
wave) if the file is missing, so the dashboard always looks good out of
the box.

Recommended specs for the hero video:

- Format: `.mp4` (H.264) — broadly supported, small file size
- Dimensions: 1920×1080 or 1280×720, aspect ratio ~16:9
- Duration: 8–15 seconds, seamless loop
- File size: keep under ~4 MB so the dashboard stays snappy on
  Streamlit Community Cloud
- Audio: no audio track (the element is muted anyway, but stripping
  audio saves bytes)
- Content: abstract water / coastline / flowing network — nothing too
  busy, since text overlays the video

Two quick ways to source a usable clip:

1. Pull a clip from the Aqualia corporate website / YouTube and trim
   with `ffmpeg`:

   ```bash
   ffmpeg -i source.mp4 -an -vf "scale=1920:-2" -t 12 \
          -movflags +faststart -pix_fmt yuv420p hero-video.mp4
   ```

2. Use a royalty-free Pexels / Pixabay "ocean waves" / "abstract water"
   clip and rename it to `hero-video.mp4`.
