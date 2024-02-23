import nodemailer from 'nodemailer';

const mailSender = async (email:string, title:string, body:any) => {
  try {
    // Create a Transporter to send emails
    let transporter = nodemailer.createTransport({
        host: process.env.SMTP_HOST,
        port:  2525,
        secure: false, // upgrade later with STARTTLS
        auth: {
          user:  process.env.SMTP_USER,
          pass: process.env.SMTP_PASSWORD,
        },
      });
    // Send emails to users
    let info = await transporter.sendMail({
      from: 'Punchin - Administrator',
      to: email,
      subject: title,
      html: body,
    });
    console.log("Email info: ", info);
    return info;
  } catch (error:any) {
    console.log(error.message);
  }
};

// Define a function to send emails
export async function sendVerificationEmail(email:string, otp:number) {
    try {
      const mailResponse = await mailSender(
        email,
        "Verification Email",
        `<h1>Please confirm your OTP</h1>
         <p>Here is your OTP code: ${otp}</p>`
      )
      console.log("Email sent successfully: ", mailResponse);
    } catch (error) {
      console.log("Error occurred while sending email: ", error);
      throw error;
    }
  }