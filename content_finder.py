#!/usr/bin/env python3
import sys
import os

# Check tkinter compatibility before importing
def check_tkinter():
    """Check if tkinter is available and working"""
    try:
        import tkinter as tk
        # Try to create a test window to ensure it actually works
        test = tk.Tk()
        test.withdraw()
        test.destroy()
        return True
    except Exception as e:
        print("=" * 70)
        print("ERROR: Tkinter is not working properly on your system")
        print("=" * 70)
        print(f"\nError details: {str(e)}\n")
        print("SOLUTION:")
        print("1. Install Homebrew Python (recommended):")
        print("   brew install python-tk")
        print("\n2. Then run the tool with:")
        print("   /opt/homebrew/bin/python3 content_finder.py")
        print("\nOR use the updated launcher which does this automatically.")
        print("=" * 70)
        return False

if not check_tkinter():
    sys.exit(1)

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pysrt
import ffmpeg
from datetime import timedelta
import threading
import subprocess

def format_timestamp(seconds):
    """Convert seconds to HH:MM:SS format"""
    return str(timedelta(seconds=int(seconds)))

def get_audio_tracks(video_file):
    """Get information about audio tracks in the video file"""
    try:
        probe = ffmpeg.probe(video_file)
        audio_streams = []
        audio_index = 0  # Track audio stream number separately
        
        for stream in probe['streams']:
            if stream['codec_type'] == 'audio':
                stream_index = stream['index']  # Overall stream index in file
                # Get language if available
                language = stream.get('tags', {}).get('language', 'unknown')
                # Get title if available
                title = stream.get('tags', {}).get('title', '')
                # Get codec info
                codec = stream.get('codec_name', 'unknown')
                channels = stream.get('channels', '?')
                
                # Build display name
                display = f"Track {stream_index}: {language}"
                if title:
                    display += f" ({title})"
                display += f" - {codec} {channels}ch"
                
                audio_streams.append({
                    'stream_index': stream_index,  # Overall stream index
                    'audio_index': audio_index,     # Audio-specific index (0, 1, 2...)
                    'display': display,
                    'language': language,
                    'title': title,
                    'codec': codec
                })
                audio_index += 1
        
        return audio_streams
    except Exception as e:
        print(f"Warning: Could not probe audio tracks: {e}")
        return []

