import io
import zipfile
import os
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import base64
from typing import List, Dict
import json
from openai import OpenAI
# Add this import at the top of the file
import shutil
import io
import zipfile
from fastapi.responses import StreamingResponse
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
device = "cuda" if torch.cuda.is_available() else "cpu"
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(device)
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")

# OpenAI client
client = OpenAI(api_key="API KEy")

def generate_caption(image):
    inputs = blip_processor(image, return_tensors="pt").to(device)
    with torch.no_grad():
        generated_ids = blip_model.generate(**inputs)
    caption = blip_processor.decode(generated_ids[0], skip_special_tokens=True)
    return caption

def open_ai_answers_gpt4(prompt, temp=0.3, n=2):
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are a highly skilled data analyst with expertise in understanding theme of text data and extracting similar theme text from it in a JSON. If you don't find any given text similar give empty Json as output"},
            {"role": "user", "content": prompt},
        ],
        response_format={ "type": "json_object" },
        temperature=temp,
        n=n,
    )
    return response.choices[0].message.content

@app.post("/process_images/")
async def process_images(main_image: UploadFile = File(...), group_images: List[UploadFile] = File(...)):
    # Process main image
    main_image_content = await main_image.read()
    main_image_pil = Image.open(io.BytesIO(main_image_content)).convert("RGB")
    main_caption = generate_caption(main_image_pil)

    # Process group images and generate captions
    group_image_data = {}
    for img in group_images:
        img_content = await img.read()
        img_pil = Image.open(io.BytesIO(img_content)).convert("RGB")
        caption = generate_caption(img_pil)
        group_image_data[img.filename] = {
            "caption": caption,
            "data": base64.b64encode(img_content).decode()
        }

    # Generate prompt for OpenAI
    prompt = f"""
    Provide a JSON output containing two dictionaries. 
    The first dictionary, 'similar', should include keys corresponding to the input image filenames and values that are dictionaries containing the 'caption' key.
    The second dictionary, 'clusters', should include keys as themes and values as a list of dictionaries where each dictionary contains 'filename' and 'caption' keys.
    Main image caption: "{main_caption}"
    Group image captions:
    {json.dumps({k: v['caption'] for k, v in group_image_data.items()})}
    """

    # Get OpenAI response
    openai_response = open_ai_answers_gpt4(prompt)
    print("OpenAI response:", openai_response)  # Log the OpenAI response

    # Parse OpenAI response
    response_data = json.loads(openai_response)

    # Prepare response
    result = {
        "main_image": {
            "caption": main_caption,
            "data": base64.b64encode(main_image_content).decode()
        },
        "similar_images": response_data.get("similar", {}),
        "clustered_images": response_data.get("clusters", {}),
        "images": {k: v['data'] for k, v in group_image_data.items()}
    }

    print("Final result:", json.dumps(result, indent=2))  # Log the final result
    app.state.last_result = result
    return result


@app.get("/download_clusters/")
async def download_clusters():
    if not hasattr(app.state, 'last_result'):
        return {"error": "No processed images available"}

    result = app.state.last_result

    # Create a BytesIO object to store the zip file
    zip_buffer = io.BytesIO()

    # Create a ZipFile object
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for theme, images in result["clustered_images"].items():
            for img_info in images:
                filename = img_info["filename"]
                caption = img_info["caption"]
                
                # Add image to zip
                img_data = base64.b64decode(result["images"][filename])
                zip_file.writestr(f"{theme}/{filename}", img_data)
                
                # Add caption to zip
                caption_filename = f"{theme}/{os.path.splitext(filename)[0]}.txt"
                zip_file.writestr(caption_filename, caption)

    # Seek to the beginning of the BytesIO object
    zip_buffer.seek(0)

    # Create a StreamingResponse
    return StreamingResponse(
        iter([zip_buffer.getvalue()]),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=clusters.zip"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
