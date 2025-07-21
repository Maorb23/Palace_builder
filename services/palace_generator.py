import threading
from django.core.files.base import ContentFile
from services.openai_service import client
import base64
import uuid
from PIL import Image, ImageDraw
import io
import numpy as np
from PIL import ImageFilter 
from django.db import models

def call_nebius_api(prompt, size="512x512"):
    print(f"Making API call with prompt: {prompt[:100]}...")
    try:
        response = client.images.generate(
            model="black-forest-labs/flux-dev",
            prompt=prompt,
            response_format="b64_json",
            extra_body={
                "response_extension": "png",
                "width": int(size.split("x")[0]),
                "height": int(size.split("x")[1]),
                "num_inference_steps": 28,
                "negative_prompt": "fantasy, magical, unrealistic, cartoon, anime, abstract, surreal",
                "seed": -1
            }
        )
        print(f"API response received: {response}")
        b64_image = response.data[0].b64_json
        decoded_image = base64.b64decode(b64_image)
        print(f"Image decoded: {len(decoded_image)} bytes")
        return decoded_image
    except Exception as e:
        print(f"Error in API call: {e}")
        import traceback
        traceback.print_exc()
        return None

def build_complete_palace_prompt(main_task):
    """Build prompt for the complete palace with all layers"""
    all_layers = main_task.sub_tasks.all().order_by('order')
    layers_desc = ', '.join([
        f"step {sub.order}: {sub.title} ({sub.time_estimate} min)" if sub.time_estimate else f"step {sub.order}: {sub.title}"
        for sub in all_layers
    ])
    
    # Create a mission-focused palace prompt
    detailed_prompt = f"""
Create a one-of-a-kind full palace that artistically represents the successful completion of this mission: \"{main_task.title}\". The image MUST show a complete unobstructed palace with all major architectural components visible. 

Mission Details:
- Main Objective: {main_task.title}
- Completion Steps: {layers_desc}
- Category: {main_task.category}
- Complexity Level: {main_task.complexity}/5

Palace Design Guidelines:
- The palace should be a unique and imaginative interpretation of the mission's completion.
- Feel free to experiment with unexpected forms, styles, and materials, but make sure to include major architectural components.
- Let the architecture, colors, and atmosphere reflect the spirit and journey of the mission in a creative way.
- Each palace should look distinctly different from others, surprising and delighting the viewer.
- Avoid repeating standard palace features unless they fit your unique vision for this mission. 
- Include spires and towers.
- You hate circles, so avoid them.

Style: Inventive, original, and visually striking. The palace should evoke a sense of accomplishment and pride, but its design is open to your creative interpretation.

Lighting, materials, and atmosphere: Use whatever best expresses the uniqueness and success of \"{main_task.title}\".

Make the viewer feel the satisfaction and pride of having completed: \"{main_task.title}\"—in a satisfying way.
"""
    
    return detailed_prompt.strip()

def generate_complete_palace_once(main_task):
    """Generate the complete palace image ONLY ONCE and save it"""
    print(f"Generating complete palace for task: {main_task.title}")
    
    # Check if we already have a complete palace image
    if hasattr(main_task, 'complete_palace_image') and main_task.complete_palace_image:
        print("Complete palace already exists, skipping generation")
        return main_task.complete_palace_image
    
    complete_prompt = build_complete_palace_prompt(main_task)
    print(f"Complete palace prompt: {complete_prompt}")
    
    complete_image_bytes = call_nebius_api(complete_prompt)
    if complete_image_bytes:
        # Save complete palace to a separate field
        filename = f'complete_palace_{uuid.uuid4().hex[:8]}.png'
        main_task.complete_palace_image.save(filename, ContentFile(complete_image_bytes))
        main_task.save()
        print(f"Complete palace saved to: {main_task.complete_palace_image.url}")
        return main_task.complete_palace_image
    return None

