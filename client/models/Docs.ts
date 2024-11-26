import mongoose from "mongoose";

const DocSchema = new mongoose.Schema({
    email:{type:String},
    folders :{ type: [{folderName :{type:String}}] , default:[] }
},
{collection:'Doc'}
);

const Doc = mongoose.models.DocSchema || mongoose.model('Doc',DocSchema);

export default Doc;