import { useState } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

import "../styles/AdminLogin.css";


function AdminLogin() {

    const navigate = useNavigate();

    const [username, setUsername] = useState("");

    const [password, setPassword] = useState("");

    const [error, setError] = useState("");

    const [loading, setLoading] = useState(false);

    const handleAdminLogin = (e) => {

        e.preventDefault();

        setError("");

        if (!username || !password) {

            setError(
                "Please enter username and password"
            );

            return;

        }


        setLoading(true);

        const adminUsername = "Tejesh";

        const adminPassword = "Tejesh654321";

        if (
            username === adminUsername &&
            password === adminPassword
        ) {

            // Save admin login
            localStorage.setItem(
                "admin",
                "true"
            );


            alert(
                "Admin Login Successful 🎬"
            );


            // Go to Admin Movies
            navigate(
                "/admin/movies"
            );

        }

        else {

            setError(
                "Invalid admin username or password"
            );

        }


        setLoading(false);

    };

    return (

        <>

            <Navbar />


            <div className="admin-login-page">


                <div className="admin-login-card">

                    <div className="admin-login-icon">
                        🔐
                    </div>


                    <h1>
                        MovieHub
                    </h1>


                    <h2>
                        Admin Login
                    </h2>


                    <p className="admin-login-subtitle">
                        Login to access the admin dashboard
                    </p>

                    {error && (

                        <div className="admin-login-error">

                            ⚠️ {error}

                        </div>

                    )}

                    <form
                        onSubmit={
                            handleAdminLogin
                        }
                    >


                        {/* USERNAME */}

                        <div className="admin-input-group">

                            <label>
                                Username
                            </label>


                            <input
                                type="text"
                                placeholder="Enter admin username"
                                value={username}
                                onChange={(e) =>
                                    setUsername(
                                        e.target.value
                                    )
                                }
                            />

                        </div>


                        {/* PASSWORD */}

                        <div className="admin-input-group">

                            <label>
                                Password
                            </label>


                            <input
                                type="password"
                                placeholder="Enter admin password"
                                value={password}
                                onChange={(e) =>
                                    setPassword(
                                        e.target.value
                                    )
                                }
                            />

                        </div>


                        {/* LOGIN BUTTON */}

                        <button
                            type="submit"
                            disabled={loading}
                            className="admin-login-btn"
                        >

                            {loading
                                ? "Logging in..."
                                : "Admin Login 🔐"}

                        </button>


                    </form>

                    <button
                        type="button"
                        className="admin-back-btn"
                        onClick={() =>
                            navigate("/")
                        }
                    >

                        ← Back To Home

                    </button>


                </div>

            </div>


            <Footer />

        </>

    );

}


export default AdminLogin;
