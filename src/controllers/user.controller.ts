import { createUserOrganizationService } from "../services/user.service";
import { Request, Response } from 'express';

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