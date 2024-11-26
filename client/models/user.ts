import mongoose from "mongoose";

const UserSchema = new mongoose.Schema ({
    firstName:{ type:String, required:true },
    lastName:{ type:String },
    email:{ type:String, required : true },
    password: { type:String , required : true }
},
{collection:'Users'});

const User = mongoose.models.UserSchema || mongoose.model('User',UserSchema);

export default User;