import { Response,Request } from "express";import { addUserToOrganizationService, getUserOrganizationService } from "../services/organization.service";

export async function addUserToOrganizationController(req:Request,res:Response){ 
    try {
        const body = req.body;
        const userOrg = await getUserOrganizationService(res.locals.userId);
        const user = await addUserToOrganizationService({firstName:body.firstName,lastName: body.lastName, email: body.email, organizationId:userOrg?.profile?.organization.id!, phone:body.phone});
        res.status(201).json({
            message: "User Added to organization",
            user
        })
    } catch (error:any) {
        console.log(error);
        return res.status(500).json(error.message)
    }
}