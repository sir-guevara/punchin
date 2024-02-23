import prisma from "../utils/prisma.utils"
import { toTitleCase } from "../utils/utils"

type AddUserToOrgI ={
    firstName: string,
    lastName: string,
    phone: string,
    email: string,
    organizationId: string
    

}
export async function addUserToOrganizationService(params: AddUserToOrgI){
    try {
     const user = await   prisma.user.create({
            data:{
                firstName: toTitleCase(params.firstName),
                lastName: toTitleCase(params.lastName),
                email: params.email.toLowerCase(),
                phone: params.phone,
                profile:{
                    create:{
                        organization:{
                            connect:{
                                id:params.organizationId
                            }
                        }
                    }
                }
            }
        })
        return user
    } catch (error:any) {
        console.log(error)
        throw new Error(error)
    }
}

export async function getUserOrganizationService(userId:string){
    try {
        const user = await prisma.user.findUnique({
            where:{
                id:userId
            },
            select:{
                profile:{
                    select:{
                        organization:{
                            select:{
                                id:true
                            }
                        }
                    }
                }
            }
        })
        return user
    } catch (error:any) {
        console.log(error)
        throw new Error(error)
    }
}