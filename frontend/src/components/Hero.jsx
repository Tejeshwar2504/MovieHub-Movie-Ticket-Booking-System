import { useNavigate } from "react-router-dom";

import { getMovieImage } from "../utils/movieImages";

import "../styles/Hero.css";


function Hero() {

    const navigate = useNavigate();


    const handleBooking = () => {

        navigate("/movies");

    };


    return (

        <section className="hero">


            <div className="hero-background">

                <img
                    src={getMovieImage("Cinema.jpg")}
                    alt="MovieHub Cinema"
                />

            </div>

            <div className="hero-overlay"></div>

            <div className="hero-content">

                <span className="hero-small-title">
                    🎬 WELCOME TO MOVIEHUB
                </span>


                <h1>
                    Lights.
                    <br />
                    Camera.
                    <br />
                    Your Movie Experience.
                </h1>


                <p>
                    Discover the latest movies, explore nearby theatres, choose your preferred showtime and seats, and book your tickets effortlessly — all in one place.
                </p>


                <div className="hero-buttons">

                    <button
                        type="button"
                        className="hero-book-btn"
                        onClick={handleBooking}
                    >

                        🎟️ Book Now

                    </button>


                    <button
                        type="button"
                        className="hero-movies-btn"
                        onClick={() =>
                            navigate("/movies")
                        }
                    >

                        🎬 Explore Movies

                    </button>

                </div>

            </div>

            <div className="hero-bottom-fade"></div>

        </section>

    );

}


export default Hero;
