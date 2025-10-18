
import sys
sys.path.insert(0, ".")

from voice_providers.chatterbox_provider import ChatterboxProvider

provider = ChatterboxProvider()
provider.generate_with_voice(
    text="""There's a revolution happening in Building a Personal Brand, and most people don't even know it yet. What started as a small innovation has grown into something extraordinary. The pioneers who saw this coming early are already reaping the benefits. This is your moment to be part of something bigger. To transform how you work, create, and succeed. The story of Building a Personal Brand is just beginning.""",
    voice_name="Tomi_Zenyai",
    exaggeration=0.5,
    output_path="temp_complete/voiceover.wav"
)
print("SUCCESS")