def find_word_in_subtitles(subtitle_file, word):
    """Find all instances of a word in subtitle file"""
    try:
        subs = pysrt.open(subtitle_file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            subs = pysrt.open(subtitle_file, encoding='latin-1')
        except Exception as e:
            raise Exception(f"Failed to read subtitle file: {str(e)}")
    except Exception as e:
        raise Exception(f"Error opening subtitle file: {str(e)}")
    
    timestamps = []
    for sub in subs:
        if word.lower() in sub.text.lower():
            start_time = sub.start.ordinal / 1000.0
            end_time = sub.end.ordinal / 1000.0
            text = sub.text.replace('\n', ' ')
            timestamps.append((start_time, end_time, text))
    return timestamps

def create_clips(video_file, subtitle_file, word, output_folder, pre_time, post_time, progress_callback=None, merge_clips=False, audio_track=None):
    """Create video clips for each instance of the word"""
    try:
        # Validate inputs
        if not os.path.exists(video_file):
            raise Exception(f"Video file not found: {video_file}")
        if not os.path.exists(subtitle_file):
            raise Exception(f"Subtitle file not found: {subtitle_file}")
        
        # Find all instances
        timestamps = find_word_in_subtitles(subtitle_file, word)
        
        if not timestamps:
            messagebox.showinfo("No Matches", f"No instances of '{word}' found in subtitles.")
            return False

        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Create word-specific subfolder
        safe_word = "".join(c for c in word if c.isalnum() or c in (' ', '-', '_')).strip()
        word_folder = os.path.join(output_folder, f"clips_{safe_word}")
        os.makedirs(word_folder, exist_ok=True)

        clip_files = []
        total_clips = len(timestamps)
        
        # Create individual clips
        for i, (start, end, text) in enumerate(timestamps):
            if progress_callback:
                progress_callback(i, total_clips)
            
            adjusted_start = max(0, start - pre_time)
            adjusted_end = end + post_time
            
            # Create descriptive filename
            timestamp_str = format_timestamp(start).replace(':', '-')
            output_clip = os.path.join(word_folder, f"clip_{i+1:03d}_{timestamp_str}.mp4")
            clip_files.append(output_clip)
            
            try:
                # Build ffmpeg command based on audio track selection
                if audio_track is not None:
                    # Select specific audio track - use direct command for stream mapping
                    cmd = [
                        'ffmpeg',
                        '-ss', str(adjusted_start),
                        '-i', video_file,
                        '-to', str(adjusted_end - adjusted_start),
                        '-map', '0:v:0',
                        '-map', f'0:a:{audio_track}',
                        '-c:v', 'libx264',
                        '-c:a', 'aac',
                        '-y',
                        output_clip
                    ]
                    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if result.returncode != 0:
                        error_msg = result.stderr.decode() if result.stderr else "Unknown error"
                        raise Exception(f"FFmpeg error: {error_msg}")
                else:
                    # Use all audio tracks (default)
                    (
                        ffmpeg
                        .input(video_file, ss=adjusted_start, to=adjusted_end)
                        .output(output_clip, vcodec='libx264', acodec='aac', 
                                loglevel='error', **{'y': None})
                        .run(capture_stdout=True, capture_stderr=True)
                    )
            except (ffmpeg.Error, subprocess.CalledProcessError, Exception) as e:
                if isinstance(e, ffmpeg.Error):
                    error_msg = e.stderr.decode() if e.stderr else str(e)
                else:
                    error_msg = str(e)
                raise Exception(f"FFmpeg error creating clip {i+1}: {error_msg}")

        # Merge clips if requested
        if merge_clips and len(clip_files) > 1:
            if progress_callback:
                progress_callback(total_clips, total_clips, "Merging clips...")
            
            merge_output = os.path.join(word_folder, f"merged_{safe_word}.mp4")
            
            # Create concat file
            concat_file = os.path.join(word_folder, "concat_list.txt")
            with open(concat_file, 'w') as f:
                for clip in clip_files:
                    f.write(f"file '{os.path.basename(clip)}'\n")
            
            try:
                (
                    ffmpeg
                    .input(concat_file, format='concat', safe=0)
                    .output(merge_output, c='copy', loglevel='error', **{'y': None})
                    .run(capture_stdout=True, capture_stderr=True)
                )
                os.remove(concat_file)
            except ffmpeg.Error as e:
                error_msg = e.stderr.decode() if e.stderr else str(e)
                raise Exception(f"FFmpeg error merging clips: {error_msg}")

        if progress_callback:
            progress_callback(total_clips, total_clips, "Complete!")
        
        messagebox.showinfo("Success", 
            f"Created {total_clips} clip(s) in:\n{word_folder}" +
            (f"\n\nMerged video: merged_{safe_word}.mp4" if merge_clips and len(clip_files) > 1 else ""))
        return True
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        return False

def browse_file(entry, callback=None):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)
    if callback and filename:
        callback(filename)

def browse_folder(entry):
    foldername = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, foldername)

