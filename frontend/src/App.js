import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [mainImage, setMainImage] = useState(null);
  const [groupImages, setGroupImages] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleMainImageChange = (e) => {
    setMainImage(e.target.files[0]);
  };

  const handleGroupImagesChange = (e) => {
    setGroupImages(Array.from(e.target.files));
  };

  const handleSubmit = async () => {
    if (!mainImage || groupImages.length === 0) {
      alert('Please select a main image and at least one group image.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('main_image', mainImage);
    groupImages.forEach((img) => {
      formData.append('group_images', img);
    });

    try {
      const response = await axios.post('http://localhost:8000/process_images/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Backend response:', response.data);
      setResult(response.data);
    } catch (err) {
      console.error('Error processing images:', err);
      setError('An error occurred while processing the images. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    try {
      const response = await axios.get('http://localhost:8000/download_clusters/', {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'clusters.zip');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (err) {
      console.error('Error downloading clusters:', err);
      setError('An error occurred while downloading the clusters. Please try again.');
    }
  };

  const renderImage = (imageData, alt, maxWidth) => {
    if (!imageData) {
      console.warn(`Image data missing for ${alt}`);
      return <p>Image not available</p>;
    }
    return (
      <img
        src={`data:image/jpeg;base64,${imageData}`}
        alt={alt}
        style={{ maxWidth: maxWidth }}
      />
    );
  };

  return (
    <div className="App">
      <h1>Image Caption Clustering</h1>
      <div>
        <label>Main Image: </label>
        <input type="file" accept="image/*" onChange={handleMainImageChange} />
      </div>
      <div>
        <label>Group Images: </label>
        <input type="file" accept="image/*" multiple onChange={handleGroupImagesChange} />
      </div>
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Processing...' : 'Process Images'}
      </button>
      <button onClick={handleDownload} disabled={!result || loading}>
        Download Clusters
      </button>

      {loading && (
        <div className="loader-container">
          <div className="loader"></div>
          <p>Processing images, please wait...</p>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}

      {result && (
        <div className="result">
          <h2>Main Image Caption</h2>
          {renderImage(result.main_image.data, "Main", '300px')}
          <p>{result.main_image.caption || 'No caption available'}</p>

          <h2>Similar Images</h2>
          <div className="image-grid">
            {Object.entries(result.similar_images).length > 0 ? (
              Object.entries(result.similar_images).map(([filename, info]) => (
                <div key={filename} className="image-card">
                  {renderImage(result.images[filename], filename, '200px')}
                  <p><strong>Caption:</strong> {info.caption || 'No caption available'}</p>
                </div>
              ))
            ) : (
              <p>No similar images found</p>
            )}
          </div>

          <h2>Clustered Images</h2>
          {Object.entries(result.clustered_images).length > 0 ? (
            Object.entries(result.clustered_images).map(([theme, images]) => (
              <div key={theme}>
                <h3>Theme: {theme}</h3>
                <div className="image-grid">
                  {images.map((imageInfo, index) => (
                    <div key={`${theme}-${index}`} className="image-card">
                      {renderImage(result.images[imageInfo.filename], imageInfo.filename, '200px')}
                      <p><strong>Caption:</strong> {imageInfo.caption || 'No caption available'}</p>
                    </div>
                  ))}
                </div>
              </div>
            ))
          ) : (
            <p>No clustered images found</p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
