import base64
import os.path

from openai import OpenAI

from prompt_to_storyboard.agents.storyboard_prompts_agent import StoryboardPrompt

STORYBOARD_IMAGES_FOLDER = "./prompt_to_storyboard/assets/storyboards"
CORE_STORYBOARD_IMAGE_PROMPT = """
You are a professional storyboard artist, who is an expert at taking prompts and script snippets, and creating storyboard images based on them.

The image must be in the style of a storyboard, with a focus on action and composition.
The image should have vivid colors and a clear, clean, cell-shaded style.
Characters should be depicted as simply as possible.
Movement and action should be indicated with arrows and lines.
Dialogue should NEVER be included in the image. Any dialogue MUST be indicated using ONLY the character's actions and expressions, if applicable.
ONLY create a single panel for the storyboard image.

The image MUST NOT contain any AI generation artifacts, and MUST be a clean, clear image that can be used as a reference for a storyboard.
"""

def generate_base_prompt(prompt: str, script: str, story_bible: str):
    """
        Generate the beginning of the prompt for storyboard image generation
    """
    return f"""
    {CORE_STORYBOARD_IMAGE_PROMPT}

    Create a storyboard image based on the following prompt:
    ```
    {prompt}
    ```
    as well as the following script snippet:
    ```
    {script}
    ```
    The following story bible is associated with the user's prompt. Ensure the generated storyboard image is consistent with this content:
    ```
    {story_bible}
    ```"""

class StoryboardImagesAgent:
    client: OpenAI

    def generate_storyboard_images(self, storyboard_prompts: list[StoryboardPrompt], story_bible: str):
        # Only generate the storyboard images if they don't already exist
        if (not os.path.exists(f"{STORYBOARD_IMAGES_FOLDER}/storyboard_{0}.png")):
            first_prompt = generate_base_prompt(storyboard_prompts[0]['prompt'], storyboard_prompts[0]['script'], story_bible)

            result = self.client.images.generate(
                model="gpt-image-1",
                prompt=first_prompt,
                size="1536x1024",

                # Go extra hard on the first image, since it will be used as a reference for the rest
                quality="high",
            )

            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

            # The first image is complete
            with open(f"{STORYBOARD_IMAGES_FOLDER}/storyboard_{0}.png", "wb") as f:
                f.write(image_bytes)
                print(f"Image {0} saved.")
        else:
            print(f"Image {0} already exists. Skipping generation.")

        # Generate the rest of the storyboard images
        for i in range(1, len(storyboard_prompts)):
            if (not os.path.exists(f"{STORYBOARD_IMAGES_FOLDER}/storyboard_{i}.png")):
                prompt = f"""
                {generate_base_prompt(storyboard_prompts[i]['prompt'], storyboard_prompts[i]['script'], story_bible)}

                The reference image is the first image in the storyboard. The generated image should have the same style as this image, but with the new prompt. ONLY use this reference image to inform the style of the new image."""

                print(f"Generating image {i}...")
                result = self.client.images.edit(
                    model="gpt-image-1",
                    prompt=prompt,
                    size="1536x1024",
                    quality="medium",
                    image=[
                        open(f"{STORYBOARD_IMAGES_FOLDER}/storyboard_{0}.png", "rb")
                    ]
                )

                image_base64 = result.data[0].b64_json
                image_bytes = base64.b64decode(image_base64)

                # The first image is complete
                with open(f"{STORYBOARD_IMAGES_FOLDER}/storyboard_{i}.png", "wb") as f:
                    f.write(image_bytes)
                    print(f"Image {i} saved.")
            else:
                print(f"Image {i} already exists. Skipping generation.")

    # ========= BUILT INS ==========
    def __init__(self):
        self.client = OpenAI()
