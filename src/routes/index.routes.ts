import { loginController, registerController, verifyOtpController } from "../controllers/user.controller";
import express from "express";
import { validate } from "../utils/utils";
import { CreateUserAndOrgDTO, LoginDto, OTPDto } from "../dtos/User.dto";

const indexRoute  = express.Router()

indexRoute.post("/register",validate(CreateUserAndOrgDTO) ,registerController)
indexRoute.post("/auth",validate(LoginDto) ,loginController)
indexRoute.post("/auth/otp",validate(OTPDto) ,verifyOtpController)


export default indexRoute