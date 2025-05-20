import base64
import os.path

from openai import OpenAI

STORYBOARD_IMAGES_FOLDER = "./prompt_to_storyboard/assets/storyboards"
CORE_STORYBOARD_IMAGE_PROMPT_HEADER = """
You are a professional storyboard artist, who is an expert at taking prompts and creating storyboard images based on them.
Create a storyboard image based on the following prompt:
"""
CORE_STORYBOARD_IMAGE_PROMPT_FOOTER = f"""
The image must be in the style of a storyboard, with a focus on action and composition.
Characters should be depicted as simply as possible, and arrows and other aspects should be added to indicate movement and action.
ONLY create a single panel for the storyboard image
"""

class StoryboardImagesAgent:
    client: OpenAI

    def generate_storyboard_images(self, storyboard_prompts: list[str], story_bible: str):
        # Only generate the storyboard images if they don't already exist
        if (not os.path.exists(f"{STORYBOARD_IMAGES_FOLDER}/storyboard_{0}.png")):
            first_prompt = f"""
            {CORE_STORYBOARD_IMAGE_PROMPT_HEADER}
            ```
            {storyboard_prompts[0]}
            ```

            {CORE_STORYBOARD_IMAGE_PROMPT_FOOTER}"""
            print(first_prompt)
            result = self.client.images.generate(
                model="gpt-image-1",
                prompt=first_prompt,
                size="1536x1024",
                quality="medium",
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
                {CORE_STORYBOARD_IMAGE_PROMPT_HEADER}
                ```
                {storyboard_prompts[i]}
                ```

                {CORE_STORYBOARD_IMAGE_PROMPT_FOOTER}
                The reference image is the first image in the storyboard. The generated image should have the same style as this image, but with the new prompt."""

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
