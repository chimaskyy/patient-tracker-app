import { Link } from "react-router-dom";
import { useState } from "react";
import MenuIcon from "@mui/icons-material/Menu";
import { MenuOpen } from "@mui/icons-material";
import HomeIcon from "@mui/icons-material/Home";

const Header = (props) => {
  const [activePage, setActivePage] = useState("home");

  const toggleMenuHandler = (e) => {
    e.stopPropagation();
    props.setMenuVisible(!props.menuVisible);
  };

  return (
    <header className="bg-blue-700 sticky top-0 z-20">
      <div className="max-w-7xl mx-auto items-center flex justify-between p-2.5">
        <div>
          <Link to="/">
            <span className="flex md:hidden text-slate-200">
              <HomeIcon />
            </span>
            <span className="hidden md:flex">Home</span>
          </Link>
        </div>
        <div onClick={toggleMenuHandler} className="md:hidden text-slate-200">
          {props.menuVisible ? <MenuOpen /> : <MenuIcon />}
        </div>
        <nav
          className={`${
            !props.menuVisible && "hidden"
          } absolute z-20 bg-blue-100 flex flex-col top-full right-0 p-2
          md:static md:w-auto md:bg-inherit md:p-0 md:flex`}
        >
          <ul nav-bar="nav" className="md:flex md:flex-row">
            <li className="list-none py-2 border-b border-blue-900 border-opacity-25 mr-4 md:text-white">
              <Link
                to="/our-doctors"
                className={`w-full flex text-base md:hover:text-blue-200 cursor-pointer
                ${
                  activePage === "our-doctors" &&
                  "text-blue-700 md:text-blue-200"
                }`}
                onClick={() => setActivePage("our-doctors")}
              >
                Our Doctor
              </Link>
            </li>
            <li className="list-none py-2 border-b border-blue-900 border-opacity-25 mr-4 md:text-white">
              <Link
                to="/about"
                className={`w-full flex text-base md:hover:text-blue-200 cursor-pointer
                ${activePage === "about" && "text-blue-700 md:text-blue-200"}`}
                onClick={() => setActivePage("about")}
              >
                About
              </Link>
            </li>
            <li className="list-none py-2 border-b border-blue-900 border-opacity-25 mr-4 md:text-white">
              <Link
                to="/services"
                className={`w-full flex text-base md:hover:text-blue-200 cursor-pointer
                ${
                  activePage === "services" && "text-blue-700 md:text-blue-200"
                }`}
                onClick={() => setActivePage("services")}
              >
                Services
              </Link>
            </li>
            <li className="list-none py-2 border-b border-blue-900 border-opacity-25 mr-4 md:text-white">
              <Link
                to="/login"
                className={`w-full flex text-base md:hover:text-blue-200 cursor-pointer
                ${activePage === "login" && "text-blue-700 md:text-blue-200"}`}
                onClick={() => setActivePage("login")}
              >
                Login
              </Link>
            </li>
            <li className="list-none py-2 mr-4 md:text-white">
              <Link
                to="/create-report"
                className={`w-full flex text-base md:hover:text-blue-200 cursor-pointer
                ${
                  activePage === "create-report" &&
                  "text-blue-700 md:text-blue-200"
                }`}
                onClick={() => setActivePage("create-report")}
              >
                Create Report
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;