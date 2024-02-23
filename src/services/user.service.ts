import bcrypt from "bcrypt";
import prisma from "../utils/prisma.utils";
import {  genrateOtp, toTitleCase } from "../utils/utils";
import { createUserInput } from '../dtos/User.dto';
import {createHmac} from "crypto";
import { sendVerificationEmail } from "./email.service";


export async function createUserOrganizationService(params:createUserInput) {
   
    try {
       
        const  newUser = await prisma.user.create({
            data:{
                firstName: toTitleCase(params.firstName),
                lastName:toTitleCase(params.lastName),
                email:params.email.toLowerCase(),
                phone:params.phone,
                isActive:true,
            profile:{
                create:{
                    role:"ADMIN",
                    organization:{
                        create:{
                            name: toTitleCase(params.organizationName)
                        }
                    }
                }
            } }
        })
        if(!newUser)  throw Error('Could not create user');
        return newUser;
    
    } catch (error) {
        console.log(error)
        throw Error('Could not create user');
    }
   
}


interface userlogin {
    email:string
}
export async function LoginService(params:userlogin) {
    
    try {
        const user  = await prisma.user.findUnique({
            where:{
                email:params.email.toLowerCase()
            },
        })
        if(!user) throw new Error ('User not found')
        return user
    
    } catch (error) {
        console.log(error)
        return false
    }
   
}



const key ="otklwbfoiJKJBJKjkdbkajapeky"


export async  function createOtpService(medium:string, callback:Function) {
        const otp = genrateOtp();
        const ttl = 5 * 60 * 1000; // 5 minutes
        const expires = Date.now() + ttl;
        const data =`${medium}.${otp}.${expires}`;
        const hash = createHmac("sha256",key).update(data).digest("hex");
        const fullHash = `${hash}.${expires}`
        await sendVerificationEmail(medium,otp)
        // TODO send SMS notification somtime
        
        return callback(null, fullHash)
    }

export async function verifyOtpService(params:{otp:number,medium:string,hash:string},callback:Function){
    let [hashValue,expires] = params.hash.split('.');
    let now = Date.now();
    if(now > parseInt(expires)) return callback('OTP Expired')

    let data = `${params.medium}.${params.otp}.${expires}`;
    let newCalculatedHash = createHmac("sha256",key).update(data).digest("hex");
    if(newCalculatedHash === hashValue) return callback(null,'success')
    return callback('Invalid OTP')
}