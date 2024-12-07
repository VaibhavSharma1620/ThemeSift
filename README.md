# 🖼️ ThemeSift: Intelligent Image Clustering and Theme Extraction

## 📝 Project Overview

ThemeSift is an advanced image analysis tool that leverages cutting-edge AI technologies to automatically categorize and cluster images based on their visual themes. By combining computer vision and large language models, ThemeSift provides an intelligent solution for organizing and understanding image collections.

## Demo
![Demo video](/DevTry.png)

### 🚀 Key Features

- **Intelligent Caption Generation**: Uses BLIP image captioning model to generate descriptive captions for images
- **Theme-based Clustering**: Employs GPT-4 to analyze image captions and identify thematic similarities
- **Interactive Web Interface**: React-based frontend for seamless image upload and visualization
- **Downloadable Clusters**: Easily export images grouped by their detected themes

## 🤖 Technical Architecture

### Backend (FastAPI)
- **Image Captioning**: Utilizes Salesforce BLIP model for generating image descriptions
- **Theme Analysis**: OpenAI GPT-4 identifies thematic connections between images
- **Processing Endpoints**: 
  - `/process_images/`: Uploads and analyzes images
  - `/download_clusters/`: Exports themed image clusters

### Frontend (React)
- Image upload interface
- Real-time processing and result visualization
- Cluster download functionality

## 💡 Potential Use Cases

1. **Digital Asset Management**
   - Photographers can quickly organize large photo libraries
   - Design agencies can categorize visual reference materials
   - Stock photo websites can improve image tagging

2. **Personal Photo Organization**
   - Automatically sort vacation, family, or event photos
   - Create themed photo albums with minimal manual effort

3. **Content Creation**
   - Social media managers can identify and group content themes
   - Bloggers can quickly find relevant images for articles

4. **Research and Academia**
   - Analyze visual trends in academic or scientific image collections
   - Group research images by subject or characteristics

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup
1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up OpenAI API key in the code

### Frontend Setup
1. Navigate to frontend directory
2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Application
1. Start Backend (FastAPI):
   ```bash
   uvicorn main:app --reload
   ```
2. Start Frontend (React):
   ```bash
   npm start
   ```

## 🔒 Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for GPT-4 theme analysis

## 🌟 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
Distributed under the MIT License. See LICENSE for more information.

## 🙏 Acknowledgements
- Salesforce BLIP Model
- OpenAI GPT-4
- FastAPI
- React
