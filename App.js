import React, { useEffect, useState } from 'react';
import { Button, Text, View, PermissionsAndroid, Platform } from 'react-native';
import CameraRoll from '@react-native-community/cameraroll';
import { batchProcessImages } from './src/imageProcessing';
import { requestPhotoPermissions } from './src/permissions';

const App = () => {
    const [images, setImages] = useState([]);
    const [facesDetected, setFacesDetected] = useState({});

    useEffect(() => {
        const fetchImages = async () => {
            // Request Permission to Access Gallery
            const hasPermission = await requestPhotoPermissions();

            if (hasPermission) {
                const photos = await CameraRoll.getPhotos({
                    first: 1000,
                    assetType: 'Photos',
                });
                const imageUris = photos.edges.map(edge => edge.node.image.uri);
                setImages(imageUris);
            }
        };

        fetchImages();
    }, []);

    return (
        <View style = {{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
            <Button title="Start Analysis" onPress={handleBatchProcess} />
            <Text>Processed {Object.keys(facesDetected).length} of {images.length} images</Text>
        </View>
    );
};

export default App;