import { Request, Response, NextFunction } from "express";
import * as yup from "yup";
export function toTitleCase(str?:string){
    if(!str) return '';
    return  str.toLowerCase().replace(/\b\w/g, s => s.toUpperCase());
}

export const validate =
  (schema: yup.AnyObject) =>
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      await schema.validateSync(req.body);
      return next();
    } catch (error:any) {
      return res.status(400).json(error.message);
    }
  };


export function genrateOtp(): number {
    const randomNumber = Math.floor(Math.random() * 900000);
    return randomNumber + 100000;
  }