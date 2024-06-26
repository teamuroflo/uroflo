import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { ReactTyped } from "react-typed";
import uroflo_logo from "../assets/uroflo_blue_full.svg";

const Landing = () => {
  let resetInitiated = true;
  const navigate = useNavigate();
  const [showText, setShowText] = useState(false);
  const [showTapAnywhere, setShowTapAnywhere] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowText(true);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (showText) {
      const timer = setTimeout(() => {
        setShowTapAnywhere(true);
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [showText]);

  const begin = () => {
    navigate("/start", { state: { resetInitiated } });
  };

  const click = () => {
    const url = "http://localhost:8000/interface/click";
    const data = {
      click: "TRUE",
    };
    axios
      .post(url, data)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  return (
    <button
      className="w-screen h-screen bg-slate-950 flex flex-row justify-center items-center relative"
      onClick={() => {
        begin();
        click();
      }}
    >
      <img
        src={uroflo_logo}
        alt="uroflo logo"
        className="w-2/3 h-2/3 animate-fadeInMoveLeft"
      />
      {showText && (
        <ReactTyped
          strings={["Urine in good hands."]}
          typeSpeed={40}
          className="text-5xl text-slate-200 absolute left-[50%] italic"
        />
      )}
      {showTapAnywhere && (
        <p className="animate-fadeIn transition-opacity text-3xl text-slate-200 absolute bottom-0 mb-12 text-center w-full">
          Tap to begin
        </p>
      )}
    </button>
  );
};

export default Landing;
