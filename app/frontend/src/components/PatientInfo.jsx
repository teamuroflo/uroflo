import { useEffect, useState } from "react";
import axios from "axios";

function formatDOB(dob) {
  let dobDate = new Date(dob);
  let month = String(dobDate.getMonth() + 1).padStart(2, "0"); // Months are 0-indexed in JavaScript
  let day = String(dobDate.getDate()).padStart(2, "0");
  let year = dobDate.getFullYear();
  dob = month + "/" + day + "/" + year;
  return dob;
}

const PatientInfo = () => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [mrn, setMRN] = useState("");
  let [dob, setDOB] = useState("");
  const [sex, setSex] = useState("");
  const [contactA, setContactA] = useState("");
  const [contactB, setContactB] = useState("");
  const [activeTime, setActiveTime] = useState(0);

  let days = Math.floor(activeTime / 1440);
  let hours = Math.floor(activeTime / 60);
  let minutes = activeTime % 60;

  function calculateAge(dob) {
    const dobDate = new Date(dob);
    const today = new Date();

    let age = today.getFullYear() - dobDate.getFullYear();
    const m = today.getMonth() - dobDate.getMonth();

    if (m < 0 || (m === 0 && today.getDate() < dobDate.getDate())) {
      age--;
    }

    return age;
  }

  let age = calculateAge(dob);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/patient") // replace with your API endpoint
        .then((response) => setFirstName(response.data.firstname)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/patient") // replace with your API endpoint
        .then((response) => setLastName(response.data.lastname)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/patient") // replace with your API endpoint
        .then((response) => setMRN(response.data.MRN)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/patient") // replace with your API endpoint
        .then((response) => setDOB(response.data.DOB)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/patient") // replace with your API endpoint
        .then((response) => setSex(response.data.sex)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/patient") // replace with your API endpoint
        .then((response) => setContactA(response.data.contact_A)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/patient") // replace with your API endpoint
        .then((response) => setContactB(response.data.contact_B)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      axios
        .get("http://localhost:8000/system") // replace with your API endpoint
        .then((response) => setActiveTime(response.data.active_time)) // replace 'rate' with the actual key in the response
        .catch((error) => console.error(error));
    }, 1000); // fetch every 1 second

    return () => clearInterval(intervalId); // clean up on component unmount
  }, []);

  dob = formatDOB(dob);

  return (
    <div className="h-full w-full flex flex-row text-slate-200">
      <div className="h-full w-[60%] flex flex-col items-start justify-end">
        <div className="text-xl flex flex-col items-start">
          <p className="text-3xl font-bold">
            {lastName}, {firstName} ({age} {sex})
          </p>
          <p>MRN: {mrn}</p>
          <p>DOB: {dob}</p>
        </div>
      </div>
      <div className="h-full w-[40%] flex flex-col items-end justify-end">
        <div className="text-xl flex flex-col items-end">
          <p>
            {days} d {hours} h {minutes} min ACTIVE
          </p>
          <p>CONTACT A: {contactA}</p>
          <p>CONTACT B: {contactB}</p>
        </div>
      </div>
    </div>
  );
};

export default PatientInfo;
