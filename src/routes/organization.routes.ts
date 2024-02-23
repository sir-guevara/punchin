import { loginController, registerController, verifyOtpController } from "../controllers/user.controller";
import express from "express";
import { authMiddleware } from "../middlewares/auth.midlleware";
import { addUserToOrganizationController } from "../controllers/organization.controller";
import { validate } from "../utils/utils";
import { AddUserToOrgDTO } from "../dtos/User.dto";
const organizationRoute  = express.Router()

organizationRoute.post('/adduser', validate(AddUserToOrgDTO) ,addUserToOrganizationController)

export default organizationRoute