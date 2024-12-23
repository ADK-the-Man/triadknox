import bpy
import sys
import os

# Get the command line arguments after '--'
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # Get all arguments after '--'

new_text = argv[0] if argv else "Default Text"

# Load the existing .blend file
blend_file_path = r"C:\Users\dhara\OneDrive\Documents\Blenkins\flender-app\blenkins.blend"  # Update to your .blend file path
bpy.ops.wm.open_mainfile(filepath=blend_file_path)

# Check existing text objects
print("Existing objects in the scene:")
for obj in bpy.data.objects:
    print(f"Object Name: {obj.name}, Type: {obj.type}")

# Find the text object named 'Text'
text_obj = bpy.data.objects.get("Text")  # Directly look for the object named "Text"

if text_obj and text_obj.type == 'FONT':
    # Update the text content
    text_obj.data.body = new_text
    print(f"Updated text to: {new_text}")  # Log the new text for debugging
    
    # Calculate the width of the text after updating the body
    text_width = text_obj.dimensions.x  # Get the width of the text
    
    # Define the camera's properties
    camera = bpy.data.objects.get("Camera")  # Ensure this is the name of your camera
    if camera:
        # Get the camera's view dimensions (you may want to adjust these values)
        cam = camera.data
        aspect_ratio = cam.aspect_x / cam.aspect_y
        
        # Set a maximum width for the camera view
        max_camera_width = 6.0  # Adjust this value according to your scene
        scale_factor = max_camera_width / text_width if text_width > 0 else 1  # Avoid division by zero
        
        # Scale the text object
        text_obj.scale *= scale_factor
        print(f"Scaled text by factor: {scale_factor}")
    else:
        print("Camera not found in the scene.")

else:
    print("Text object 'Text' not found or is not of type FONT.")

# Set up rendering settings
output_path = r"C:\Users\dhara\OneDrive\Documents\Blenkins\flender-app\{}.mp4".format(new_text)  # Use absolute path
bpy.context.scene.render.filepath = output_path

# Set the format to FFmpeg and ensure audio settings are correct
bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
bpy.context.scene.render.ffmpeg.format = 'MPEG4'  # Set to MP4 format
bpy.context.scene.render.ffmpeg.audio_codec = 'AAC'  # Use AAC audio codec for compatibility
bpy.context.scene.render.ffmpeg.audio_bitrate = 192  # Set audio bitrate for good quality
bpy.context.scene.render.ffmpeg.audio_channels = 'STEREO'  # Set audio to stereo

# Optional: Add a background sound/music
soundstrip = None
if bpy.context.scene.sequence_editor is None:
    bpy.context.scene.sequence_editor_create()

seq = bpy.context.scene.sequence_editor
sound_path = r"C:\Users\dhara\OneDrive\Documents\Blenkins\flender-app\devara.mp3"  # Use absolute path

if os.path.exists(sound_path):
    soundstrip = seq.sequences.new_sound(name="BackgroundMusic", filepath=sound_path, channel=1, frame_start=0)
    
    # Trim the audio to match video length
    soundstrip.frame_final_end = bpy.context.scene.frame_end  # Adjust sound length to match video length
    print("Background music added and trimmed to match the video duration.")
else:
    print(f"Sound file not found at: {sound_path}")

# Render the animation with audio enabled
print("Rendering started...")
bpy.ops.render.render(animation=True)
print("Rendering complete. Video saved to: " + output_path)
