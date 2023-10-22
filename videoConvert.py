import subprocess
import sys
import json

def extract_video_info(filename):
    # Use FFmpeg to extract video stream details in JSON format
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        filename
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return json.loads(result.stdout)

def chroma_subsampling_to_codec(pix_fmt):
    mapping = {
        'yuv420p': '08',
        'yuv422p': '09',
        'yuv444p': '10',
    }

def generate_av1_codec_string(video_info):
    # Extract and process details from video_info to generate codec string

    profile = video_info['profile']
    level = video_info['level']
    chroma_subsampling = chroma_subsampling_to_codec(video_info['pix_fmt'])
    bit_depth = video_info['bits_per_sample']
    color_space = video_info['color_space']
    color_transfer = video_info['color_transfer']
    color_primaries = video_info['color_primaries']

    # Example:
    # "av01.0.08M.08.0.110.01.01.01.1"
    codec_string = f"av01.{profile}.{level}.{chroma_subsampling}.{bit_depth}.{color_space}.{color_transfer}.{color_primaries}.01.1"

    return codec_string

def main():
    if len(sys.argv) < 2:
        print("Usage: python program_name.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    video_info = extract_video_info(filename)
    
    for stream in video_info['streams']:
        if stream['codec_name'] == 'av1' and stream['codec_type'] == 'video':
            print(generate_av1_codec_string(stream))
            return

    print("AV1 video stream not found in the provided file.")

if __name__ == "__main__":
    main()