def create_layer_specific_mask(completed_subtasks, total_count, size=(512, 512)):
    """
    Create a mask that reveals only the specific layers for completed sub-tasks
    - Each completed task reveals only its own layer, not previous ones
    - completed_subtasks: queryset of completed sub-tasks
    - total_count: total number of sub-tasks
    """
    w, h = size
    mask_arr = np.zeros((h, w), dtype=np.uint8)
    
    if not completed_subtasks.exists():
        return Image.fromarray(mask_arr, mode="L")
    
    # Calculate layer height for each sub-task
    layer_height = h // total_count
    
    # For each completed sub-task, reveal only its specific layer
    for subtask in completed_subtasks:
        order = subtask.order
        if order > 0 and order <= total_count:
            # Calculate the layer boundaries for this specific order
            layer_start = h - (order * layer_height)
            layer_end = h - ((order - 1) * layer_height)
            
            # Ensure we don't go out of bounds
            layer_start = max(0, layer_start)
            layer_end = min(h, layer_end)
            
            # Reveal only this specific layer
            mask_arr[layer_start:layer_end, :] = 255
            print(f"Revealing layer {order}: rows {layer_start}-{layer_end}")
    
    # Convert to PIL and add slight blur for smooth edges
    mask_img = Image.fromarray(mask_arr, mode="L")
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(2))
    
    return mask_img

def apply_mask_to_image(complete_bytes, mask_img, grey_color=(128, 128, 128)):
    """Apply mask to reveal palace parts over grey background"""
    try:
        complete = Image.open(io.BytesIO(complete_bytes)).convert("RGB")
        grey_bg = Image.new("RGB", complete.size, grey_color)
        
        # Resize mask to match image size
        mask_img = mask_img.resize(complete.size)
        
        # Composite: white in mask = palace, black = grey background
        final = Image.composite(complete, grey_bg, mask_img)
        
        # Save to bytes
        buf = io.BytesIO()
        final.save(buf, format="PNG")
        return buf.getvalue()
        
    except Exception as e:
        print(f"Error applying mask: {e}")
        return None

def generate_palace_image(main_task):
    print(f"Generating palace image for task: {main_task.title}")
    
    # 1. Generate complete palace ONLY ONCE
    complete_palace_image = generate_complete_palace_once(main_task)
    if not complete_palace_image:
        print("Failed to generate complete palace")
        return
    
    # 2. Calculate completion progress based on order
    completed_subtasks = main_task.sub_tasks.filter(is_completed=True)
    total_count = main_task.sub_tasks.count()
    
    print(f"Completed sub-tasks: {completed_subtasks.count()}/{total_count}")
    
    # 3. Create layer-specific mask (each completed task reveals only its layer)
    mask_image = create_layer_specific_mask(completed_subtasks, total_count)
    
    # 4. Apply mask to reveal specific layers
    with open(complete_palace_image.path, 'rb') as f:
        complete_palace_bytes = f.read()
    
    final_image_bytes = apply_mask_to_image(complete_palace_bytes, mask_image)
    
    if final_image_bytes:
        filename = f'palace_{uuid.uuid4().hex[:8]}.png'
        main_task.palace_image.save(filename, ContentFile(final_image_bytes))
        main_task.save()
        print(f"Layer-specific palace saved to: {main_task.palace_image.url}")
    else:
        print("Failed to create layer-specific palace image")

def trigger_palace_generation_async(main_task):
    threading.Thread(target=generate_palace_image, args=(main_task,)).start()

def test_image_generation():
    """Test function to verify image generation is working"""
    print("Testing image generation...")
    try:
        test_prompt = "A simple test image of a building foundation."
        image_bytes = call_nebius_api(test_prompt)
        if image_bytes:
            print(f"Test successful! Generated {len(image_bytes)} bytes")
            return True
        else:
            print("Test failed: No image bytes returned")
            return False
    except Exception as e:
        print(f"Test failed with error: {e}")
        return False 