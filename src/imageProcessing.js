import axios from 'axios';

export const batchProcessImages = async (imageUris, setFacesDetected) => {
    const batchSize = 10; // Process 10 Images at a Time
    for (let i = 0; i < imageUris.length; i += batchSize) {
        const batch = imageUris.slice(i, i + batchSize > imageUris.length ? imageUris.length : i + batchSize);

        for (const uri of batch) {
            await uploadImage(uri, setFacesDetected)
        }
    }
};

const uploadImage = async (uri, setFacesDetected) => {
    const formData = new FormData();

    formData.append('image', {
        uri,
        type: 'image/jpeg', // Adjust Based on File Type
        name: 'photo.jpg',

    });

    try {
        const response = await axios.post('http://your-backend-url/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data'},
        });
        setFacesDetected(prevState => ({
            ...prevState,
            [uri]: response.data.faces_detected,
        }));
    } catch (error) {
        console.log('Error Uploading Image: ', error);
    }
};