def main():
    root = tk.Tk()
    root.title("Subtitle Word Clip Extractor")
    root.resizable(False, False)

    # Store audio track info
    audio_tracks = []
    
    # Audio track combobox
    audio_track_var = tk.StringVar()
    audio_track_combo = ttk.Combobox(root, textvariable=audio_track_var, width=47, state='readonly')
    audio_track_combo['values'] = ["All audio tracks (default)"]
    audio_track_combo.current(0)
    
    def load_audio_tracks(video_file):
        """Load audio tracks from video file"""
        nonlocal audio_tracks
        try:
            audio_tracks = get_audio_tracks(video_file)
            if audio_tracks:
                options = ["All audio tracks (default)"] + [track['display'] for track in audio_tracks]
                audio_track_combo['values'] = options
                audio_track_combo.current(0)
                messagebox.showinfo("Audio Tracks Found", 
                    f"Found {len(audio_tracks)} audio track(s).\n" +
                    "You can select a specific track or use all tracks (default).")
            else:
                audio_track_combo['values'] = ["All audio tracks (default)"]
                audio_track_combo.current(0)
        except Exception as e:
            print(f"Could not load audio tracks: {e}")
            audio_track_combo['values'] = ["All audio tracks (default)"]
            audio_track_combo.current(0)
    
    # Input fields
    tk.Label(root, text="Video File:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    video_entry = tk.Entry(root, width=50)
    video_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_file(video_entry, load_audio_tracks)).grid(row=0, column=2, padx=5, pady=5)
    
    # Audio track selector
    tk.Label(root, text="Audio Track:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    audio_track_combo.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text="Refresh", command=lambda: load_audio_tracks(video_entry.get()) if video_entry.get() else None).grid(row=1, column=2, padx=5, pady=5)

    tk.Label(root, text="Subtitle File:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    subtitle_entry = tk.Entry(root, width=50)
    subtitle_entry.grid(row=2, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_file(subtitle_entry)).grid(row=2, column=2, padx=5, pady=5)

    tk.Label(root, text="Word to Find:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
    word_entry = tk.Entry(root, width=50)
    word_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(root, text="Output Folder:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
    output_folder_entry = tk.Entry(root, width=50)
    output_folder_entry.grid(row=4, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_folder(output_folder_entry)).grid(row=4, column=2, padx=5, pady=5)
    
    # Set default output folder to user's home directory
    default_output = os.path.join(os.path.expanduser("~"), "WordClipperOutput")
    output_folder_entry.insert(0, default_output)

    # Time sliders with default values
    tk.Label(root, text="Seconds Before:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
    pre_time_slider = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL)
    pre_time_slider.set(1)  # Default to 1 second
    pre_time_slider.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

    tk.Label(root, text="Seconds After:").grid(row=6, column=0, padx=5, pady=5, sticky='e')
    post_time_slider = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL)
    post_time_slider.set(1)  # Default to 1 second
    post_time_slider.grid(row=6, column=1, padx=5, pady=5, sticky='ew')

    # Merge clips option
    merge_var = tk.BooleanVar()
    merge_checkbox = tk.Checkbutton(root, text="Merge all clips into one video", variable=merge_var)
    merge_checkbox.grid(row=7, column=1, padx=5, pady=5, sticky='w')

    # Preview button
    def on_preview():
        subtitle_file = subtitle_entry.get()
        word = word_entry.get()
        
        if not subtitle_file or not word:
            messagebox.showwarning("Input Error", "Please provide subtitle file and word.")
            return
        
        if not os.path.exists(subtitle_file):
            messagebox.showerror("Error", "Subtitle file not found.")
            return
        
        try:
            timestamps = find_word_in_subtitles(subtitle_file, word)
            
            if not timestamps:
                messagebox.showinfo("No Matches", f"No instances of '{word}' found in subtitles.")
                return
            
            # Create preview window
            preview_window = tk.Toplevel(root)
            preview_window.title(f"Preview: Found {len(timestamps)} instance(s)")
            preview_window.geometry("600x400")
            
            # Add scrollbar
            frame = tk.Frame(preview_window)
            frame.pack(fill=tk.BOTH, expand=True)
            
            scrollbar = tk.Scrollbar(frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            text_widget = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=text_widget.yview)
            
            # Display results
            text_widget.insert(tk.END, f"Found {len(timestamps)} instance(s) of '{word}':\n\n")
            for i, (start, end, text) in enumerate(timestamps):
                timestamp = format_timestamp(start)
                text_widget.insert(tk.END, f"#{i+1} at {timestamp}\n")
                text_widget.insert(tk.END, f"  {text}\n\n")
            
            text_widget.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

    # Progress bar
    progress_label = tk.Label(root, text="")
    progress_label.grid(row=8, column=0, columnspan=3, pady=5)
    
    progress_bar = ttk.Progressbar(root, length=400, mode='determinate')
    progress_bar.grid(row=9, column=0, columnspan=3, pady=5)

    def update_progress(current, total, status="Processing..."):
        progress = (current / total) * 100 if total > 0 else 0
        progress_bar['value'] = progress
        progress_label.config(text=f"{status} ({current}/{total})")
        root.update_idletasks()

    def on_create():
        video_file = video_entry.get()
        subtitle_file = subtitle_entry.get()
        word = word_entry.get()
        output_folder = output_folder_entry.get()
        pre_time = pre_time_slider.get()
        post_time = post_time_slider.get()
        merge = merge_var.get()
        
        # Determine selected audio track
        selected_audio = None
        selected_index = audio_track_combo.current()
        if selected_index > 0 and audio_tracks:  # 0 is "All audio tracks (default)"
            track_list_index = selected_index - 1  # Adjust for the "All tracks" option
            if track_list_index < len(audio_tracks):
                # Get the audio stream index (0, 1, 2...) for FFmpeg's 0:a:X format
                # This is different from the overall stream index
                selected_audio = audio_tracks[track_list_index]['audio_index']
        
        if not video_file or not subtitle_file or not word or not output_folder:
            messagebox.showwarning("Input Error", "Please provide all inputs.")
            return
        
        # Reset progress
        progress_bar['value'] = 0
        progress_label.config(text="Starting...")
        
        # Run in separate thread to keep UI responsive
        def run_creation():
            success = create_clips(video_file, subtitle_file, word, output_folder, 
                                  pre_time, post_time, update_progress, merge, selected_audio)
            if success:
                progress_bar['value'] = 100
                progress_label.config(text="Complete!")
            else:
                progress_bar['value'] = 0
                progress_label.config(text="")
        
        thread = threading.Thread(target=run_creation, daemon=True)
        thread.start()

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=10, column=0, columnspan=3, pady=10)
    
    tk.Button(button_frame, text="Preview Instances", command=on_preview, width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Create Clips", command=on_create, width=15, bg='#4CAF50', fg='white').pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()