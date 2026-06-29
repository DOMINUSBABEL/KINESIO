import os
import subprocess

CWD = r"C:\Users\jegom\shorts_project"

COMMITS = [
    {
        "msg": "feat: add downloader utility for royalty-free music catalog",
        "files": ["download_royalty_free_music.py"]
    },
    {
        "msg": "feat: download and integrate royalty-free music assets library",
        "files": ["music/"]
    },
    {
        "msg": "feat: add Mount & Blade Warband horizontal and short scripts",
        "files": ["script_warband_long.md", "scripts_shorts_warband_curiosities.md"]
    },
    {
        "msg": "feat: implement neural TTS audio generator for Mount & Blade",
        "files": ["generate_audio_warband.py"]
    },
    {
        "msg": "feat: add Mount & Blade video compilation pipeline and manifest updater",
        "files": ["compile_warband_videos.py", "update_manifest_warband.py"]
    },
    {
        "msg": "feat: add GTA VI vertical short scripts and asset downloader",
        "files": ["scripts_shorts_gta6.md", "download_gta6_assets.py"]
    },
    {
        "msg": "feat: implement neural TTS audio generator for GTA VI campaign",
        "files": ["generate_audio_gta6.py"]
    },
    {
        "msg": "feat: implement KINESIO v5 dynamic video compiler with animated subtitles",
        "files": ["compile_gta6_videos.py", "update_manifest_gta6.py"]
    },
    {
        "msg": "feat: consolidate campaign SEO plans and update video manifest",
        "files": ["warband_campaign_seo.md", "gta6_campaign_seo.md", "video_manifest.md"]
    },
    {
        "msg": "refactor: commit remaining workspace scripts and metadata",
        "files": ["."]
    }
]

def run_git(args):
    res = subprocess.run(["git"] + args, cwd=CWD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res

def main():
    print("Starting progressive 10-commit sequence...")
    
    # 1. Set user identity just in case it is missing in the local git environment
    run_git(["config", "user.name", "DOMINUSBABEL"])
    run_git(["config", "user.email", "dominus@example.com"])
    
    for idx, commit in enumerate(COMMITS):
        commit_num = idx + 1
        print(f"\n--- Commit {commit_num}/10 ---")
        
        # Add files
        for f in commit["files"]:
            print(f"Adding: {f}")
            run_git(["add", f])
            
        # Commit
        msg = commit["msg"]
        print(f"Committing: {msg}")
        res = run_git(["commit", "-m", msg])
        
        if res.returncode == 0:
            print(f"[SUCCESS] Commit {commit_num} created.")
            # Print short hash
            hash_res = run_git(["log", "-1", "--pretty=format:%h - %s"])
            print(f"  {hash_res.stdout}")
        else:
            # Check if there is nothing to commit
            if "nothing to commit" in res.stdout or "nothing to commit" in res.stderr:
                print(f"[SKIPPED] Nothing to commit for step {commit_num} (files may be already committed or empty).")
            else:
                print(f"[FAILED] Commit {commit_num} failed: {res.stderr.strip()}")
                
    print("\nAll commits completed. Pushing to origin/main...")
    push_res = run_git(["push", "origin", "main"])
    if push_res.returncode == 0:
        print("[SUCCESS] Pushed all commits to GitHub.")
    else:
        print(f"[WARNING] Push failed: {push_res.stderr.strip()}")

if __name__ == "__main__":
    main()
