import { NextFunction , Request, Response} from "express"
import { verifyJwt } from "../utils/jwt.utils"


export function authMiddleware(req:Request, res:Response , next:NextFunction){

    const accessToken  = req.headers['x-auth-token'] as string

    if(!accessToken) return res.status(401).json({message: 'invalid access token'})

    const {payload,isValid,expired} = verifyJwt(accessToken)
    if(!isValid) return res.status(401).json({message: 'No access token'})
    if(expired) return res.status(401).json({message: 'Access token has expired'})
    //@ts-ignore
    res.locals.userId = payload?.userId
    next()

}