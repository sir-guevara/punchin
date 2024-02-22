import bcrypt from "bcrypt";
import prisma from "../utils/prisma.utils";
import {  toTitleCase } from "../utils/utils";


export async function createUserOrganizationService(params:{email:string, phone:string, firstName:string, lastName:string,organizationName:string}) {
   
    try {
       
        const  newUser = await prisma.user.create({
            data:{
                firstName: toTitleCase(params.firstName!),
                lastName:toTitleCase(params.lastName!),
                email:params.email?.toLowerCase(),
                phone:params.phone!,
            profile:{
                create:{
                    organization:{
                        create:{
                            name: toTitleCase(params.organizationName!)
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


export async function addUserToOrganizationService(params:{email:string, phone:string, firstName:string, lastName:string,organizationName?:string,}) {
   
    try {
       
        const  newUser = await prisma.user.create({
            data:{firstName: toTitleCase(params.firstName!),lastName:toTitleCase(params.lastName!), email:params.email?.toLowerCase(),phone:params.phone!,
            profile:{
                create:{
                    organization:{
                        create:{
                            name: toTitleCase(params.organizationName!)
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
        // TODO generate OTP
        return user
    
    } catch (error) {
        console.log(error)
        return false
    }
   
}