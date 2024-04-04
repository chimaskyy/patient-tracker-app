import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import avatar from "../assets/images/avatar.png";

import IconButton from "@mui/material/IconButton";
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';

const Patients = () => {
  const [data, setData] = useState([]);
  const [search, setSearch] = useState("");

  const apiURL = import.meta.env.VITE_API_BASE_URL;
  
  const URL = `${apiURL}/api/v1/patients`;

  useEffect(() => {
    axios
      .get(URL)
      .then((response) => {
        setData(response.data.data);
        console.log(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div className="h-screen">
      <div className="w-full text-center">
        <input
          className="border rounded mt-5 text-center p-1 w-1/3 md:w-1/4 lg:w-1/5"
          placeholder="search by name"
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>
      {data &&
        data
          .filter((item) => {
            return search.toLowerCase() === ""
              ? item
              : item.first_name.toLowerCase().includes(search.toLowerCase()) ||
                  item.last_name.toLowerCase().includes(search.toLowerCase());
          })
          .map((patient) => (
            <div
              key={patient.email}
              className="my-2 mx-1 rounded-md flex items-start justify-between p-5 border"
            >
              <div>
                <img
                  src={avatar}
                  alt="patient-image"
                  className="w-12 h-12 rounded-full bg-gray-300"
                />
                <h3 className="text-gray-600">{patient.first_name} {patient.last_name}</h3>
              </div>
              <div>
                <p className="text-gray-600 pt-11">Email: {patient.email}</p>
              </div>
              <div className="pt-11">
                <IconButton>
                  <EditIcon fontSize="small"/>
                </IconButton>
              </div>
              <div className="pt-11">
                <IconButton size="small">
                    <DeleteIcon fontSize="small"/>
                </IconButton>
              </div>
              <Link 
              to={`/patients/${patient.id}/user-dashboard`} className="pt-11">view patient's details</Link>
            </div>
          ))}
    </div>
  );
};

export default Patients;
