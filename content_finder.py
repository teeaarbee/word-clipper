import tkinter as tk
from tkinter import filedialog, messagebox
import pysrt
import ffmpeg
import os

def find_word_in_subtitles(subtitle_file, word):
    subs = pysrt.open(subtitle_file)
    timestamps = []
    for sub in subs:
        if word.lower() in sub.text.lower():
            start_time = sub.start.ordinal / 1000.0
            end_time = sub.end.ordinal / 1000.0
            timestamps.append((start_time, end_time))
    return timestamps

def create_clips(video_file, subtitle_file, word, output_folder, pre_time, post_time):
    timestamps = find_word_in_subtitles(subtitle_file, word)
    
    if not timestamps:
        messagebox.showinfo("No Matches", f"No instances of '{word}' found in subtitles.")
        return

    # Create individual clips
    for i, (start, end) in enumerate(timestamps):
        adjusted_start = max(0, start - pre_time)  # Ensure start is not negative
        adjusted_end = end + post_time
        output_clip = os.path.join(output_folder, f"clip_{i}.mp4")
        ffmpeg.input(video_file, ss=adjusted_start, to=adjusted_end).output(output_clip, vcodec='libx264', acodec='aac').run(overwrite_output=True)

    messagebox.showinfo("Success", f"Clips saved in {output_folder}")

def browse_file(entry):
    filename = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, filename)

def browse_folder(entry):
    foldername = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, foldername)

def main():
    root = tk.Tk()
    root.title("Subtitle Word Clip Extractor")

    tk.Label(root, text="Video File:").grid(row=0, column=0, padx=5, pady=5)
    video_entry = tk.Entry(root, width=50)
    video_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_file(video_entry)).grid(row=0, column=2, padx=5, pady=5)

    tk.Label(root, text="Subtitle File:").grid(row=1, column=0, padx=5, pady=5)
    subtitle_entry = tk.Entry(root, width=50)
    subtitle_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_file(subtitle_entry)).grid(row=1, column=2, padx=5, pady=5)

    tk.Label(root, text="Word to Find:").grid(row=2, column=0, padx=5, pady=5)
    word_entry = tk.Entry(root, width=50)
    word_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(root, text="Output Folder:").grid(row=3, column=0, padx=5, pady=5)
    output_folder_entry = tk.Entry(root, width=50)
    output_folder_entry.grid(row=3, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=lambda: browse_folder(output_folder_entry)).grid(row=3, column=2, padx=5, pady=5)

    tk.Label(root, text="Seconds Before:").grid(row=4, column=0, padx=5, pady=5)
    pre_time_slider = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL)
    pre_time_slider.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(root, text="Seconds After:").grid(row=5, column=0, padx=5, pady=5)
    post_time_slider = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL)
    post_time_slider.grid(row=5, column=1, padx=5, pady=5)

    def on_create():
        video_file = video_entry.get()
        subtitle_file = subtitle_entry.get()
        word = word_entry.get()
        output_folder = output_folder_entry.get()
        pre_time = pre_time_slider.get()
        post_time = post_time_slider.get()
        
        if not video_file or not subtitle_file or not word or not output_folder:
            messagebox.showwarning("Input Error", "Please provide all inputs.")
            return
        
        create_clips(video_file, subtitle_file, word, output_folder, pre_time, post_time)

    tk.Button(root, text="Create Clips", command=on_create).grid(row=6, column=0, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()