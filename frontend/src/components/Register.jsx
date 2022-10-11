import React, { useContext, useEffect, useState } from 'react'
import { useForm } from 'react-hook-form';
import { UserContext } from '../context/UserContext'

const Register = () => {
    const {register, handleSubmit, formState:{ isSubmitting, errors}, watch} = useForm();

    const [errorMessage, setErrorMessage] = useState("");
    const [,setToken] = useContext(UserContext);

    const submitRegistration = async (data) => {
        const response = await fetch("/api/users", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: data.email,
                username: data.username,
                company_name: data.companyName,
                hashed_password: data.password,
                confirm_password: data.confirmPassword
            })
        })

        const result = await response.json();

        if (!response.ok) {
            if (typeof result.detail === "string") {
                setErrorMessage(result.detail);
            } else {
                setErrorMessage(result.detail[0].msg);
            }
        } else {
            setErrorMessage("");
            setToken(result.access_token);
        }
    }

  return (
    <div className="column">
        <form className="box" onSubmit={handleSubmit(submitRegistration)}>
            <h1 className="title has-text-centered">Register</h1>

            <div className="field">
              <label className="label">Email Address</label>
                <div className="control">
                    <input
                        type="email"
                        placeholder="Enter email"
                        className="input"
                        required
                        {...register("email")}
                    />
                </div>
            </div>

            <div className="field">
              <label className="label">Username</label>
                <div className="control">
                    <input
                        type="text"
                        placeholder="Username"
                        className="input"
                        required
                        {...register("username")}
                    />
                </div>
            </div>

            <div className="field">
              <label className="label">Company Name</label>
                <div className="control">
                    <input
                        type="text"
                        placeholder="Company Name"
                        className="input"
                        required
                        {...register("companyName")}
                    />
                </div>
            </div>

            <div className="field">
              <label className="label">Password</label>
                <div className="control">
                    <input
                    type="password"
                    placeholder="Password"
                    className="input"
                    required
                    {...register("password")}
                    />
                </div>
            </div>

            <div className="field">
              <label className="label">Confirm Password</label>
                <div className="control">
                    <input
                        type="password"
                        placeholder="Confirm Password"
                        className="input"
                        required
                        {...register("confirmPassword")}
                    />
                </div>
            </div>

            {errorMessage && <small style={{ color: "red"}}>{errorMessage}</small>}
            <br />
            <button className='button is-primary' type='submit' disabled={isSubmitting}>
                Register
            </button>
            
        </form>
    </div>
  )
}

export default Register;