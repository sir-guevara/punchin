import { registerController } from "../controllers/user.controller";
import express from "express";

const indexRoute  = express.Router()

indexRoute.post("/register",registerController)


export default indexRoute