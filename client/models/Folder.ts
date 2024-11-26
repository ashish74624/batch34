import mongoose from "mongoose";

const FolderSchema = new mongoose.Schema({
    email: { type: String, required: true },
    folderName: { type: String, required: true },
    imageName: { type: String, required: true },
    imageCloud: {
        versionName: { type: String },
        generatedName: { type: String }
    }
}, {
    collection: 'Folder'
});

// Check if the model already exists before defining it
const Folder = mongoose.models.Folder || mongoose.model('Folder', FolderSchema);

export default Folder;
