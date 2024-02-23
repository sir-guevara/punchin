import { LoginService, createOtpService, createUserOrganizationService, verifyOtpService } from "../services/user.service";
import { Request, Response } from 'express';
import { signJwt } from "../utils/jwt.utils";

export async function registerController(req:Request,res:Response) {
    try {
        const body = req.body ;
        // const value = await createUserSchema.validateSync(body);TODO
        const data = body! 
        //@ts-ignore
        const user = await createUserOrganizationService({firstName:data.firstName,lastName: data.lastName, email: data.email, organizationName:data.organizationName , phone:data.phone});
        res.status(201).json({
            message: "User Organization Created Successfully",
            user
        })
    } catch (error:any) {
        console.log(error);
        return res.status(500).json(error.message)
    }
}

export async function loginController(req: Request, res: Response){
    try{
        const body = req.body;
        const user = await LoginService(body)
        //@ts-ignore
        createOtpService(user.email,(error,result)=>{
            if(error){
                return res.status(401).json(error)
            }
           
            return res.status(200).json({
                     //@ts-ignore
                message: "OTP Sent Successfully to " + user.email, userId: user.id,
                result
            })
        })
    }
    catch (error:any) {
        console.log({error});
        return res.status(500).json(error.message)
    }
}

export async function verifyOtpController(req: Request, res: Response){
    try{
        const body = req.body;
        const params ={
            medium:body.medium,
            otp:body.otp,
            hash:body.hash,
        }
        verifyOtpService(params, (error?:string,result?:string)=>{
            if(error){
                return res.status(401).json(error)
            }
             //@ts-ignore
             const accessToken = signJwt({userId:body.userId},  {expiresIn:3*30*24*60*60})
            return res.status(200).json({
                message: "OTP Verified Successfully",
                accessToken
            })
        })
       
    }
    catch (error:any) {
        console.log({error});
        return res.status(500).json(error.message)
    }
}
