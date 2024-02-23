import express, {
    ErrorRequestHandler,
    Express,
  } from "express";



  import * as dotenv from "dotenv";
import morgan from "morgan";

import indexRoute from "./routes/index.routes";
import organizationRoute from "./routes/organization.routes";
import { authMiddleware } from "./middlewares/auth.midlleware";


const app: Express = express();

dotenv.config();


const PORT = process.env.PORT || 4000;
app.use(express.json());
app.use(morgan("dev"));
app.use(express.urlencoded({ extended: false }));


// routes
app.use("/", indexRoute);
app.use("/organization",authMiddleware, organizationRoute);



// server start
const start = async function () {
    try {
      await app.listen(PORT);
      console.log(`Server started 🚀 at http://locahost:${PORT}`);
    } catch (error) {
      console.log(`Server Error  ⛔️`, error);
    }
  };
  
  start();
