import  { PermissionsAndroid, Platform } from 'react-native';

export const requestPhotoPermissions = async () => {
    if (Platform.OS === 'android') {
        try {
            const granted = await PermissionsAndroid.request(
                PermissionsAndroid.PERMISSIONS.READ_EXTERNAL_STORAGE,
                {
                    title: 'Photo Library Access Permission',
                    message: 'We Need Access to your Photo Library to Analyze and Clean.',
                    buttonNeutral: 'Ask Later',
                    buttonNegative: 'Cancel',
                    buttonPositive: 'OKAY!'
                }
            );
            return granted === PermissionsAndroid.RESULTS.GRANTED;
        } catch (err) {
            console.warn(err);
            return false;
        }
    } else {
        return true; //iOS Automatically Handles Permission Requests via plist
    }
};