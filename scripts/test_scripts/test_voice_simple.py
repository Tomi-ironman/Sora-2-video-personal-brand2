#!/usr/bin/env python3
"""Simple test of voice cloning API"""

from voice_cloning_api import clone_voice

# Test with a simple, short sentence
simple_text = "Hello, this is a test of the voice cloning system."

print("Testing with simple text...")
result = clone_voice(simple_text, "narrations/test_simple.wav", timeout=300)

if result:
    print(f"\n✅ SUCCESS! Audio saved to: {result}")
    
    # Open it
    import subprocess
    subprocess.run(['open', result])
else:
    print("\n❌ FAILED")
    print("\nLet's try debugging the API endpoint...")
    
    # Try a raw curl request
    import subprocess
    print("\nTrying with curl...")
    subprocess.run([
        'curl', '-X', 'POST',
        'https://zenyai-voice-cloning-d73w32b5wq-uc.a.run.app/clone-voice',
        '-H', 'Content-Type: application/json',
        '-d', '{"reference_audio_url": "https://storage.googleapis.com/chatterbox-ai-models/voices/tomi_reference.wav", "text": "Hello world"}'
    ])
