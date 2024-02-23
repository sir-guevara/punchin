// dtos/UserDTO.ts

import * as yup from 'yup';

export const CreateUserAndOrgDTO = yup.object().shape({
  firstName: yup.string().required('First name is required').min(3),
  lastName: yup.string().required('Last name is required').min(3),
  phone: yup.string().required('Phone number is required'),
  email: yup.string().email().required('Email is required'),
  organizationName: yup.string().required('Organization name is required').min(3, 'Organization name must be at least 3 characters')
});



export const LoginDto = yup.object().shape({
  email: yup.string().email().required('Email is required'),
});

export const OTPDto = yup.object().shape({
  medium: yup.string().required('medium is required'),
  otp: yup.number().required('OTP code is required'),
  hash: yup.string().required('hash is required'),
  userId: yup.string().required('userId is required'),
});


export const AddUserToOrgDTO = yup.object().shape({
  firstName: yup.string().required('First name is required').min(3),
  lastName: yup.string().required('Last name is required').min(3),
  phone: yup.string().required('Phone number is required'),
  email: yup.string().email().required('Email is required')
});



export type createUserInput = yup.InferType<typeof CreateUserAndOrgDTO>;
