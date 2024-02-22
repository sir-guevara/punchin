import jwt from "jsonwebtoken"


export function signJwt(object:Object,options?:jwt.SignOptions | undefined){
    const privateKey = process.env.TOKEN_SECRET!

// console.log({privateKey})
    return jwt.sign(object, privateKey,{
        ...(options && options ),
    })
}


export function verifyJwt(token : string){
    const privateKey = process.env.TOKEN_SECRET!

    try {
        const payload = jwt.verify(token, privateKey)
        
        return {
            isValid:true,
            expired: false,
            payload
        }
    } catch (e: any) {
        if(e.message == 'jwt expired'){
            return {
            isValid:true,
            expired:true,
            payload: null
        }
        }
        return {
            isValid:false,
            expired: e.message == 'jwt expired',
            payload: null
        }
    }
}